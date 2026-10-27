include ../../../mk/demo.mk

CFLAGS := -O1 -g -I$(TLIB_PATH) $(PTHREAD)

SRCS := $(wildcard *.c)
OBJS := $(SRCS:.c=)

# Default target
all: $(OBJS)

%: %.c
	$(CC) $(CFLAGS) $< -o $@

# measure.py 会反复启动 ./sleep N 并统计进程资源变化
run: all
	python3 measure.py

clean:
	rm -f $(OBJS)

.PHONY: all clean run
