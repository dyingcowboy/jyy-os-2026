include ../../../mk/demo.mk

# 这个 demo 用 x86-64 汇编直接调用 Linux 系统调用（SYS_write / SYS_exit），
# 演示「编译 -> 汇编 -> 链接」三步。macOS 自带的是 Mach-O 的 as/ld，
# 既不能汇编 x86-64 指令，也不认 Linux 的 syscall 约定，所以本机跳过。
#
# 原来的三步是（在 Linux x86-64 上）：
#     $(CC) -g -S minimal.S > minimal.s
#     as minimal.s -o minimal.o
#     ld -o minimal minimal.o
DEMO_SKIP_REASON := 需要 x86-64 汇编与 Linux 系统调用（macOS 的 as/ld 不适用）
$(eval $(call skip_demo))
