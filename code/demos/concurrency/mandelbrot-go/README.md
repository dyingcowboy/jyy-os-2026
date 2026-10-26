# Mandelbrot-Go

多个 goroutine 按行分块并行计算 Mandelbrot 集，通过 channel (`done`) 汇报完成，monitor 用 `select` 同时监听完成信号和定时器实现实时预览，最终由 `finish` channel 通知主线程退出。
