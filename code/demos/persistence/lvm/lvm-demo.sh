#!/bin/bash
# LVM demo: 8 image files → PV → VG → LV → GPT partition → FAT32 + ext4
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
    echo "PANIC: this script must be run as root" >&2
    exit 1
fi

IMG_DIR="$(cd "$(dirname "$0")" && pwd)/images"
IMG_COUNT=8
IMG_SIZE=32  # MiB per image
VG_NAME=vg_demo
LV_NAME=lv_demo
LV_PATH="/dev/${VG_NAME}/${LV_NAME}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
STRACE_LOG="${SCRIPT_DIR}/strace.log"

# 清空旧日志
: > "$STRACE_LOG"

trace_lvm() {
    local title="$1"; shift
    local tmp="${STRACE_LOG}.tmp.$$"
    echo "" >> "$STRACE_LOG"
    echo "=== $(date +%H:%M:%S) $title ===" >> "$STRACE_LOG"
    strace -f -o "$tmp" \
        -e trace=ioctl,openat,fsync \
        -- "$@"
    cat "$tmp" >> "$STRACE_LOG"
    rm -f "$tmp"
}

# --- 1. Create 8 small image files ---
mkdir -p "$IMG_DIR"
for i in $(seq 1 $IMG_COUNT); do
    img="${IMG_DIR}/disk${i}.img"
    if [ -f "$img" ]; then
        echo "[skip] $img already exists"
    else
        truncate -s "${IMG_SIZE}M" "$img"
        echo "[ok]   created $img (${IMG_SIZE}MiB)"
    fi
done

# --- 2. Set up loop devices & LVM ---
LOOP_DEVS=()
for i in $(seq 1 $IMG_COUNT); do
    img="${IMG_DIR}/disk${i}.img"
    wipefs -a "$img" 2>/dev/null || true   # clean leftover signatures
    dev=$(trace_lvm "losetup $img" losetup --find --show "$img")
    LOOP_DEVS+=("$dev")
    echo "[ok]   loop device $dev ← disk${i}.img"
done

# Create PVs on all loop devices
for dev in "${LOOP_DEVS[@]}"; do
    trace_lvm "pvcreate $dev" pvcreate -f "$dev"
done
echo "[ok]   PVs created on ${#LOOP_DEVS[@]} loop devices"

# Create VG spanning all PVs
trace_lvm "vgcreate" vgcreate "$VG_NAME" "${LOOP_DEVS[@]}"
echo "[ok]   VG '$VG_NAME' created"

# Create LV using all free space
trace_lvm "lvcreate" lvcreate -y -l 100%FREE -n "$LV_NAME" "$VG_NAME"
LV_SIZE=$(blockdev --getsize64 "$LV_PATH")
echo "[ok]   LV '$LV_PATH' created ($((LV_SIZE / 1024 / 1024))MiB)"

# --- 3. Partition with GPT: one FAT32 + one ext4 (50/50) ---
# sgdisk %-syntax is unreliable; use explicit sector count
LV_SECTORS=$(blockdev --getsz "$LV_PATH")
HALF_SECTORS=$((LV_SECTORS / 2))
PART_START=2048
PART1_END=$((PART_START + HALF_SECTORS - 1))

sgdisk -og "$LV_PATH"
sgdisk -n "1:${PART_START}:${PART1_END}" -t 1:0700 "$LV_PATH"
sgdisk -n "2:0:0" -t 2:8300 "$LV_PATH"
echo "[ok]   GPT table: 2 equal partitions"

# Create partition device mappings (needed for DM/LVM devices)
trace_lvm "kpartx" kpartx -av "$LV_PATH"

PART1="/dev/mapper/${VG_NAME}-${LV_NAME}1"
PART2="/dev/mapper/${VG_NAME}-${LV_NAME}2"

# Format
mkfs.vfat -F 32 "$PART1"
echo "[ok]   FAT32 formatted on $PART1"

mkfs.ext4 -F "$PART2"
echo "[ok]   ext4 formatted on $PART2"

# --- 4. Mount partitions ---
mkdir -p ./p1 ./p2
mount "$PART1" ./p1
echo "[ok]   $PART1 → ./p1"
mount "$PART2" ./p2
echo "[ok]   $PART2 → ./p2"

echo ""
echo "=== Done ==="
echo "LV:     $LV_PATH ($((LV_SIZE / 1024 / 1024))MiB across $IMG_COUNT images)"
echo "Part 1: FAT32  $PART1"
echo "Part 2: ext4   $PART2"
echo ""
echo "To tear down:"
echo "  ./lvm-cleanup.sh"
