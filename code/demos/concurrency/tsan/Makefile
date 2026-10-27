include ../../../mk/demo.mk

CFLAGS := -g -I$(TLIB_PATH) $(PTHREAD)

all: race trace-race
ifeq ($(IS_LINUX),1)
  # QEMU 插件只能在 Linux 上编译（需要 qemu-plugin.h 和 glib）
  all: qemu-memtrace.so
endif

# --- Original TSAN demo ---
race: race.c Makefile
	$(CC) -O2 -fsanitize=thread $(CFLAGS) -o $@ $<

trace-race: trace-race.c
	$(CC) -O0 $(CFLAGS) -o $@ $<

# --- QEMU memory trace plugin (Linux only) ---
#
# Requires: qemu-user-static, glib-2.0-dev
#
# Ubuntu/Debian: apt install qemu-user-static libglib2.0-dev
#
# Adjust QEMU_PLUGINDIR if qemu-plugin.h is elsewhere:
#   make QEMU_PLUGINDIR=/usr/include qemu-memtrace.so

QEMU_PLUGINDIR ?= /usr/include
GLIB_CFLAGS   := $(shell pkg-config --cflags glib-2.0 2>/dev/null)
GLIB_LDFLAGS  := $(shell pkg-config --libs   glib-2.0 2>/dev/null)

qemu-memtrace.so: qemu-memtrace.c
	$(CC) -shared -fPIC -O2 -Wall -Wextra \
		-I$(QEMU_PLUGINDIR) $(GLIB_CFLAGS) \
		-o $@ $< $(GLIB_LDFLAGS)

clean:
	rm -f race qemu-memtrace.so trace-race

.PHONY: all clean
