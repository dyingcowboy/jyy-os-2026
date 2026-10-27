include ../../../mk/demo.mk

all: peterson

CFLAGS := -O2 -I$(TLIB_PATH) $(PTHREAD)

peterson: peterson.c Makefile
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f peterson

.PHONY: all clean
