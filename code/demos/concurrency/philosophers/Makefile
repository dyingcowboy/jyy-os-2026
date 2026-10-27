include ../../../mk/demo.mk

all: philosophers

CFLAGS := -O2 -I$(TLIB_PATH) $(PTHREAD)

philosophers: philosophers.c
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -f philosophers

.PHONY: all clean
