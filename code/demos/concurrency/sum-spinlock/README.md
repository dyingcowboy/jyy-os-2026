# 使用硬件原子指令实现互斥

我们的线程库也提供了 spin_lock, spin_unlock 的 API 实现互斥，直接用 inline assembly 调用指令集实现——在实际上，GCC 提供了 __atomic_compare_exchange_n 的 built-in 帮助我们实现跨体系结构的可移植性：例如，armv8.1 加入了新的原子指令，使用正确的编译选项可以获得最佳的性能。
