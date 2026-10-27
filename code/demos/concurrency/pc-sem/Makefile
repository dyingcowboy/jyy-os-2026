include ../../../mk/demo.mk

all: pc

CFLAGS := -O2 -I$(TLIB_PATH) $(PTHREAD)

pc: pc.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f pc

.PHONY: all clean
