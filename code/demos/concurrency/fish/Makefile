include ../../../mk/demo.mk

all: fish

CFLAGS := -O2 -I$(TLIB_PATH) $(PTHREAD)

fish: fish.c
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -f fish

.PHONY: all clean
