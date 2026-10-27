include ../../../mk/demo.mk

# PostScript 的 page.ps 需要 Ghostscript 的 ps2pdf 才能转成 PDF。
ifeq ($(shell command -v ps2pdf 2>/dev/null),)
DEMO_SKIP_REASON := 需要 Ghostscript 的 ps2pdf（brew install ghostscript）
$(eval $(call skip_demo))
else
all: page.pdf

page.pdf: page.ps
	ps2pdf page.ps

clean:
	rm -f page.pdf

.PHONY: all clean
endif
