include ../../../mk/demo.mk

CFLAGS := -Wall -g

SRCS := $(wildcard *.c)
OBJS := $(SRCS:.c=)

# Default target
all: $(OBJS)

%: %.c
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -f $(OBJS) /tmp/my_pipe

.PHONY: all clean
