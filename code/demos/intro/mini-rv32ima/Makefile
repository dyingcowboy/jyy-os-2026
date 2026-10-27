include ../../../mk/demo.mk

all: mini-rv32ima

mini-rv32ima: main.c mini-rv32ima.h
	$(CC) -g -o $@ $<

clean:
	rm -f mini-rv32ima

.PHONY: all clean
