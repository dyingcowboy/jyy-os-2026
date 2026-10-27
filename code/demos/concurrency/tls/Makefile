include ../../../mk/demo.mk

# -std=c23 需要较新的编译器（Apple clang 16+ / GCC 14+）
CFLAGS := -Wall -g -O2 -I$(TLIB_PATH) -std=c23 $(PTHREAD)

SRCS := $(wildcard *.c)
OBJS := $(SRCS:.c=)

# Default target
all: $(OBJS)

%: %.c
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -f $(OBJS)

.PHONY: all clean
