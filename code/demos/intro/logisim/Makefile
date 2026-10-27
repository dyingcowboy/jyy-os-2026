include ../../../mk/demo.mk

all: logisim

logisim: logisim.c
	$(CC) -I. -o $@ logisim.c

run: logisim
	./logisim | python3 seg-display.py  # The UNIX Philosophy

clean:
	rm -f logisim

.PHONY: all clean run
