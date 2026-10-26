#!/usr/bin/env python3
"""
dumpext4.py - Visualize ext4 filesystem internals using debugfs.

Usage: python3 dumpext4.py /path/to/dir > output.html

Finds the ext4 device backing the given directory, uses debugfs to probe
inode structures, directory entries, and block allocations, then renders
an HTML page with an embedded SVG graph.

Requires (Linux): debugfs (e2fsprogs), graphviz (dot)
May need: sudo for block device read access
"""

import os
import re
import subprocess
import sys


# ── helpers ─────────────────────────────────────────────────────────────

def fmt_size(n):
    if n < 1024:
        return f"{n} B"
    for unit in ("KiB", "MiB", "GiB", "TiB"):
        n /= 1024
        if n < 1024:
            return f"{n:.1f} {unit}"
    return f"{n:.1f} PiB"


def html_escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def dot_escape(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


# ── find ext4 device ────────────────────────────────────────────────────

def find_device(path):
    """Return (device_path, mount_point) for the filesystem containing path."""
    abspath = os.path.realpath(path)

    # Try findmnt
    try:
        r = subprocess.run(
            ["findmnt", "-n", "-o", "SOURCE,TARGET", "--target", abspath],
            capture_output=True, text=True,
        )
        if r.returncode == 0 and r.stdout.strip():
            parts = r.stdout.strip().split(None, 1)
            if len(parts) == 2:
                return parts[0], parts[1]
    except FileNotFoundError:
        pass

    # Fallback: parse /proc/mounts
    try:
        with open("/proc/mounts") as f:
            best = None
            for line in f:
                parts = line.split()
                if len(parts) < 2:
                    continue
                dev, mnt = parts[0], parts[1]
                if abspath == mnt or abspath.startswith(mnt + "/"):
                    if best is None or len(mnt) > len(best[1]):
                        best = (dev, mnt)
            if best:
                return best
    except FileNotFoundError:
        pass

    raise RuntimeError(f"Cannot determine device for {abspath}")


# ── debugfs wrapper ─────────────────────────────────────────────────────

class DebugFS:
    def __init__(self, device):
        self.device = device
        try:
            r = subprocess.run(
                ["debugfs", "-c", "-R", "show_super_stats", device],
                capture_output=True, text=True, timeout=10,
            )
        except FileNotFoundError:
            print("Error: debugfs not found. Install e2fsprogs.", file=sys.stderr)
            sys.exit(1)

        if r.returncode != 0:
            combined = (r.stderr + r.stdout).lower()
            perm_indicators = [
                "permission denied",
                "operation not permitted",
                "requires root",
                "superuser",
                "no read access",
            ]
            if any(indicator in combined for indicator in perm_indicators):
                print(f"Error: debugfs requires root privileges to read {device}",
                      file=sys.stderr)
                print("Try: sudo python3 dumpext4.py ...", file=sys.stderr)
            else:
                print(f"Error: debugfs failed on {device}: {r.stderr.strip()}",
                      file=sys.stderr)
            sys.exit(1)

    def _run(self, cmd):
        r = subprocess.run(
            ["debugfs", "-c", "-R", cmd, self.device],
            capture_output=True, text=True, timeout=30,
        )
        if r.returncode != 0:
            combined = (r.stderr + r.stdout).lower()
            if "permission denied" in combined:
                print(f"debugfs error ({cmd}): permission denied — "
                      f"re-run with sudo", file=sys.stderr)
                sys.exit(1)
            print(f"debugfs error ({cmd}): {r.stderr.strip()}", file=sys.stderr)
        return r.stdout

    def ls(self, path):
        """List directory. Returns [(name, inode), ...].

        debugfs ls output uses multiple spaces between entries, e.g.:
          12  (12) .    34  (24) file.txt
        We locate each entry by the "inode (rec_len) " header pattern.
        """
        out = self._run(f"ls {path}")
        entries = []
        entry_start = re.compile(r"(\d+)\s+\(\d+\)\s+")
        matches = list(entry_start.finditer(out))
        for i, m in enumerate(matches):
            ino = int(m.group(1))
            name_start = m.end()
            name_end = matches[i + 1].start() if i + 1 < len(matches) else len(out)
            name = out[name_start:name_end].strip()
            entries.append((name, ino))
        return entries

    def stat(self, ino):
        """Get inode details via debugfs stat <ino>."""
        out = self._run(f"stat <{ino}>")
        info = {
            "ino": ino, "type": "unknown", "mode": 0,
            "size": 0, "nlinks": 0, "blocks": [],
        }

        lines = out.splitlines()
        for i, line in enumerate(lines):
            line = line.strip()

            # First line: Inode: N  Type: xxx  Mode: NNNN  Flags: ...
            if "Type:" in line:
                if "regular" in line:        info["type"] = "file"
                elif "directory" in line:    info["type"] = "dir"
                elif "symbolic" in line or "symlink" in line:     info["type"] = "symlink"
                elif "character" in line:    info["type"] = "chardev"
                elif "block device" in line: info["type"] = "blockdev"
                elif "FIFO" in line:         info["type"] = "fifo"

            # Mode (on the first line)
            m = re.search(r"Mode:\s+(\d+)", line)
            if m:
                info["mode"] = int(m.group(1), 8)

            # Size — only match the User/Group/Size line, not
            # "Fragment: ... Size: 0" which comes later.
            m = re.search(r"User:.*\bSize:\s+(\d+)", line)
            if m:
                info["size"] = int(m.group(1))

            # Links
            m = re.search(r"\bLinks:\s+(\d+)", line)
            if m:
                info["nlinks"] = int(m.group(1))

            # Fast symlink target (inline, <= 60 bytes, stored in i_block[])
            m = re.search(r'Fast link dest:\s*"(.*)"', line)
            if m:
                info["target"] = m.group(1)
                info["sym_storage"] = "inline"

            # BLOCKS / EXTENTS — may continue on next lines
            if line.startswith("BLOCKS:") or line.startswith("EXTENTS:"):
                rest = line.split(":", 1)[1].strip()
                j = i + 1
                while j < len(lines) and lines[j].strip().startswith("("):
                    rest += " " + lines[j].strip()
                    j += 1
                info["blocks"] = self._parse_blocks(rest)
                break

        # Symlink: detect inline vs block storage.
        # Short symlinks (<=60 bytes) store the target inline in i_block[];
        # debugfs stat shows it as "Fast link dest: \"...\"".
        # Longer symlinks use a full data block — target must be read from there.
        if info["type"] == "symlink":
            info.setdefault("target", None)
            info.setdefault("sym_storage", "block" if info["blocks"] else "unknown")

        return info

    @staticmethod
    def _parse_blocks(s):
        """Parse BLOCKS/EXTENTS into [(start_phys, end_phys), ...]."""
        ranges = []
        s = s.strip()
        if not s or s == "(none)":
            return ranges
        for part in s.split(","):
            part = part.strip()
            m = re.match(r"\(.*?\):\s*(.*)", part)
            rng = m.group(1).strip() if m else part
            if "-" in rng:
                a, b = rng.split("-", 1)
                ranges.append((int(a), int(b)))
            elif rng.isdigit():
                n = int(rng)
                ranges.append((n, n))
        return ranges


# ── scanning ─────────────────────────────────────────────────────────────

def scan_tree(dfs, root_path, max_depth=10):
    tree = {}
    visited = set()
    _scan(dfs, root_path, tree, visited, 0, max_depth)
    return tree


def _scan(dfs, path, tree, visited, depth, max_depth):
    for name, ino in dfs.ls(path):
        if name in (".", ".."):
            continue
        info = dfs.stat(ino)
        node = {
            "ino": ino,
            "type": info["type"],
            "mode": info["mode"],
            "size": info["size"],
            "nlinks": info["nlinks"],
            "blocks": info["blocks"],
        }
        if info["type"] == "dir" and ino not in visited and depth < max_depth:
            visited.add(ino)
            child_path = f"{path.rstrip('/')}/{name}"
            node["children"] = {}
            _scan(dfs, child_path, node["children"], visited, depth + 1, max_depth)
        elif info["type"] == "symlink":
            node["target"] = info.get("target")
            node["sym_storage"] = info.get("sym_storage", "unknown")
        tree[name] = node


# ── DOT generation ─────────────────────────────────────────────────────

_COLORS = {
    "dir": "#0969da", "file": "#1a7f37", "symlink": "#9a6700",
    "chardev": "#8250df", "blockdev": "#8250df",
    "fifo": "#656d76", "socket": "#cf222e", "unknown": "#656d76",
}

_TYPE_TAG = {
    "dir": "DIR", "file": "FILE", "symlink": "LINK",
    "chardev": "CHR", "blockdev": "BLK", "fifo": "FIFO",
    "socket": "SOCK", "unknown": "???",
}


def _fmt_blocks(ranges):
    if not ranges:
        return ""
    total = sum(b - a + 1 for a, b in ranges)
    parts = [str(a) if a == b else f"{a}-{b}" for a, b in ranges]
    return f"{total} blk: {', '.join(parts)}"


def _node_html(name, node):
    bg = _COLORS.get(node["type"], "#6e7681")
    tag = _TYPE_TAG.get(node["type"], "???")

    rows = [
        f'<TR><TD BGCOLOR="{bg}"><FONT COLOR="white">'
        f'ino #{node["ino"]}  {tag}</FONT></TD></TR>',
        f'<TR><TD>{html_escape(name)}</TD></TR>',
        f'<TR><TD><FONT POINT-SIZE="8">'
        f'{node["mode"]:04o}  {fmt_size(node["size"])}</FONT></TD></TR>',
    ]
    blk = _fmt_blocks(node.get("blocks", []))
    if blk:
        rows.append(
            f'<TR><TD><FONT POINT-SIZE="8" COLOR="#0550ae">'
            f'{html_escape(blk)}</FONT></TD></TR>'
        )
    if node["type"] == "symlink":
        storage = node.get("sym_storage", "unknown")
        storage_label = {
            "inline": "inline (in i_block[])",
            "block": "data block",
        }.get(storage, storage)
        if node.get("target"):
            rows.append(
                f'<TR><TD><FONT POINT-SIZE="8" COLOR="#9a6700">'
                f'&#8594; {html_escape(node["target"])}</FONT></TD></TR>'
            )
        rows.append(
            f'<TR><TD><FONT POINT-SIZE="8" COLOR="#656d76">'
            f'storage: {html_escape(storage_label)}</FONT></TD></TR>'
        )
    if node["nlinks"] > 1:
        rows.append(
            f'<TR><TD><FONT POINT-SIZE="8">nlink={node["nlinks"]}'
            f'</FONT></TD></TR>'
        )
    return (
        '<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4"'
        f' BGCOLOR="#ffffff" COLOR="#d0d7de">{"".join(rows)}</TABLE>'
    )


def tree_to_dot(tree, root_name, root_info):
    lines = [
        "digraph fs {",
        '  graph [rankdir=TB, bgcolor="#ffffff"];',
        '  node [shape=plaintext, fontname="monospace", fontsize=10];',
        '  edge [fontsize=9, color="#d0d7de", fontcolor="#656d76"];',
    ]
    root_id = f"ino_{root_info['ino']}"
    lines.append(f'  "{root_id}" [label=<{_node_html(root_name, root_info)}>];')
    _dot_add(tree, root_id, lines, {root_info["ino"]})
    lines.append("}")
    return "\n".join(lines)


def _dot_add(tree, parent_id, lines, drawn):
    for name, node in tree.items():
        ino = node["ino"]
        nid = f"ino_{ino}"
        if ino in drawn:
            lines.append(
                f'  "{parent_id}" -> "{nid}"'
                f' [label="{dot_escape(name)}"];'
            )
            continue
        drawn.add(ino)
        lines.append(f'  "{nid}" [label=<{_node_html(name, node)}>];')
        lines.append(
            f'  "{parent_id}" -> "{nid}"'
            f' [label="{dot_escape(name)}"];'
        )
        if node["type"] == "dir" and "children" in node:
            _dot_add(node["children"], nid, lines, drawn)


# ── HTML output ─────────────────────────────────────────────────────────

def _summary(tree):
    counts = {"dir": 0, "file": 0, "symlink": 0, "other": 0}

    def walk(t):
        for n in t.values():
            k = n["type"] if n["type"] in counts else "other"
            counts[k] += 1
            if "children" in n:
                walk(n["children"])

    walk(tree)
    parts = []
    if counts["dir"]:     parts.append(f"{counts['dir']} dirs")
    if counts["file"]:    parts.append(f"{counts['file']} files")
    if counts["symlink"]: parts.append(f"{counts['symlink']} symlinks")
    if counts["other"]:   parts.append(f"{counts['other']} other")
    return ", ".join(parts) or "empty"


def make_html(svg, title, summary):
    return (
        "<!DOCTYPE html>\n"
        '<html lang="en"><head><meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1.0">\n'
        f"<title>{html_escape(title)}</title>\n"
        "<style>\n"
        "* { margin:0; box-sizing:border-box; }\n"
        "body { font-family:-apple-system,sans-serif;"
        " background:#ffffff; color:#24292f; }\n"
        ".hdr { padding:12px 20px; border-bottom:1px solid #d0d7de; }\n"
        ".hdr h1 { font-size:14px; color:#0969da; }\n"
        ".hdr p  { font-size:12px; color:#656d76; margin-top:2px; }\n"
        "#graph { padding:12px; overflow:auto; }\n"
        "#graph svg { max-width:100%; height:auto; }\n"
        "</style>\n"
        "</head><body>\n"
        f'<div class="hdr"><h1>{html_escape(title)}</h1>'
        f"<p>{summary}</p></div>\n"
        f'<div id="graph">{svg}</div>\n'
        "</body></html>"
    )


# ── main ────────────────────────────────────────────────────────────────

def main():
    import argparse

    p = argparse.ArgumentParser(
        description="Visualize ext4 filesystem internals using debugfs",
    )
    p.add_argument("directory", help="directory to visualize")
    p.add_argument("--max-depth", type=int, default=10)
    args = p.parse_args()

    abspath = os.path.realpath(args.directory)
    if not os.path.isdir(abspath):
        print(f"Error: {abspath} is not a directory", file=sys.stderr)
        sys.exit(1)

    device, mount = find_device(abspath)
    rel_path = "/" + os.path.relpath(abspath, mount)
    print(f"Device: {device}", file=sys.stderr)
    print(f"Mount:  {mount}", file=sys.stderr)
    print(f"Path:   {rel_path}", file=sys.stderr)

    dfs = DebugFS(device)

    root_ino = os.stat(abspath).st_ino
    root_info = dfs.stat(root_ino)
    root_info["ino"] = root_ino
    root_name = os.path.basename(abspath) or mount

    print(f"Scanning {rel_path} ...", file=sys.stderr)
    tree = scan_tree(dfs, rel_path, args.max_depth)
    summary = _summary(tree)
    print(f"Done: {summary}", file=sys.stderr)

    dot = tree_to_dot(tree, root_name, root_info)

    r = subprocess.run(
        ["dot", "-Tsvg"], input=dot, capture_output=True,
        text=True, timeout=30,
    )
    if r.returncode != 0:
        print(f"Error: dot failed: {r.stderr}", file=sys.stderr)
        sys.exit(1)

    title = f"ext4: {device} {rel_path}"
    print(make_html(r.stdout, title, f"{summary} | {device}"))


if __name__ == "__main__":
    main()
