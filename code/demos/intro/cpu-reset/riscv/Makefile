include ../../../../mk/demo.mk

# 交叉编译 riscv64 裸机程序：需要 riscv64-linux-gnu 工具链和 qemu-system-riscv64。
# macOS 上没有这套工具链，make 会打印跳过说明。
ifeq ($(shell command -v riscv64-linux-gnu-gcc 2>/dev/null),)
DEMO_SKIP_REASON := 需要 riscv64-linux-gnu 交叉工具链与 qemu-system-riscv64
$(eval $(call skip_demo))
else
CC = riscv64-linux-gnu-gcc
LD = riscv64-linux-gnu-ld
OBJCOPY = riscv64-linux-gnu-objcopy
QEMU = qemu-system-riscv64

all: kernel.bin

kernel.bin: start.S
	$(CC) -c $< -o start.o -march=rv64gc -mabi=lp64 -nostdlib -fno-asynchronous-unwind-tables
	$(LD) start.o -o kernel.elf -T riscv.ld
	$(OBJCOPY) -O binary kernel.elf $@

run: kernel.bin
	$(QEMU) -machine virt -bios none -device loader,file=kernel.bin,addr=0x1000 -nographic -d in_asm,cpu,exec -smp 1 -D /dev/stdout

clean:
	rm -f start.o kernel.elf kernel.bin

.PHONY: all run clean
endif
