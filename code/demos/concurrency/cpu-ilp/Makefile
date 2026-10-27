include ../../../mk/demo.mk

CFLAGS   = -O2
TARGET   = ilp_bench
SCRIPT   = perf_ilp.sh

# ARMv7-A specific flags (Raspberry Pi 2)
CFLAGS_ARMV7 = -march=armv7-a -mtune=cortex-a7 -mfpu=neon-vfpv4

.PHONY: all run clean

all: $(TARGET)

$(TARGET): ilp_bench.c
	$(CC) $(CFLAGS) -o $@ $<

# perf 只在 Linux 上有；macOS 上可以直接运行 ./ilp_bench <变体>
run: $(TARGET)
	./$(SCRIPT)

clean:
	rm -f $(TARGET)
