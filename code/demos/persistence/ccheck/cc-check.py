#!/usr/bin/env python3
"""
cc-check.py - Crash Consistency Checker (simplified C³)

Usage:
    python3 cc-check.py [--workdir DIR] [--bound K] -- <cmd> [args...]

Traces file system syscalls via strace, simulates crash sites,
and outputs a single JSON to stdout containing all snapshots.

Target: Linux (requires strace)
Output: JSON to stdout, logs to stderr
"""

import argparse
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
import shutil
import tempfile
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

# ─── Syscall Event Model ─────────────────────────────────────────────

@dataclass
class SyscallEvent:
    index: int
    syscall: str
    args: list
    result: int
    path: str = ""
    path2: str = ""
    data: bytes = b""
    data_truncated: bool = False
    offset: int = -1
    is_metadata: bool = False

    @property
    def is_barrier(self):
        return self.syscall in ("fsync", "fdatasync", "sync", "syncfs")

    @property
    def is_write_data(self):
        return self.syscall in ("write", "pwrite64")


# ─── strace Parsing ──────────────────────────────────────────────────

TRACE_SYSCALLS = ",".join([
    "open", "openat", "creat",
    "read", "pread64",
    "write", "pwrite64",
    "close",
    "fsync", "fdatasync", "sync", "syncfs",
    "rename", "renameat", "renameat2",
    "unlink", "unlinkat",
    "mkdir", "mkdirat",
    "rmdir",
    "link", "linkat",
    "symlink", "symlinkat",
    "truncate", "ftruncate",
    "lseek",
    "dup", "dup2", "dup3",
])

RE_LINE = re.compile(
    r'^\s*(\d+)\s+'
    r'(\w+)\('
    r'(.*)'
    r'\)\s*=\s*(-?\d+)'
    r'(?:<([^>]*)>)?'
    r'(?:\s+[A-Z]+.*)?$'
)
RE_FD_PATH = re.compile(r'<([^>]+)>')
RE_STRING = re.compile(r'"((?:[^"\\]|\\.)*)"')
RE_HEX = re.compile(r'\\x([0-9a-fA-F]{2})')


def _strip_fd_ann(s: str) -> str:
    """Remove strace -y annotation: '3</tmp/foo>' -> '3'."""
    return re.sub(r'\d+<[^>]*>', lambda m: m.group(0).split('<')[0], s)


def _parse_int(s: str) -> Optional[int]:
    s = _strip_fd_ann(s.strip().rstrip(",").rstrip(")"))
    try:
        return int(s, 0)
    except (ValueError, TypeError):
        return None


def _decode_hex_path(s: str) -> str:
    """Decode strace -xx hex-encoded path from -y annotation.
    E.g., '\\x2f\\x74\\x6d\\x70' -> '/tmp'."""
    if not s or '\\x' not in s:
        return s
    try:
        result = bytearray()
        i = 0
        while i < len(s):
            if s[i] == '\\' and i + 3 < len(s) and s[i+1] == 'x':
                result.append(int(s[i+2:i+4], 16))
                i += 4
            else:
                result.append(ord(s[i]))
                i += 1
        return bytes(result).decode("utf-8", errors="replace")
    except (ValueError, UnicodeDecodeError):
        return s


def _decode_str(s: str) -> str:
    """Decode a strace -xx hex-encoded string to a normal string.
    E.g., '\\x2f\\x74\\x6d\\x70' -> '/tmp'. Handles both hex and plain text."""
    if not s or '\\x' not in s:
        return s
    return decode_strace_string(s).decode("utf-8", errors="replace")


def extract_fd_path(s: str) -> Optional[str]:
    m = RE_FD_PATH.search(s)
    return _decode_hex_path(m.group(1)) if m else None


def decode_strace_string(s: str) -> bytes:
    result = bytearray()
    i = 0
    while i < len(s):
        m = RE_HEX.match(s, i)
        if m:
            result.append(int(m.group(1), 16))
            i = m.end()
        elif s[i] == '\\' and i + 1 < len(s):
            esc = s[i + 1]
            if   esc == 'n':    result.append(10)
            elif esc == 't':    result.append(9)
            elif esc == 'r':    result.append(13)
            elif esc == '\\':   result.append(92)
            elif esc == '"':    result.append(34)
            elif esc == '0':    result.append(0)
            else:               result.append(ord(esc))
            i += 2
        else:
            result.append(ord(s[i]))
            i += 1
    return bytes(result)


def log(msg: str):
    print(msg, file=sys.stderr)


def parse_strace_log(log_path: str, workdir: str) -> Tuple[List[SyscallEvent], Set[str]]:
    events: List[SyscallEvent] = []
    touched: Set[str] = set()
    # fd -> (path, tracked_offset)
    fd_table: Dict[int, Dict[int, Tuple[str, int]]] = defaultdict(dict)
    workdir_abs = os.path.abspath(workdir)
    idx = 0

    def _in(path: str) -> bool:
        if not path:
            return False
        p = os.path.abspath(path)
        return p == workdir_abs or p.startswith(workdir_abs + os.sep)

    # Buffer for strace unfinished/resumed line pairs
    unfinished: Dict[int, str] = {}

    RE_RESUMED = re.compile(r'^\s*(\d+)\s+<\.\.\.\s+(\w+)\s+resumed>\)\s*=\s*(-?\d+)(?:<([^>]*)>)?(?:\s+[A-Z]+.*)?$')

    with open(log_path, "r", errors="replace") as f:
        for line in f:
            line = line.strip()

            # Handle resumed lines: merge with unfinished buffer
            rm = RE_RESUMED.match(line)
            if rm:
                r_pid_str, r_syscall, r_ret_str, r_ret_path = rm.groups()
                r_pid = int(r_pid_str)
                if r_pid in unfinished:
                    # Reconstruct: "PID syscall(args) = ret[<path>]"
                    line = f"{r_pid} {r_syscall}({unfinished.pop(r_pid)}) = {r_ret_str}"
                    if r_ret_path:
                        line += f"<{r_ret_path}>"
                else:
                    continue  # orphan resumed line, skip
            elif "<unfinished ...>" in line:
                # Buffer the unfinished args for later merging
                m = re.match(r'^\s*(\d+)\s+(\w+)\((.*)\s+<unfinished\s+\.\.\.>$', line)
                if m:
                    unfinished[int(m.group(1))] = m.group(3)
                continue

            m = RE_LINE.match(line)
            if not m:
                continue
            m_groups = m.groups()
            pid_str, syscall, args_str, ret_str = m_groups[:4]
            ret_path = _decode_hex_path(m_groups[4]) if len(m_groups) > 4 and m_groups[4] else ""
            pid, ret = int(pid_str), int(ret_str)
            if ret < 0:
                continue

            path, path2, data, offset = "", "", b"", -1
            truncated = False
            is_metadata = False

            # ── open/openat/creat ──
            if syscall in ("open", "openat", "creat"):
                strings = RE_STRING.findall(args_str)
                if strings:
                    path = _decode_str(strings[0])
                # Prefer ret_path (from -y annotation on return value) over
                # path extracted from args, since args may have a dirfd path
                # (for openat) or a relative path that ret_path resolves fully.
                p = ret_path or extract_fd_path(args_str)
                if p:
                    path = p
                if _in(path):
                    fd_table[pid][ret] = (path, 0)
                    touched.add(path)
                is_metadata = True

            # ── close ──
            elif syscall == "close":
                parts = args_str.split(",", 1)
                fd_arg = _parse_int(parts[0]) if parts else None
                p = extract_fd_path(parts[0]) if parts else None
                if p:
                    path = p
                elif fd_arg is not None:
                    entry = fd_table.get(pid, {}).get(fd_arg)
                    path = entry[0] if entry else ""
                if fd_arg is not None and _in(path):
                    fd_table.get(pid, {}).pop(fd_arg, None)
                is_metadata = True

            # ── lseek ──
            elif syscall == "lseek":
                parts = [p.strip() for p in args_str.split(",")]
                fd_arg = _parse_int(parts[0]) if parts else None
                if fd_arg is not None and fd_arg in fd_table.get(pid, {}):
                    old_path, cur_off = fd_table[pid][fd_arg]
                    whence_str = parts[2].strip() if len(parts) > 2 else "SEEK_SET"
                    new_off = _parse_int(parts[1]) if len(parts) > 1 else 0
                    if "SEEK_SET" in whence_str:
                        fd_table[pid][fd_arg] = (old_path, new_off or 0)
                    elif "SEEK_CUR" in whence_str:
                        fd_table[pid][fd_arg] = (old_path, cur_off + (new_off or 0))
                    elif "SEEK_END" in whence_str:
                        # approximate: use tracked content length from our file state
                        fd_table[pid][fd_arg] = (old_path, (new_off or 0))
                continue  # lseek doesn't generate an event

            # ── write / pwrite64 ──
            elif syscall in ("write", "pwrite64"):
                parts = [p.strip() for p in args_str.split(",")]
                p = extract_fd_path(parts[0])
                if p:
                    path = p
                else:
                    fd_arg = _parse_int(parts[0])
                    if fd_arg is not None:
                        entry = fd_table.get(pid, {}).get(fd_arg)
                        path = entry[0] if entry else ""
                str_matches = RE_STRING.findall(args_str)
                if str_matches:
                    raw_str = str_matches[0]
                    data = decode_strace_string(raw_str)
                    if raw_str.endswith("...") and ret < 4096:
                        # strace truncation marker: string ends with "..."
                        truncated = True
                if syscall == "pwrite64" and len(parts) >= 4:
                    # pwrite64(fd, buf, count, offset) — offset is parts[3]
                    off_val = _parse_int(parts[3])
                    if off_val is not None:
                        offset = off_val
                else:
                    # Regular write: use tracked fd offset
                    fd_arg = _parse_int(parts[0])
                    if fd_arg is not None and fd_arg in fd_table.get(pid, {}):
                        _, tracked_off = fd_table[pid][fd_arg]
                        offset = tracked_off
                # Update tracked offset after write (only for write, not pwrite64)
                if _in(path) and syscall == "write":
                    fd_arg = _parse_int(parts[0])
                    if fd_arg is not None and fd_arg in fd_table.get(pid, {}):
                        old_path, _ = fd_table[pid][fd_arg]
                        write_end = max(offset, 0) + len(data)
                        fd_table[pid][fd_arg] = (old_path, write_end)

            # ── read ──
            elif syscall in ("read", "pread64"):
                parts = [p.strip() for p in args_str.split(",")]
                p = extract_fd_path(parts[0])
                if p:
                    path = p
                else:
                    fd_arg = _parse_int(parts[0])
                    if fd_arg is not None:
                        entry = fd_table.get(pid, {}).get(fd_arg)
                        path = entry[0] if entry else ""
                if _in(path):
                    touched.add(path)
                # Update fd offset after read (only for read, not pread64)
                if _in(path) and syscall == "read":
                    fd_arg = _parse_int(parts[0])
                    if fd_arg is not None and fd_arg in fd_table.get(pid, {}):
                        old_path, off = fd_table[pid][fd_arg]
                        fd_table[pid][fd_arg] = (old_path, off + ret)

            # ── rename ──
            elif syscall in ("rename", "renameat", "renameat2"):
                strings = RE_STRING.findall(args_str)
                if len(strings) >= 2:
                    path, path2 = _decode_str(strings[0]), _decode_str(strings[1])
                elif len(strings) == 1:
                    path = _decode_str(strings[0])
                touched.add(path)
                if path2:
                    touched.add(path2)
                # Update fd_table: fds pointing to old path now point to new path
                if path and path2:
                    for pidd, fds in fd_table.items():
                        for fd, (fp, off) in list(fds.items()):
                            if fp == path:
                                fd_table[pidd][fd] = (path2, off)
                is_metadata = True

            # ── unlink ──
            elif syscall in ("unlink", "unlinkat", "rmdir"):
                strings = RE_STRING.findall(args_str)
                if strings:
                    path = _decode_str(strings[0])
                if path:
                    touched.add(path)
                # Update fd_table: fds pointing to unlinked file keep the path
                # (POSIX: fd remains valid after unlink of the directory entry)
                is_metadata = True

            # ── mkdir ──
            elif syscall in ("mkdir", "mkdirat"):
                strings = RE_STRING.findall(args_str)
                if strings:
                    path = _decode_str(strings[0])
                is_metadata = True

            # ── truncate/ftruncate ──
            elif syscall in ("truncate", "ftruncate"):
                if syscall == "truncate":
                    strings = RE_STRING.findall(args_str)
                    if strings:
                        path = _decode_str(strings[0])
                else:
                    parts = [p.strip() for p in args_str.split(",")]
                    p = extract_fd_path(parts[0]) if parts else None
                    if p:
                        path = p
                    else:
                        fd_arg = _parse_int(parts[0]) if parts else None
                        if fd_arg is not None:
                            entry = fd_table.get(pid, {}).get(fd_arg)
                            path = entry[0] if entry else ""
                is_metadata = True

            # ── fsync ──
            elif syscall in ("fsync", "fdatasync", "sync", "syncfs"):
                parts = [p.strip() for p in args_str.split(",")]
                p = extract_fd_path(parts[0]) if parts else None
                if p:
                    path = p
                else:
                    fd_arg = _parse_int(parts[0]) if parts else None
                    if fd_arg is not None:
                        entry = fd_table.get(pid, {}).get(fd_arg)
                        path = entry[0] if entry else ""
                is_metadata = True

            # ── dup ──
            elif syscall in ("dup", "dup2", "dup3"):
                parts = [p.strip() for p in args_str.split(",")]
                old_fd = _parse_int(parts[0])
                if old_fd is not None and old_fd in fd_table.get(pid, {}):
                    # dup2/dup3: if target fd (ret) was already open, implicitly close it
                    if syscall in ("dup2", "dup3") and ret in fd_table.get(pid, {}):
                        fd_table[pid].pop(ret, None)
                    fd_table[pid][ret] = fd_table[pid][old_fd]
                continue

            # ── link/symlink ──
            elif syscall in ("link", "linkat", "symlink", "symlinkat"):
                strings = RE_STRING.findall(args_str)
                if len(strings) >= 2:
                    path, path2 = _decode_str(strings[0]), _decode_str(strings[1])
                is_metadata = True

            else:
                continue

            if path and not _in(path):
                continue
            if path2 and not _in(path2):
                # For rename/link: destination path is in workdir but source
                # is not — skip this event entirely for safety
                if syscall in ("rename", "renameat", "renameat2",
                               "link", "linkat", "symlink", "symlinkat"):
                    continue
            # Allow barrier events (sync/fsync) and symlink (target outside workdir) even with empty path
            if not path and not path2 and syscall not in ("sync", "syncfs", "symlink", "symlinkat"):
                continue

            events.append(SyscallEvent(
                index=idx, syscall=syscall, args=args_str.split(","),
                result=ret, path=path, path2=path2, data=data,
                data_truncated=truncated, offset=offset,
                is_metadata=is_metadata,
            ))
            idx += 1

    return events, touched


# ─── Snapshot & Crash Simulator ──────────────────────────────────────

@dataclass
class FileState:
    content: bytearray = field(default_factory=bytearray)
    exists: bool = True


def take_snapshot(workdir: str) -> Dict[str, str]:
    """Take snapshot: {relative_path: base64(content)}."""
    snap = {}
    w = os.path.abspath(workdir)
    for root, dirs, files in os.walk(w, followlinks=False):
        for fname in files:
            fp = os.path.join(root, fname)
            # Skip non-regular files (FIFOs, sockets, devices) to avoid blocking
            if not os.path.isfile(fp) or os.path.islink(fp):
                continue
            try:
                with open(fp, "rb") as f:
                    snap[os.path.relpath(fp, w)] = base64.b64encode(f.read()).decode()
            except (OSError, PermissionError):
                pass
        # Record empty directories as special sentinel markers
        if not files and not dirs:
            rel = os.path.relpath(root, w)
            if rel != ".":
                snap[rel + "/"] = ""
    return snap


def snapshot_diff(initial: Dict[str, str], current: Dict[str, str]) -> Dict:
    """Compute diff between two snapshots for compact output."""
    diff = {"added": [], "removed": [], "modified": []}
    for p in current:
        if p not in initial:
            diff["added"].append(p)
        elif current[p] != initial.get(p):
            diff["modified"].append(p)
    for p in initial:
        if p not in current:
            diff["removed"].append(p)
    return diff


def snapshot_summary(snap: Dict[str, str]) -> Dict[str, Dict]:
    """Per-file size + sha256 for quick comparison."""
    summary = {}
    for p, b64 in snap.items():
        raw = base64.b64decode(b64)
        summary[p] = {
            "size": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest()[:32],
        }
    return summary


class CrashSimulator:
    def __init__(self, initial_snapshot: Dict[str, str], workdir: str):
        self.workdir = os.path.abspath(workdir)
        self.initial: Dict[str, FileState] = {}
        for p, b64 in initial_snapshot.items():
            self.initial[p] = FileState(bytearray(base64.b64decode(b64)), True)

    def _clone(self) -> Dict[str, FileState]:
        return {p: FileState(bytearray(f.content), f.exists)
                for p, f in self.initial.items()}

    @staticmethod
    def _copy(files: Dict[str, FileState]) -> Dict[str, FileState]:
        return {p: FileState(bytearray(f.content), f.exists)
                for p, f in files.items()}

    def _rel(self, p: str) -> str:
        return os.path.relpath(p, self.workdir) if p else ""

    @staticmethod
    def _snap(fs: Dict[str, FileState]) -> Dict[str, str]:
        return {p: base64.b64encode(bytes(f.content)).decode()
                for p, f in fs.items() if f.exists}

    def _apply(self, files: Dict[str, FileState], evt: SyscallEvent,
               mode: str = "normal"):
        """Apply event. mode: normal|drop|partial|empty."""
        if mode == "drop":
            return
        rel = self._rel(evt.path)

        if evt.syscall in ("open", "openat", "creat"):
            if rel not in files:
                files[rel] = FileState(bytearray(), True)
            else:
                # Re-opening a file that was previously unlinked: restore exists
                files[rel].exists = True
                # creat always truncates (O_TRUNC is implicit)
                if evt.syscall == "creat":
                    files[rel].content = bytearray()
                elif "O_TRUNC" in str(evt.args):
                    files[rel].content = bytearray()

        elif evt.syscall in ("write", "pwrite64"):
            if not evt.data or rel not in files or not files[rel].exists:
                return
            data = evt.data
            if mode == "partial":
                kept = 1
                while kept * 2 <= len(data):
                    kept *= 2
                data = data[:max(kept // 2, 0)]
            elif mode == "empty":
                data = b""
            off = evt.offset if evt.offset >= 0 else len(files[rel].content)
            end = off + len(data)
            if end > len(files[rel].content):
                files[rel].content.extend(b'\x00' * (end - len(files[rel].content)))
            files[rel].content[off:off + len(data)] = data

        elif evt.syscall in ("rename", "renameat", "renameat2"):
            if not evt.path2:
                return
            rel2 = self._rel(evt.path2)
            if rel == rel2:
                return  # POSIX: rename("a", "a") is a no-op
            if rel2 in files:
                # Atomically replace target if it exists
                files[rel2].exists = False
            if rel in files and files[rel].exists:
                files[rel2] = FileState(bytearray(files[rel].content), True)
                files[rel].exists = False

        elif evt.syscall in ("unlink", "unlinkat", "rmdir"):
            if rel in files:
                files[rel].exists = False

        elif evt.syscall in ("truncate", "ftruncate"):
            if rel in files and files[rel].exists:
                # Parse target size from the last numeric arg
                size = 0
                for arg in reversed(evt.args):
                    v = _parse_int(arg)
                    if v is not None:
                        size = v
                        break
                if size <= len(files[rel].content):
                    # Truncate (including to 0)
                    files[rel].content = files[rel].content[:size]
                else:
                    # Extend with zeros
                    files[rel].content.extend(b'\x00' * (size - len(files[rel].content)))

        elif evt.syscall in ("mkdir", "mkdirat"):
            if rel not in files:
                files[rel] = FileState(bytearray(), True)

        elif evt.syscall in ("link", "linkat"):
            if not evt.path2:
                return
            rel2 = self._rel(evt.path2)
            if rel in files and files[rel].exists:
                # Hard link: same inode, same content
                files[rel2] = FileState(bytearray(files[rel].content), True)

        elif evt.syscall in ("symlink", "symlinkat"):
            if not evt.path2:
                return
            rel2 = self._rel(evt.path2)
            if rel2 not in files:
                # Symlink: store target path as file content
                files[rel2] = FileState(
                    bytearray(evt.path.encode("utf-8", errors="replace")), True)

    def simulate(self, events: List[SyscallEvent],
                 bound: int = 2) -> List[Dict]:
        sites: List[Dict] = []
        files = self._clone()
        # (event_idx, state_before_write)
        pending: List[Tuple[int, Dict[str, FileState]]] = []

        def add(snap, desc, after, ctype):
            sites.append({
                "snapshot": snap,
                "description": desc,
                "after_event": after,
                "crash_type": ctype,
            })

        add(self._snap(files), "Initial state (before any syscall)", -1, "initial")

        for i, evt in enumerate(events):
            if evt.is_barrier:
                pending.clear()
                self._apply(files, evt)
                add(self._snap(files),
                    f"Barrier: {evt.syscall}({os.path.basename(evt.path or '')})",
                    i, "barrier")
                continue

            state_before = self._copy(files)
            if evt.is_write_data:
                pending.append((i, state_before))

            self._apply(files, evt)

            # ES: expected snapshot after metadata ops
            if evt.is_metadata:
                add(self._snap(files),
                    f"After: {evt.syscall}({os.path.basename(evt.path or '')})",
                    i, "metadata")

            # ── Crash site: partial writes ──
            for dc in range(1, min(bound + 1, len(pending) + 1)):
                _, base = pending[-dc]
                cf = self._copy(base)
                dropped = set(pw[0] for pw in pending[-dc:])
                for j in range(pending[-dc][0], i + 1):
                    self._apply(cf, events[j],
                                "partial" if j in dropped else "normal")
                add(self._snap(cf),
                    f"Partial: {evt.syscall} done, {dc} write(s) partially dropped",
                    i, "partial_write")

            # ── Crash site: empty writes (data lost, file extended with zeros) ──
            for dc in range(1, min(bound + 1, len(pending) + 1)):
                _, base = pending[-dc]
                cf = self._copy(base)
                dropped = set(pw[0] for pw in pending[-dc:])
                for j in range(pending[-dc][0], i + 1):
                    self._apply(cf, events[j],
                                "empty" if j in dropped else "normal")
                add(self._snap(cf),
                    f"Empty: {evt.syscall} done, {dc} write(s) returned but data=0x00",
                    i, "empty_write")

            # ── Crash site: drop ALL pending writes, keep metadata ──
            # (metadata-data reordering: metadata takes effect, data writes lost)
            if pending:
                _, base = pending[0]
                cf = self._copy(base)
                write_set = set(pw[0] for pw in pending)
                for j in range(pending[0][0], i + 1):
                    if j not in write_set:
                        self._apply(cf, events[j])
                add(self._snap(cf),
                    f"Reorder: {evt.syscall} applied, {len(pending)} earlier write(s) lost",
                    i, "metadata_reorder")

            # ── Crash site: writes persisted, but subsequent metadata LOST ──
            # (reverse reordering: data on disk but metadata like rename/unlink not)
            # This captures: write completed but rename didn't happen,
            # so file content is at the OLD path, not the new one.
            if evt.is_metadata:
                # State = all writes applied up to now, but THIS metadata op dropped
                cf = self._copy(state_before)  # state before this metadata op
                # Don't apply this event — metadata is lost
                add(self._snap(cf),
                    f"Lost metadata: {evt.syscall} NOT applied (data persisted)",
                    i, "lost_metadata")

        add(self._snap(files), "Final state (normal completion)",
            len(events) - 1 if events else -1, "final")

        return sites


def dedup(sites: List[Dict]) -> List[Dict]:
    seen: Set[str] = set()
    out = []
    for s in sites:
        h = hashlib.sha256()
        for p in sorted(s["snapshot"]):
            h.update(p.encode())
            h.update(s["snapshot"][p].encode())
        k = h.hexdigest()
        if k not in seen:
            seen.add(k)
            out.append(s)
    return out


# ─── Main ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="cc-check: Crash Consistency Checker (simplified C³)",
        epilog="Example: python3 cc-check.py --workdir /tmp/test -- cp src.txt dst.txt",
    )
    parser.add_argument("--workdir", default=".",
                        help="Directory to track files in (default: .)")
    parser.add_argument("--bound", type=int, default=2,
                        help="Search bound for crash generation (default: 2)")
    parser.add_argument("--strace-log", default=None,
                        help="Reuse existing strace log (skip execution)")
    parser.add_argument("cmd", nargs=argparse.REMAINDER,
                        help="Command (use -- before command)")
    args = parser.parse_args()

    cmd = args.cmd
    if cmd and cmd[0] == "--":
        cmd = cmd[1:]
    if not cmd and not args.strace_log:
        parser.error("No command. Usage: cc-check.py [--workdir DIR] -- <cmd> [args...]")

    workdir = os.path.abspath(args.workdir)
    if not os.path.isdir(workdir):
        log(f"ERROR: workdir does not exist: {workdir}")
        sys.exit(1)

    # 1. Initial snapshot
    log("Taking initial snapshot...")
    initial_snap = take_snapshot(workdir)

    # 2. Run strace or reuse log
    tmpdir = None
    if args.strace_log:
        strace_log = args.strace_log
    else:
        log(f"Running: {' '.join(cmd)}")
        tmpdir = tempfile.mkdtemp(prefix="cc-check-")
        strace_log = os.path.join(tmpdir, "strace.log")
        strace_cmd = [
            "strace", "-f",
            "-e", "trace=" + TRACE_SYSCALLS,
            "-e", "signal=none",
            "-y", "-xx", "-s", "4096",
            "-o", strace_log,
        ] + cmd
        try:
            proc = subprocess.run(strace_cmd, cwd=workdir,
                                  capture_output=True, text=True)
            log(f"Exit code: {proc.returncode}")
            if proc.returncode != 0:
                log(f"WARNING: strace exited with code {proc.returncode}")
        except FileNotFoundError:
            log("ERROR: strace not found. Install strace and try again.")
            sys.exit(1)

    # 3. Parse
    log("Parsing strace log...")
    events, touched = parse_strace_log(strace_log, workdir)
    log(f"{len(events)} events, {len(touched)} files touched")

    # 4. Final snapshot
    log("Taking final snapshot...")
    final_snap = take_snapshot(workdir)

    # 5. Simulate
    log(f"Simulating crashes (bound={args.bound})...")
    sim = CrashSimulator(initial_snap, workdir)
    sites = sim.simulate(events, bound=args.bound)
    sites = dedup(sites)
    log(f"{len(sites)} unique crash sites")

    # 6. Build compact trace
    trace = []
    for evt in events:
        d_b64 = ""
        if evt.data:
            d_b64 = base64.b64encode(evt.data).decode()
            if len(d_b64) > 2048:
                d_b64 = d_b64[:2048]  # truncated; see data_len for actual size
        trace.append({
            "i": evt.index,
            "op": evt.syscall,
            "path": evt.path,
            "path2": evt.path2,
            "ret": evt.result,
            "off": evt.offset,
            "data_len": len(evt.data),
            "data": d_b64,
            "truncated": evt.data_truncated,
            "meta": evt.is_metadata,
            "barrier": evt.is_barrier,
            "write": evt.is_write_data,
        })

    # 7. Build crash sites with compact snapshot representation
    crash_sites_out = []
    for s in sites:
        snap = s["snapshot"]
        crash_sites_out.append({
            "description": s["description"],
            "after_event": s["after_event"],
            "crash_type": s["crash_type"],
            "files": snapshot_summary(snap),
            "diff_from_initial": snapshot_diff(initial_snap, snap),
            "snapshot": snap,
        })

    # 8. Output JSON to stdout
    output = {
        "version": 1,
        "command": cmd,
        "workdir": workdir,
        "bound": args.bound,
        "touched_files": sorted(touched),
        "initial_snapshot": initial_snap,
        "final_snapshot": final_snap,
        "final_diff": snapshot_diff(initial_snap, final_snap),
        "trace": trace,
        "crash_sites": crash_sites_out,
    }
    json.dump(output, sys.stdout, ensure_ascii=False, separators=(",", ":"))
    log("Done.")

    # Clean up temp directory
    if tmpdir and os.path.isdir(tmpdir):
        shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    main()
