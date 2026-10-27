include ../../../mk/demo.mk

# 读取 /proc/<pid>/* 并用 prctl 设置进程属性，需要 Linux 的 <sys/prctl.h>
# 和 <linux/capability.h>、<linux/ioprio.h>。
ifeq ($(IS_LINUX),1)
CFLAGS := -Wall -Wextra -O2

all: proc-info

proc-info: proc-info.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f proc-info

.PHONY: all clean
else
DEMO_SKIP_REASON := 需要 Linux 的 <sys/prctl.h> 与 /proc
$(eval $(call skip_demo))
endif
