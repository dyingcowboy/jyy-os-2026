#!/bin/bash
set -e

BINARIES="spin mutex atomic trap"
THREADS="1 2 4 8 16"
REPEAT=5
TOTAL_OPS=10000000

CSV="results.csv"
echo "impl,T,trial,ns_per_op" > $CSV

for bin in $BINARIES; do
    for T in $THREADS; do
        for trial in $(seq 1 $REPEAT); do
            t0=$(date +%s%N)
            ./$bin $T > /dev/null
            t1=$(date +%s%N)
            elapsed_ns=$((t1 - t0))
            ns_per_op=$(echo "scale=2; $elapsed_ns / $TOTAL_OPS" | bc)
            echo "$bin,$T,$trial,$ns_per_op" >> $CSV
            echo "$bin T=$T trial=$trial: ${ns_per_op} ns/op"
        done
    done
done

echo "Results saved to $CSV"
