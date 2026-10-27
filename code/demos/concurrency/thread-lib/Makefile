include ../../../mk/demo.mk

all: hello

hello: hello.c
	$(CC) -I. $(PTHREAD) -o $@ $<

clean:
	rm -f hello

.PHONY: all clean
