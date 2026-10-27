include ../../../mk/demo.mk

all: join-1 join-2

CFLAGS := -O2 -I$(TLIB_PATH) $(PTHREAD)

join-1: join-1.c main.c
	$(CC) $(CFLAGS) -o $@ $^

join-2: join-2.c main.c
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -f join-1 join-2

.PHONY: all clean
