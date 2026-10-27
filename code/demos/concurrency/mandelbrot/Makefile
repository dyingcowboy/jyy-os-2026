include ../../../mk/demo.mk

# Apple clang 默认不带 OpenMP（Homebrew 的 libomp 或 llvm 才带）。
# 这里探测一下：有 OpenMP 就并行编译，没有就退化成单线程版本，
# 源码里的 "#pragma omp" 会被忽略，程序照样能编译、运行。
OPENMP_OK := $(shell printf 'int main(void){return 0;}\n' \
	| $(CC) -fopenmp -x c - -o /dev/null >/dev/null 2>&1 && echo yes)

ifeq ($(OPENMP_OK),yes)
  CFLAGS := -O2 -fopenmp -I$(TLIB_PATH) $(PTHREAD)
else
  CFLAGS := -O2 -I$(TLIB_PATH) $(PTHREAD)
  # 只有真正要编译时才提示，make clean / make status 不打扰
  ifeq ($(filter clean status,$(MAKECMDGOALS)),)
    $(info 提示：当前编译器不支持 OpenMP，mandelbrot 将按单线程构建。)
  endif
endif

all: mandelbrot

mandelbrot: mandelbrot.c
	$(CC) $(CFLAGS) -o $@ $^ -lm

clean:
	rm -f mandelbrot *.jpg *.ppm

.PHONY: all clean
