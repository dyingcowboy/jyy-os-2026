include ../../../mk/demo.mk

# 这是上游 OpenSBI 的构建系统，需要 Linux + riscv64-linux-gnu 交叉工具链。
# 上游文件完整保留在同目录的 Makefile.opensbi，下面的 include 会原样使用它，
# 只是在本机缺少工具链时先拦一层，免得 make 抛出难懂的错误。
ifneq ($(IS_LINUX),1)
DEMO_SKIP_REASON := 需要 Linux + riscv64-linux-gnu 交叉工具链（OpenSBI 固件）
$(eval $(call skip_demo))
else ifeq ($(shell command -v riscv64-linux-gnu-gcc 2>/dev/null),)
DEMO_SKIP_REASON := 需要 riscv64-linux-gnu 交叉工具链（OpenSBI 固件）
$(eval $(call skip_demo))
else
include Makefile.opensbi
endif
