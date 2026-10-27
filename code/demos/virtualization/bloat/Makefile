include ../../../mk/demo.mk

CFLAGS := -Wall -g -fPIC

# Default target: build sample and libbloat.so
all: sample libbloat.so

# Build libbloat.so from bloat.c
libbloat.so: bloat.c
	$(CC) $(CFLAGS) -shared $< -o $@

# Build sample linked against libbloat.so
sample: sample.c libbloat.so
	$(CC) $(CFLAGS) $< -L. -lbloat -Wl,-rpath,. -o $@

clean:
	rm -f sample libbloat.so

.PHONY: all clean
