# 指令级并行 (ILP)

在树莓派 2 (Cortex-A7, 顺序双发射) 上用内联汇编构造不同数据依赖关系的指令序列（依赖链、独立整数、VFP 浮点、NEON SIMD、整数+浮点混合、独立乘法），通过 `perf stat` 测量每种模式下的 IPC (Instructions Per Cycle)，直观感受处理器如何利用指令级并行提升性能。
