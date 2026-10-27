include ../../../mk/demo.mk

# 静态编译能让系统调用序列更干净，便于 strace 观察。
# macOS 不支持 -static（没有静态 crt0），所以只在 Linux 上加这个参数。
ifeq ($(IS_LINUX),1)
CFLAGS := -Wall -g -static
else
CFLAGS := -Wall -g
endif

SRCS := $(wildcard *.c)
OBJS := $(SRCS:.c=)

all: $(OBJS)

%: %.c
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -f $(OBJS)

.PHONY: all clean
