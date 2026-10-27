include ../../../mk/demo.mk

# 内核模块 + 用户态启动器，只能在 Linux 上编译（需要内核头文件）。
ifeq ($(IS_LINUX),1)
# Set the name of the kernel module
obj-m := driver.o

# Set the path to the kernel source directory
KERNEL_SRC := /lib/modules/$(shell uname -r)/build

# Set the current working directory
PWD := $(shell pwd)

all:
	$(MAKE) -C $(KERNEL_SRC) M=$(PWD) modules
	$(CC) -static $(CFLAGS) -o launch user.c

clean:
	$(MAKE) -C $(KERNEL_SRC) M=$(PWD) clean
	rm -f launch

.PHONY: all clean
else
DEMO_SKIP_REASON := 需要 Linux 内核头文件（内核模块）
$(eval $(call skip_demo))
endif
