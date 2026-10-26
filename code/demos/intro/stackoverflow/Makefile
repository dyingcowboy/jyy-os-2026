CC        = x86_64-linux-gnu-gcc
CFLAGS    = -static -fno-stack-protector -z execstack -no-pie -g -m64
TARGET    = vulnerable

.PHONY: all clean exploit

all: $(TARGET)

$(TARGET): vulnerable.c
	$(CC) $(CFLAGS) -o $@ $<

exploit: $(TARGET)
	python3 exploit.py

clean:
	rm -f $(TARGET) exploit.bin
