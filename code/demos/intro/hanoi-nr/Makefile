include ../../../mk/demo.mk

all: hanoi-r hanoi-nr

hanoi-r: hanoi-main.c hanoi-r.c
	$(CC) -g -o $@ $^

hanoi-nr: hanoi-main.c hanoi-nr.c
	$(CC) -g -o $@ $^

clean:
	rm -f hanoi-r hanoi-nr

.PHONY: all clean
