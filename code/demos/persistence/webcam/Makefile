include ../../../mk/demo.mk

# 通过 V4L2 从摄像头取帧，需要 Linux 的 <linux/videodev2.h>。
ifeq ($(IS_LINUX),1)
CFLAGS := -Wall -g

SRCS := $(wildcard *.c)
OBJS := $(SRCS:.c=)

all: $(OBJS)

%: %.c
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -f $(OBJS) *.log capture.jpg

.PHONY: all clean
else
DEMO_SKIP_REASON := 需要 Linux 的 V4L2（<linux/videodev2.h>）
$(eval $(call skip_demo))
endif
