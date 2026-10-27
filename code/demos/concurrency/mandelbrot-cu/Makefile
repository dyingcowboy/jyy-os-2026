include ../../../mk/demo.mk

# 需要 NVIDIA CUDA Toolkit（nvcc / cuobjdump / nsys）。
# macOS 上没有 CUDA，直接跳过。
ifeq ($(shell command -v nvcc 2>/dev/null),)
DEMO_SKIP_REASON := 需要 NVIDIA CUDA Toolkit（nvcc）
$(eval $(call skip_demo))
else
all: mandelbrot

mandelbrot: mandelbrot.cu
	nvcc -g -O2 $< -o $@
	cuobjdump --dump-ptx mandelbrot > mandelbrot.ptx

run: mandelbrot
	nsys profile --stats=true ./mandelbrot

clean:
	rm -f mandelbrot

.PHONY: all clean run
endif
