include ../../../mk/demo.mk

TITLE := $(shell python3 -c "import json; print(json.load(open('script.json'))['title'])")

all: game

game: script.json ggmaker.py
	python3 ggmaker.py script.json

run: game
	./start.sh "$(TITLE)"

# FUSE 版虚拟文件系统（ggfs）需要 libfuse；macOS 上对应 macFUSE。
# 没装就跳过这个目标，不影响 game 本身。
FUSE_OK := $(shell pkg-config --exists fuse 2>/dev/null && echo yes)

ifeq ($(FUSE_OK),yes)
FUSE_CFLAGS  ?= $(shell pkg-config --cflags fuse 2>/dev/null)
FUSE_LDFLAGS ?= $(shell pkg-config --libs fuse 2>/dev/null || echo -lfuse)

ggfs: ggfs.c cJSON.h cJSON.c
	$(CC) -D_FILE_OFFSET_BITS=64 -Wall -O2 $(FUSE_CFLAGS) -o $@ ggfs.c cJSON.c $(FUSE_LDFLAGS)

fuse: ggfs
	mkdir -p /tmp/ggfs
	sudo ./ggfs script.json /tmp/ggfs
else
ggfs fuse:
	@printf '\n [跳过] ggfs 需要 libfuse（macOS 上是 macFUSE）\n\n'
endif

clean:
	rm -rf "$(TITLE)" ggfs

.PHONY: all clean game run fuse
