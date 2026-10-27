include ../../../mk/demo.mk

# 需要先 clone 并编译 minix2（一个可在 Linux 上跑的 MINIX 模拟器），
# 再配合 qemu 启动，整个过程依赖 Linux 工具链。
ifeq ($(IS_LINUX),1)
MINIX := minix-1.7
# MINIX := minix-2.0

all: minix2

run: minix2
	cd minix2 \
	  && ln -s -f images/$(MINIX)-hd-*.img hd.img \
	  && ./runqemu

minix2:
	git clone --depth 1 --single-branch -b master \
	  https://github.com/davidgiven/minix2
	cd minix2 \
	  && ./mkall \
	  && gunzip images/*.gz

clean:
	rm -rf minix2

.PHONY: all minix2 run clean
else
DEMO_SKIP_REASON := 需要 Linux + qemu 编译运行 minix2
$(eval $(call skip_demo))
endif
