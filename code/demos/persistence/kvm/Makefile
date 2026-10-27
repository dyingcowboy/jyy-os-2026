include ../../../mk/demo.mk

# 通过 /dev/kvm 直接操作 KVM 的 demo，需要 Linux 的 <linux/kvm.h>。
ifeq ($(IS_LINUX),1)
CFLAGS := -Wall -g

SRCS := $(wildcard *.c)
OBJS := $(SRCS:.c=)

all: $(OBJS)

%: %.c
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -f $(OBJS)

.PHONY: all clean
else
DEMO_SKIP_REASON := 需要 Linux 的 <linux/kvm.h> 与 /dev/kvm
$(eval $(call skip_demo))
endif
