include ../../../mk/demo.mk

# 这个 demo 用 bpftrace 追踪块设备 I/O 的生命周期，只能在 Linux 上跑。
# 原来 import 时 bio-tui 丢了可执行位，所以这里显式用 python3 启动。
ifeq ($(IS_LINUX),1)
.PHONY: all run replay trace record clean load

all:
	@echo "用法: make run | make replay | make trace | make record | make load"

# 一键启动 TUI（自动启动 bpftrace → bio-state 管线）
run:
	python3 bio-tui

# 回放录制的追踪日志
replay:
	python3 bio-tui --replay trace.log

# 仅采集 bpftrace 原始数据（调试用）
trace:
	sudo bpftrace bio-trace.bt

# 录制追踪数据到文件（供 replay 使用）
record:
	sudo bpftrace bio-trace.bt > trace.log

# 生成 I/O 测试负载（在另一终端运行）
load:
	dd if=/dev/zero of=/tmp/bio-load.tmp bs=4096 count=500 conv=fsync 2>/dev/null && sync && rm -f /tmp/bio-load.tmp

clean:
	rm -f /tmp/bio-load*.tmp trace.log
else
DEMO_SKIP_REASON := 需要 bpftrace 与 Linux 块设备追踪
$(eval $(call skip_demo))
endif
