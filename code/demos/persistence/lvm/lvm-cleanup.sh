#!/bin/bash
# Tear down the LVM demo — removes everything created by lvm-demo.sh
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
    echo "PANIC: this script must be run as root" >&2
    exit 1
fi

VG_NAME=vg_demo
LV_PATH="/dev/${VG_NAME}/lv_demo"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
IMG_DIR="${SCRIPT_DIR}/images"

echo "=== LVM Demo Cleanup ==="

# 1. Unmount partitions and remove mount dirs
for mp in "${SCRIPT_DIR}/p1" "${SCRIPT_DIR}/p2"; do
    if mountpoint -q "$mp" 2>/dev/null; then
        umount "$mp"
        echo "[ok]   unmounted $mp"
    fi
    rm -rf "$mp"
done
echo "[ok]   mount dirs removed"

# 2. Remove partition device mappings
if [ -e "$LV_PATH" ]; then
    kpartx -dv "$LV_PATH" 2>/dev/null || true
    echo "[ok]   partition mappings removed"
else
    echo "[skip] no LV found"
fi

# 3. Deactivate LV
lvchange -an "$LV_PATH" 2>/dev/null || true

# 4. Remove LV
lvremove -f "$LV_PATH" 2>/dev/null || true
echo "[ok]   LV removed"

# 5. Remove VG
vgremove -f "$VG_NAME" 2>/dev/null || true
echo "[ok]   VG removed"

# 6. Remove PVs from all associated loop devices
for dev in $(losetup -ln -O NAME 2>/dev/null); do
    pvremove -ff "$dev" 2>/dev/null || true
done
losetup -D 2>/dev/null || true
echo "[ok]   loop devices detached"

# 7. Delete image files and images/ directory
rm -rf "$IMG_DIR"
echo "[ok]   $IMG_DIR removed"

# 8. Delete log files
rm -f strace.log*

echo "=== Cleanup complete ==="
