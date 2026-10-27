include ../../../../mk/demo.mk

# x86 启动扇区：需要 nasm 和 qemu-system-x86_64。
ifeq ($(shell command -v nasm 2>/dev/null),)
DEMO_SKIP_REASON := 需要 nasm 与 qemu-system-x86_64
$(eval $(call skip_demo))
else
NASM = nasm
QEMU = qemu-system-x86_64

all: boot.bin

boot.bin: boot.asm
	$(NASM) $< -f bin -o $@

run: boot.bin
	$(QEMU) -drive format=raw,file=$< -nographic -d in_asm,cpu,exec -D /dev/stdout

clean:
	rm -f boot.bin

.PHONY: all run clean
endif
