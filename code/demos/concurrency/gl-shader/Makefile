CC = gcc
CFLAGS = -Wall -O2 $(shell pkg-config --cflags glfw3)
LDLIBS = $(shell pkg-config --libs glfw3) -ldl -lm

glshader: main.c
	$(CC) $(CFLAGS) -o $@ $< $(LDLIBS)

clean:
	rm -f glshader
