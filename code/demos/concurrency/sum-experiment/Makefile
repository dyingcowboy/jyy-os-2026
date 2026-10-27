include ../../../mk/demo.mk

CFLAGS := -O2 -I$(TLIB_PATH) $(PTHREAD)

# sum-trap 用 futex 系统调用实现互斥，头文件 <linux/futex.h> 只在 Linux 上有，
# 所以这个变体在 macOS 上不构建，其余三个变体照常构建。
TARGETS := atomic mutex spin
ifeq ($(IS_LINUX),1)
  TARGETS += trap
endif

all: $(TARGETS)

atomic: sum-atomic.c main.c
	$(CC) $(CFLAGS) -o $@ $^

mutex: sum-mutex.c main.c
	$(CC) $(CFLAGS) -o $@ $^

spin: sum-spin.c main.c
	$(CC) $(CFLAGS) -o $@ $^

trap: sum-trap.c main.c
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -f atomic mutex spin trap

.PHONY: all clean
