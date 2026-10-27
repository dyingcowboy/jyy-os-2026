include ../../../mk/demo.mk

CFLAGS = -O2

RV_CC    = riscv64-unknown-elf-gcc
RV_FLAGS = -march=rv32ima -ffreestanding -nostdlib -march=rv32ima -mabi=ilp32 \
           -Wl,-Ttext=0x80000000

HAVE_RV := $(shell command -v riscv64-unknown-elf-gcc 2>/dev/null)

# crazy-os 是跑在宿主机上的 RISC-V 模拟器，本身可以直接编译；
# 它加载的 p1.bin / p2.bin 需要 riscv32 交叉工具链，没有就只构建模拟器。
all: crazy-os
ifeq ($(HAVE_RV),)
ifeq ($(filter clean status,$(MAKECMDGOALS)),)
$(info 提示：未找到 riscv64-unknown-elf-gcc，只构建 crazy-os，不生成 p1.bin/p2.bin。)
endif
else
all: p1.bin p2.bin
endif

crazy-os: crazy-os.c mini-rv32ima.h
	$(CC) $(CFLAGS) -o $@ $<

%.elf: %.c lib.h
	$(RV_CC) $(RV_FLAGS) -o $@ $<

%.bin: %.elf
	riscv64-unknown-elf-objcopy -O binary $< $@

run: all
	@test -f p1.bin && test -f p2.bin \
	  || { echo "运行需要 p1.bin/p2.bin（riscv64-unknown-elf 工具链）"; exit 1; }
	./crazy-os p1.bin p2.bin

clean:
	rm -f crazy-os *.elf *.bin

.PHONY: all clean run
