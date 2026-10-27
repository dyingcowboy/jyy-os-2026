include ../../../../mk/demo.mk

# 这个 demo 用 fle.py 自己实现「编译器 + 链接器 + 可执行文件格式」。
# 但 libc.c 里是用 x86-64 寄存器约束的内联汇编直接发 syscall 指令，
# 在 ARM 的 Mac 上没法编译（也没有 Linux 头文件可用）。
#
# 原来的规则（在 Linux x86-64 上）：
#     tools:  ln -f -s ../fle.py cc / ld / exec / ...
#     %.o:    ./cc $(CFLAGS) $< -o $@
#     hello:  ./ld $(SRCS:.c=.fle) -o $@
DEMO_SKIP_REASON := 需要 x86-64 内联汇编与 Linux 系统调用
$(eval $(call skip_demo))
