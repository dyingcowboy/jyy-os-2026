include ../../../mk/demo.mk

# 用 timerfd + epoll 做一个「轮子」库，需要 Linux 的 <sys/timerfd.h>。
ifeq ($(IS_LINUX),1)
CFLAGS = -fPIC -shared -O2 -Wall -Wextra -D_GNU_SOURCE
TARGET = libwheel.so
SRC = wheel.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -f $(TARGET)

.PHONY: all clean
else
DEMO_SKIP_REASON := 需要 Linux 的 <sys/timerfd.h> 与 epoll
$(eval $(call skip_demo))
endif
