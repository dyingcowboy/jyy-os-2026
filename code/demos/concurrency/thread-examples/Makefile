include ../../../mk/demo.mk

CFLAGS := -O1 -g -I$(TLIB_PATH) $(PTHREAD)

SRCS := $(wildcard *.c)
OBJS := $(SRCS:.c=)

# Default target
all: $(OBJS)

%: %.c
	$(CC) $(CFLAGS) $< -o $@

# 两个程序都是无限循环的观察类 demo，这里只提示怎么跑。
run: all
	@echo "两个 demo 都会一直循环，用 Ctrl-C 退出："
	@echo "  ./test_shm     # 观察两个线程读写共享变量"
	@echo "  ./test_stack   # 观察每个线程独立的栈"

clean:
	rm -f $(OBJS)

.PHONY: all clean run
