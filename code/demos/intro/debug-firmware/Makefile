include ../../../mk/demo.mk

# 磁盘映像本身在 macOS 上也能生成（xxd 属于 vim 自带工具）；
# 真正运行它才需要 qemu-system-x86_64。
all: minimal.img

minimal.img: Makefile
	( echo "eb fe 11 22 33 44" | xxd -r -p; \
	  cat /dev/zero | head -c 504; \
	  echo "55 aa" | xxd -r -p \
	) > minimal.img

run: minimal.img
	@command -v qemu-system-x86_64 >/dev/null 2>&1 || { \
	  echo "需要 qemu-system-x86_64：brew install qemu"; exit 1; }
	qemu-system-x86_64 -monitor stdio $<

debug: minimal.img
	@command -v qemu-system-x86_64 >/dev/null 2>&1 || { \
	  echo "需要 qemu-system-x86_64：brew install qemu"; exit 1; }
	qemu-system-x86_64 -s -S $< &
	gdb-multiarch -x init.gdb

clean:
	rm -f *.img

.PHONY: all clean run debug
