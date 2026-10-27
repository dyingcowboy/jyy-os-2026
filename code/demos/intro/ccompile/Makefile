include ../../../mk/demo.mk

CFLAGS := -Wall

all: examples-O0.s examples-O2.s

%-O0.s: %.c
	$(CC) $(CFLAGS) $< -S -o $@

%-O2.s: %.c
	$(CC) $(CFLAGS) $< -O2 -S -o $@

clean:
	rm -f *.s

.PHONY: all clean
