include ../../../mk/demo.mk

CFLAGS := -O2 -I$(TLIB_PATH) $(PTHREAD)

all: therac25

therac25: therac25.c
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -f therac25

.PHONY: all clean
