include ../../../mk/demo.mk

# 栈溢出实验要静态链接、关闭栈保护、允许可执行栈，并且是针对 x86-64 的。
# 需要 x86_64-linux-gnu-gcc；macOS 没有这套交叉工具链。
ifeq ($(shell command -v x86_64-linux-gnu-gcc 2>/dev/null),)
DEMO_SKIP_REASON := 需要 x86_64-linux-gnu-gcc（静态链接 + 可执行栈的 32/64 位实验）
$(eval $(call skip_demo))
else
CC        = x86_64-linux-gnu-gcc
CFLAGS    = -static -fno-stack-protector -z execstack -no-pie -g -m64
TARGET    = vulnerable

all: $(TARGET)

$(TARGET): vulnerable.c
	$(CC) $(CFLAGS) -o $@ $<

exploit: $(TARGET)
	python3 exploit.py

clean:
	rm -f $(TARGET) exploit.bin

.PHONY: all clean exploit
endif
