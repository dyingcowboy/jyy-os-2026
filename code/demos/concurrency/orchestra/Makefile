include ../../../mk/demo.mk

CFLAGS := -O2 -I$(TLIB_PATH) $(PTHREAD)

all: orchestra orchestra-cv

# 音符是 gen-notes.py 合成的（纯标准库，不再依赖 numpy）。
# 用 stamp 文件记录一次生成结果，避免每次 make 都重新合成 84 个 wav。
notes/.stamp: gen-notes.py
	python3 gen-notes.py
	@touch $@

orchestra: orchestra.c main.c notes/.stamp
	$(CC) $(CFLAGS) -o $@ $<

orchestra-cv: orchestra-cv.c main.c notes/.stamp
	$(CC) $(CFLAGS) -o $@ $<

# 运行时需要 ffplay（ffmpeg 自带）来播放 notes/*.wav
run: all
	./orchestra

clean:
	rm -rf notes orchestra orchestra-cv

.PHONY: all clean run
