include ../../../mk/demo.mk

CFLAGS := -Wall -g

SRCS := $(wildcard *.c)
OBJS := $(SRCS:.c=)

# Default target
all: $(OBJS)

%: %.c
	$(CC) testkit/testkit.c $(CFLAGS) $< -o $@

clean:
	rm -f $(OBJS) /tmp/my_pipe

.PHONY: all clean
