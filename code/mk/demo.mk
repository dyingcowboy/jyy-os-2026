# =============================================================================
#  课堂 demo 统一构建配置
# -----------------------------------------------------------------------------
#  各 demo 目录的 Makefile 用相对路径引入本文件：
#
#      include ../../../mk/demo.mk     # demos/<topic>/<demo>/
#      include ../../../../mk/demo.mk  # demos/<topic>/<sub>/<demo>/
#
#  这里只提供跨平台默认值和平台探测，具体的构建规则仍写在各 demo 自己的
#  Makefile 里。目标平台：macOS（arm64 / x86_64）与 Linux。
# =============================================================================

# ---- 仓库根目录 -------------------------------------------------------------
MK_DIR  := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))
ROOT    := $(abspath $(MK_DIR)/..)
DEMO_ID := $(patsubst demos/%,%,$(patsubst $(ROOT)/%,%,$(CURDIR)))

# ---- 平台探测 ---------------------------------------------------------------
UNAME_S := $(shell uname -s)
UNAME_M := $(shell uname -m)

ifeq ($(UNAME_S),Darwin)
  HOST_OS := macos
else ifeq ($(UNAME_S),Linux)
  HOST_OS := linux
else
  HOST_OS := $(UNAME_S)
endif

HOST_ARCH := $(UNAME_M)
IS_MACOS  := $(if $(filter macos,$(HOST_OS)),1,)
IS_LINUX  := $(if $(filter linux,$(HOST_OS)),1,)

# 本文件里的规则会出现在各 demo Makefile 的最前面，显式指定默认目标，
# 免得 `make` 执行到 status 之类的辅助目标。
.DEFAULT_GOAL := all

# ---- 编译器 -----------------------------------------------------------------
# 这里不给 CC 赋值：GNU make 内建 CC=cc，macOS 上就是 Apple clang。
# 各 demo 里请写 $(CC)/$(CXX)，不要硬编码 gcc/g++，这样 `make CC=gcc-14`
# 或者环境变量覆盖才会生效。
CXX ?= c++

# ---- 线程 -------------------------------------------------------------------
# 用到 pthread 的 demo 请把 $(PTHREAD) 加进编译/链接参数。
# macOS 的 pthread 在 libSystem 里，-pthread 只是让编译器定义 _REENTRANT；
# Linux 上 -pthread 负责链接 libpthread。两个平台都接受这个写法。
PTHREAD ?= -pthread

# ---- 课程线程库 thread-lib ---------------------------------------------------
# 这些 demo 原来依赖调用者自己 export TLIB_PATH=../thread-lib；忘记设置时，
# `-I$(TLIB_PATH)` 会退化成裸 `-I`，把后面的参数（比如 -o）当成头文件目录，
# 报出来的错误完全对不上真实原因。这里给出默认值，`make TLIB_PATH=...` 仍可覆盖。
THREAD_LIB ?= $(ROOT)/demos/concurrency/thread-lib
TLIB_PATH  ?= $(THREAD_LIB)

# ---- 无法在本机构建时的统一处理 ----------------------------------------------
# 用法：把规则包在平台判断里，不支持的平台上这样写——
#
#      DEMO_SKIP_REASON := 需要 Linux 的 <linux/kvm.h>
#      $(eval $(call skip_demo))
#
# 注意要用 eval 包一层：skip_demo 展开后是多行规则，make 需要重新解析。
# make 会打印一行中文说明并以成功状态退出，顶层批量构建时记为“跳过”。
DEMO_SKIP_REASON ?=

define skip_demo
.PHONY: all clean
all:
	@printf '\n \033[1;33m[跳过]\033[0m %s\n' '$(DEMO_ID)'
	@printf '        原因：%s\n' '$(DEMO_SKIP_REASON)'
	@printf '        当前平台：$(HOST_OS)/$(HOST_ARCH)\n\n'
clean:
	@:
endef

# ---- 统一的状态查询（供顶层 make status 调用）--------------------------------
.PHONY: status
status:
	@printf '%-46s %s\n' '$(DEMO_ID)' \
	  '$(if $(strip $(DEMO_SKIP_REASON)),跳过 — $(DEMO_SKIP_REASON),可构建)'
