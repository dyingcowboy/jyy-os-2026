#!/bin/bash
# ILP benchmark — build, run each variant under perf, extract IPC.
set -e
cd "$(dirname "$0")"

CFLAGS="-O2"
gcc $CFLAGS -o ilp_bench ilp_bench.c

if ! command -v perf &>/dev/null; then
    echo "ERROR: 'perf' not found. Install linux-tools or run the binary directly:"
    echo "  ./ilp_bench <dep|ind|fp|neon|mix|imul>"
    exit 1
fi

printf "\n%-8s %8s %15s %15s\n" "variant" "IPC" "instructions" "cycles"
printf "%-8s %8s %15s %15s\n" "-------" "---" "------------" "------"

for v in dep ind fp neon mix imul; do
    out=$(perf stat -e cycles,instructions ./ilp_bench "$v" 2>&1)
    cyc=$(echo "$out" | grep -v stalled | grep -i 'cycle'  | awk '{print $1}' | tr -d ',.')
    ins=$(echo "$out" | grep -v stalled | grep -i 'instruc' | awk '{print $1}' | tr -d ',.')
    if [ -z "$cyc" ] || [ -z "$ins" ] || [ "$cyc" -eq 0 ] 2>/dev/null; then
        ipc="N/A"
    else
        ipc=$(awk "BEGIN{printf \"%.2f\", $ins/$cyc}")
    fi
    printf "%-8s %8s %15s %15s\n" "$v" "$ipc" "$ins" "$cyc"
done
