#!/usr/bin/env python3
"""Measure per-thread resource cost by comparing before/after ./sleep N."""

import os
import sys
import json
import subprocess
import resource
import time
import statistics
SLEEP_BIN = "./sleep"
THREAD_COUNT = 1000
SAMPLE_COUNT = 3               # multiple samples for noise reduction
SETTLE_SEC = 0.3               # settle time before each sample


def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except OSError:
        return ""


def parse_kv(text):
    """Parse 'Key:  value kB' style entries."""
    d = {}
    for line in text.strip().splitlines():
        parts = line.split(":")
        if len(parts) == 2:
            k = parts[0].strip()
            v = parts[1].strip().split()[0]
            try:
                d[k] = int(v)
            except ValueError:
                d[k] = v
    return d


def get_meminfo():
    return parse_kv(read_file("/proc/meminfo"))


def get_system_threads():
    """Count total threads on system via /proc."""
    count = 0
    for pid in os.listdir("/proc"):
        if pid.isdigit():
            task_dir = f"/proc/{pid}/task"
            try:
                count += len(os.listdir(task_dir))
            except OSError:
                pass
    return count


def get_pid_status(pid):
    return parse_kv(read_file(f"/proc/{pid}/status"))


def get_pid_stat(pid):
    raw = read_file(f"/proc/{pid}/stat")
    if not raw:
        return {}
    # Field names from man proc_pid_stat
    fields = [
        "pid", "comm", "state", "ppid", "pgrp", "session",
        "tty_nr", "tpgid", "flags", "minflt", "cminflt",
        "majflt", "cmajflt", "utime", "stime", "cutime",
        "cstime", "priority", "nice", "num_threads",
        "itrealvalue", "starttime", "vsize", "rss",
    ]
    parts = raw.split()
    # comm may contain spaces and parens, find last ')'
    comm_end = raw.rfind(")")
    if comm_end >= 0:
        rest = raw[comm_end + 1:].split()
        vals = [parts[0], raw[1:comm_end]] + rest
    else:
        vals = parts
    return {fields[i]: vals[i] for i in range(min(len(fields), len(vals)))}


def get_pid_smaps_rollup(pid):
    text = read_file(f"/proc/{pid}/smaps_rollup")
    return parse_kv(text)


def get_pid_fd_count(pid):
    try:
        return len(os.listdir(f"/proc/{pid}/fd"))
    except OSError:
        return 0


def get_pid_oom_score(pid):
    v = read_file(f"/proc/{pid}/oom_score").strip()
    return int(v) if v else -1


def get_mapped_regions(pid):
    """Count mapped memory regions."""
    text = read_file(f"/proc/{pid}/maps")
    return len(text.strip().splitlines()) if text.strip() else 0


def get_sysinfo():
    raw = read_file("/proc/sys/kernel/threads-max")
    threads_max = int(raw.strip()) if raw.strip() else -1
    raw2 = read_file("/proc/sys/kernel/pid_max")
    pid_max = int(raw2.strip()) if raw2.strip() else -1
    raw3 = read_file("/proc/loadavg")
    load = raw3.strip().split() if raw3.strip() else []
    return {
        "kernel_threads_max": threads_max,
        "pid_max": pid_max,
        "loadavg_1m": load[0] if load else "?",
        "loadavg_5m": load[1] if len(load) > 1 else "?",
    }


def get_page_size():
    try:
        return os.sysconf("SC_PAGESIZE")
    except (ValueError, OSError):
        return 4096


def get_rusage_self():
    u = resource.getrusage(resource.RUSAGE_SELF)
    return {
        "maxrss_kb": u.ru_maxrss,
        "minflt": u.ru_minflt,
        "majflt": u.ru_majflt,
        "nvcsw": u.ru_nvcsw,
        "nivcsw": u.ru_nivcsw,
    }


def collect(pid=None):
    """Collect all resource metrics. pid=None means system-level only."""
    page_kb = get_page_size() // 1024
    data = {
        "timestamp": time.time(),
        "meminfo": get_meminfo(),
        "sysinfo": get_sysinfo(),
        "system_total_threads": get_system_threads(),
        "rusage_self": get_rusage_self(),
        "page_size_kb": page_kb,
    }

    if pid is not None:
        status = get_pid_status(pid)
        stat = get_pid_stat(pid)
        smaps = get_pid_smaps_rollup(pid)
        data["process"] = {
            "pid": pid,
            "status": status,
            "stat": stat,
            "smaps_rollup": smaps,
            "fd_count": get_pid_fd_count(pid),
            "mapped_regions": get_mapped_regions(pid),
            "oom_score": get_pid_oom_score(pid),
            "VmSize_kb": status.get("VmSize", 0),
            "VmRSS_kb": status.get("VmRSS", 0),
            "VmStk_kb": status.get("VmStk", 0),
            "VmData_kb": status.get("VmData", 0),
            "VmPTE_kb": status.get("VmPTE", 0),
            "Threads": status.get("Threads", 0),
            "voluntary_ctxt_switches": status.get("voluntary_ctxt_switches", 0),
            "nonvoluntary_ctxt_switches": status.get("nonvoluntary_ctxt_switches", 0),
        }
    return data


def delta(after, before, key):
    a = after.get(key, 0)
    b = before.get(key, 0)
    return (a - b) if isinstance(a, (int, float)) and isinstance(b, (int, float)) else None


def print_diff(before, after, n):
    print(f"\n{'='*60}")
    print(f"  Per-Thread Resource Cost  (N = {n} threads)")
    print(f"{'='*60}\n")

    # System memory delta (noisy — kernel cache reclamation dominates)
    mem_b = before["meminfo"]
    mem_a = after["meminfo"]
    memavail_delta = delta(mem_a, mem_b, "MemAvailable")
    memfree_delta = delta(mem_a, mem_b, "MemFree")
    slab_delta = delta(mem_a, mem_b, "Slab")
    kernelstack_delta = delta(mem_a, mem_b, "KernelStack")
    pagetables_delta = delta(mem_a, mem_b, "PageTables")

    print("── System-wide Memory (/proc/meminfo)  [⚠  noisy, may be -ve] ──")
    for name, val in [
        ("MemAvailable", memavail_delta),
        ("MemFree", memfree_delta),
        ("Slab", slab_delta),
        ("KernelStack", kernelstack_delta),
        ("PageTables", pagetables_delta),
    ]:
        if val is not None:
            per = val / n
            print(f"  {name:20s}  total: {val:>+10d} KB    per-thread: {per:>+10.1f} KB")
    print()

    # System thread count delta
    sys_threads_delta = delta(after, before, "system_total_threads")
    print("── System Threads ──")
    print(f"  total increase: {sys_threads_delta}")
    print()

    # Process-level
    proc_b = before.get("process", {})
    proc_a = after.get("process", {})
    print("── Process-Level (/proc/<pid>/status) ──")
    for name in ["VmSize", "VmRSS", "VmStk", "VmData", "VmPTE", "VmSwap"]:
        kb_b = proc_b.get(f"{name}_kb", proc_b.get(name, 0))
        kb_a = proc_a.get(f"{name}_kb", proc_a.get(name, 0))
        if isinstance(kb_b, (int, float)) and isinstance(kb_a, (int, float)):
            d = kb_a - kb_b
            per = d / n
            print(f"  {name:20s}  total: {d:>10d} KB    per-thread: {per:>10.1f} KB")

    threads_b = proc_b.get("Threads", 0)
    threads_a = proc_a.get("Threads", 0)
    print(f"  {'Threads':20s}  total: {threads_a - threads_b:>10d}          (expected {n})")

    mapped_b = proc_b.get("mapped_regions", 0)
    mapped_a = proc_a.get("mapped_regions", 0)
    print(f"  {'mapped_regions':20s}  total: {mapped_a - mapped_b:>10d}      per-thread: {(mapped_a - mapped_b)/n:>10.1f}")

    fd_b = proc_b.get("fd_count", 0)
    fd_a = proc_a.get("fd_count", 0)
    print(f"  {'fd_count':20s}  total: {fd_a - fd_b:>10d}      per-thread: {(fd_a - fd_b)/n:>10.1f}")
    print()

    # smaps_rollup delta
    smaps_b = proc_b.get("smaps_rollup", {})
    smaps_a = proc_a.get("smaps_rollup", {})
    print("── smaps_rollup ──")
    for name in ["Rss", "Pss", "Private_Clean", "Private_Dirty", "Referenced", "Anonymous",
                  "LazyFree", "AnonHugePages", "ShmemPmdMapped", "FilePmdMapped",
                  "Shared_Hugetlb", "Private_Hugetlb"]:
        val_b = smaps_b.get(name, 0)
        val_a = smaps_a.get(name, 0)
        if isinstance(val_b, (int, float)) and isinstance(val_a, (int, float)):
            d = val_a - val_b
            if d != 0:
                per = d / n
                print(f"  {name:20s}  total: {d:>10d} KB    per-thread: {per:>10.1f} KB")
    print()

    # Context switches
    vcsw_b = proc_b.get("voluntary_ctxt_switches", 0)
    vcsw_a = proc_a.get("voluntary_ctxt_switches", 0)
    nvcsw_b = proc_b.get("nonvoluntary_ctxt_switches", 0)
    nvcsw_a = proc_a.get("nonvoluntary_ctxt_switches", 0)
    print("── Context Switches ──")
    print(f"  voluntary:       {vcsw_a - vcsw_b}")
    print(f"  nonvoluntary:    {nvcsw_a - nvcsw_b}")
    print()

    # loadavg
    print("── Load Average ──")
    print(f"  before: {' '.join(str(before['sysinfo'][k]) for k in ['loadavg_1m', 'loadavg_5m'])}")
    print(f"  after:  {' '.join(str(after['sysinfo'][k]) for k in ['loadavg_1m', 'loadavg_5m'])}")
    print()

    # Use process-level metrics for summary (far less noisy than system MemAvailable)
    vm_rss_delta = (proc_a.get("VmRSS_kb", 0) if isinstance(proc_a.get("VmRSS_kb"), (int, float)) else 0) - \
                   (proc_b.get("VmRSS_kb", 0) if isinstance(proc_b.get("VmRSS_kb"), (int, float)) else 0)
    smaps_rss_b = smaps_b.get("Rss", 0)
    smaps_rss_a = smaps_a.get("Rss", 0)
    smaps_rss_delta = (smaps_rss_a - smaps_rss_b) if isinstance(smaps_rss_a, (int, float)) and isinstance(smaps_rss_b, (int, float)) else 0

    print(f"{'='*60}")
    print(f"  SUMMARY")
    print(f"    VmRSS delta:   {vm_rss_delta:>+d} KB  =>  {vm_rss_delta/n:>+.1f} KB/thread")
    print(f"    smaps Rss:     {smaps_rss_delta:>+d} KB  =>  {smaps_rss_delta/n:>+.1f} KB/thread")
    print(f"    (system MemAvailable delta: {memavail_delta or 0:>+d} KB — noisy, skip)")
    print(f"{'='*60}")


def sample_collect(pid=None, rounds=SAMPLE_COUNT):
    """Collect multiple snapshots and return the median for each metric
    to suppress transient noise."""
    if rounds <= 1:
        return collect(pid=pid)

    samples = []
    for _ in range(rounds):
        time.sleep(SETTLE_SEC)
        samples.append(collect(pid=pid))

    # Deep-merge: for each key, take median of numeric values,
    # and median of each sub-dict's keys.
    return _merge_samples(samples)


def _merge_samples(samples):
    """Merge a list of collect() dicts by taking medians of numeric leaves."""
    merged = {}
    for key in samples[0]:
        vals = [s[key] for s in samples]
        if all(isinstance(v, dict) for v in vals):
            # Recurse into sub-dicts only if all keys match
            all_keys = set()
            for v in vals:
                all_keys.update(v.keys())
            sub = {}
            for k in all_keys:
                sub_vals = [v.get(k, 0) for v in vals]
                if all(isinstance(x, (int, float)) for x in sub_vals):
                    sub[k] = int(statistics.median(sub_vals))
                elif all(isinstance(x, str) for x in sub_vals):
                    sub[k] = vals[0].get(k, "")  # strings: take first
                else:
                    sub[k] = vals[0].get(k, 0)
            merged[key] = sub
        elif all(isinstance(v, (int, float)) for v in vals):
            merged[key] = int(statistics.median(vals))
        else:
            merged[key] = vals[0]  # non-numeric: keep first
    return merged


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else THREAD_COUNT

    print(f"[*] Stabilizing system for {SETTLE_SEC*2:.1f}s...")
    time.sleep(SETTLE_SEC * 2)

    print(f"[*] Collecting baseline ({SAMPLE_COUNT} samples, system-level)...")
    before = sample_collect()

    print(f"[*] Launching: {SLEEP_BIN} {n}")
    proc = subprocess.Popen([SLEEP_BIN, str(n)])
    pid = proc.pid
    print(f"    PID = {pid}")

    # Wait for all threads to spawn; 1000 threads may need >0.5s
    print(f"[*] Waiting for threads to spawn...")
    for _ in range(10):
        time.sleep(0.3)
        st = get_pid_status(pid)
        cur = st.get("Threads", 0)
        if isinstance(cur, int) and cur >= n:
            break
        print(f"    threads so far: {cur}/{n}")

    actual_threads = get_pid_status(pid).get("Threads", "?")
    print(f"    Threads reported: {actual_threads} (target {n})")

    print(f"[*] Collecting after-snapshot ({SAMPLE_COUNT} samples, pid={pid})...")
    after = sample_collect(pid=pid, rounds=SAMPLE_COUNT)

    print_diff(before, after, n)

    # Dump raw data for further analysis
    dump_path = f"/tmp/thread-cost-{pid}.json"
    with open(dump_path, "w") as f:
        json.dump({"before": before, "after": after, "thread_count": n}, f, indent=2)
    print(f"\n[*] Raw data dumped to {dump_path}")

    print(f"[*] Terminating sleep process (SIGTERM)...")
    proc.terminate()
    proc.wait()
    print("[*] Done.")


if __name__ == "__main__":
    main()
