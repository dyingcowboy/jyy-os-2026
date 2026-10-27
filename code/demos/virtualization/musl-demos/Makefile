include ../../../mk/demo.mk

# 用 musl-gcc 静态链接，配合 strace 观察 libc 到底做了什么。
ifeq ($(shell command -v musl-gcc 2>/dev/null),)
DEMO_SKIP_REASON := 需要 musl-gcc（musl 工具链）
$(eval $(call skip_demo))
else
CFLAGS := -O2 -g3 -static

SRCS := $(wildcard *.c)
OBJS := $(SRCS:.c=)

all: $(OBJS)

%: %.c
	musl-gcc $(CFLAGS) $< -o $@

clean:
	rm -f $(OBJS)

.PHONY: all clean
endif
