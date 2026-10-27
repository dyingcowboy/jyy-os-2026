include ../../../mk/demo.mk

# 这个 demo 需要 GLFW3 和 glad 生成的加载器头文件（glad/glad.h）。
# glad 的头文件要自己生成，仓库里没有附带，所以默认构建不了。
GLFW_OK := $(shell pkg-config --exists glfw3 2>/dev/null && echo yes)

ifeq ($(GLFW_OK),yes)
CFLAGS := -Wall -O2 $(shell pkg-config --cflags glfw3)
LDLIBS := $(shell pkg-config --libs glfw3) -ldl -lm

all: glshader

glshader: main.c
	$(CC) $(CFLAGS) -o $@ $< $(LDLIBS)

clean:
	rm -f glshader

.PHONY: all clean
else
DEMO_SKIP_REASON := 需要 GLFW3 与 glad 头文件（glad 需自行生成）
$(eval $(call skip_demo))
endif
