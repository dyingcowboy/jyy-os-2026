include ../../../mk/demo.mk

all: pc-1 pc-2 pc-cv pc-cv-broadcast

CFLAGS := -O2 -I$(TLIB_PATH) $(PTHREAD)

pc-1: pc-1.c main.c
	$(CC) $(CFLAGS) -o $@ $^

pc-2: pc-2.c main.c
	$(CC) $(CFLAGS) -o $@ $^

pc-cv: pc-cv.c main.c
	$(CC) $(CFLAGS) -o $@ $^

pc-cv-broadcast: pc-cv-broadcast.c main.c
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -f pc-1 pc-2 pc-cv pc-cv-broadcast

.PHONY: all clean
