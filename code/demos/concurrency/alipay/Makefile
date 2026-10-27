include ../../../mk/demo.mk

all: alipay

CFLAGS := -O1 -g -I$(TLIB_PATH) $(PTHREAD)

alipay: alipay.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f alipay

.PHONY: all clean
