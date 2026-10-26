# Lecture 与课堂代码对应表

> 来源：JYY《操作系统原理》2026 春季学期官方讲义与 `/OS/demos/` 目录。
> Lect.30 是课程总结，会重新列出全课程代码；为避免误导，下表按 Lect.1–29 的实际首次/重复出现记录，Lect.30 单列为总索引。

## Lect.1：操作系统概述

- [数字电路模拟器](demos/intro/logisim/) — `intro/logisim`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/intro/logisim/)
- [RISC-V 处理器模拟器](demos/intro/mini-rv32ima/) — `intro/mini-rv32ima`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/intro/mini-rv32ima/)
- [汉诺塔](demos/intro/hanoi-nr/) — `intro/hanoi-nr`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/intro/hanoi-nr/)

## Lect.2：应用视角的操作系统

- [C 解释执行器](demos/intro/cinterp/) — `intro/cinterp`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/intro/cinterp/)
- [汉诺塔](demos/intro/hanoi-nr/) — `intro/hanoi-nr`；重复使用；首次见 Lect.1；[官方目录](https://jyywiki.cn/OS/demos/intro/hanoi-nr/)
- [RISC-V 处理器模拟器](demos/intro/mini-rv32ima/) — `intro/mini-rv32ima`；重复使用；首次见 Lect.1；[官方目录](https://jyywiki.cn/OS/demos/intro/mini-rv32ima/)
- [什么是编译器](demos/intro/ccompile/) — `intro/ccompile`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/intro/ccompile/)
- [最小可执行文件](demos/intro/minimal/) — `intro/minimal`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/intro/minimal/)

## Lect.3：硬件视角的操作系统

- [RISC-V 处理器模拟器](demos/intro/mini-rv32ima/) — `intro/mini-rv32ima`；重复使用；首次见 Lect.1；[官方目录](https://jyywiki.cn/OS/demos/intro/mini-rv32ima/)
- [探索 CPU Reset](demos/intro/cpu-reset/) — `intro/cpu-reset`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/intro/cpu-reset/)
- [CIH 病毒](demos/intro/cih/) — `intro/cih`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/intro/cih/)
- [调试 SeaBIOS 固件](demos/intro/debug-firmware/) — `intro/debug-firmware`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/intro/debug-firmware/)
- [OpenSBI](demos/intro/opensbi/) — `intro/opensbi`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/intro/opensbi/)

## Lect.4：Scaling Law 和 Agentic AI (Hacking Day)

- [最小 “操作系统”](demos/intro/os-minimal/) — `intro/os-minimal`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/intro/os-minimal/)

## Lect.5：程序和进程

- [Crazy OS](demos/virtualization/crazy-os/) — `virtualization/crazy-os`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/virtualization/crazy-os/)
- [展示进程信息](demos/virtualization/proc-info/) — `virtualization/proc-info`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/virtualization/proc-info/)
- [创建一棵进程子树](demos/virtualization/pstree/) — `virtualization/pstree`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/virtualization/pstree/)
- [fork-based DFS](demos/virtualization/fork-dfs/) — `virtualization/fork-dfs`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/virtualization/fork-dfs/)
- [理解 fork()](demos/virtualization/fork-demo/) — `virtualization/fork-demo`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/virtualization/fork-demo/)
- [理解 execve](demos/virtualization/execve-demo/) — `virtualization/execve-demo`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/virtualization/execve-demo/)
- [理解 exit](demos/virtualization/exit-demo/) — `virtualization/exit-demo`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/virtualization/exit-demo/)

## Lect.6：进程的地址空间

- [Crazy OS](demos/virtualization/crazy-os/) — `virtualization/crazy-os`；重复使用；首次见 Lect.5；[官方目录](https://jyywiki.cn/OS/demos/virtualization/crazy-os/)
- [重新理解指针](demos/virtualization/pointers/) — `virtualization/pointers`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/virtualization/pointers/)
- [探索进程地址空间](demos/virtualization/addr-space/) — `virtualization/addr-space`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/virtualization/addr-space/)
- [mmap 系统调用](demos/virtualization/mmap/) — `virtualization/mmap`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/virtualization/mmap/)
- [金山游侠](demos/virtualization/knight/) — `virtualization/knight`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/virtualization/knight/)
- [汉诺塔](demos/intro/hanoi-nr/) — `intro/hanoi-nr`；重复使用；首次见 Lect.1；[官方目录](https://jyywiki.cn/OS/demos/intro/hanoi-nr/)

## Lect.7：访问操作系统对象

- [Crazy OS](demos/virtualization/crazy-os/) — `virtualization/crazy-os`；重复使用；首次见 Lect.5；[官方目录](https://jyywiki.cn/OS/demos/virtualization/crazy-os/)
- [文件描述符](demos/virtualization/filedesc/) — `virtualization/filedesc`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/virtualization/filedesc/)
- [UNIX 管道](demos/virtualization/pipe/) — `virtualization/pipe`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/virtualization/pipe/)
- [TestKit 测试框架](demos/virtualization/testkit/) — `virtualization/testkit`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/virtualization/testkit/)

## Lect.8：终端和 UNIX Shell

- [理解终端](demos/virtualization/tty/) — `virtualization/tty`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/virtualization/tty/)
- [信号处理](demos/virtualization/signal/) — `virtualization/signal`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/virtualization/signal/)
- [Shebang](demos/virtualization/shebang/) — `virtualization/shebang`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/virtualization/shebang/)

## Lect.9：C 标准库和实现

- [调试 “小程序”](demos/virtualization/musl-demos/) — `virtualization/musl-demos`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/virtualization/musl-demos/)

## Lect.10：C 标准库和实现 (2)

- [调试 “小程序”](demos/virtualization/musl-demos/) — `virtualization/musl-demos`；重复使用；首次见 Lect.9；[官方目录](https://jyywiki.cn/OS/demos/virtualization/musl-demos/)

## Lect.11：可执行文件

- [Funny Little Executable](demos/virtualization/fle/) — `virtualization/fle`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/virtualization/fle/)
- [Shebang](demos/virtualization/shebang/) — `virtualization/shebang`；重复使用；首次见 Lect.8；[官方目录](https://jyywiki.cn/OS/demos/virtualization/shebang/)
- [动态链接库是进程间共享的吗？](demos/virtualization/bloat/) — `virtualization/bloat`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/virtualization/bloat/)
- [变速齿轮](demos/virtualization/wheel/) — `virtualization/wheel`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/virtualization/wheel/)

## Lect.12：构建应用生态 (Hacking Day)

- [Minix](demos/virtualization/minix/) — `virtualization/minix`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/virtualization/minix/)
- [最小 Linux](demos/virtualization/linux-minimal/) — `virtualization/linux-minimal`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/virtualization/linux-minimal/)
- [Linux](demos/virtualization/linux/) — `virtualization/linux`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/virtualization/linux/)

## Lect.13：多处理器编程：从入门到放弃

- [迷你线程库](demos/concurrency/thread-lib/) — `concurrency/thread-lib`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/thread-lib/)
- [通过线程库理解线程行为](demos/concurrency/thread-examples/) — `concurrency/thread-examples`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/thread-examples/)
- [山寨支付宝](demos/concurrency/alipay/) — `concurrency/alipay`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/alipay/)
- [使用 mutex API 实现互斥](demos/concurrency/sum-mutexapi/) — `concurrency/sum-mutexapi`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/sum-mutexapi/)
- [宽松内存模型](demos/concurrency/mem-model/) — `concurrency/mem-model`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/mem-model/)

## Lect.14：并发控制：互斥

- [尝试关闭中断](demos/concurrency/cli/) — `concurrency/cli`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/cli/)
- [使用 mutex API 实现互斥](demos/concurrency/sum-mutexapi/) — `concurrency/sum-mutexapi`；重复使用；首次见 Lect.13；[官方目录](https://jyywiki.cn/OS/demos/concurrency/sum-mutexapi/)
- [操作系统模型和检查器](demos/mosaic/) — `mosaic`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/mosaic/)
- [Peterson 算法](demos/concurrency/peterson/) — `concurrency/peterson`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/peterson/)
- [使用硬件原子指令实现互斥](demos/concurrency/sum-spinlock/) — `concurrency/sum-spinlock`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/sum-spinlock/)
- [使用不同方式求和](demos/concurrency/sum-experiment/) — `concurrency/sum-experiment`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/sum-experiment/)

## Lect.15：并发控制：同步与条件变量

- [实现乐团同步](demos/concurrency/orchestra/) — `concurrency/orchestra`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/orchestra/)
- [生产者-消费者问题](demos/concurrency/producer-consumer/) — `concurrency/producer-consumer`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/producer-consumer/)
- [奇怪的同步问题](demos/concurrency/fish/) — `concurrency/fish`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/fish/)
- [使用互斥锁实现计算图](demos/concurrency/cgraph-mutex/) — `concurrency/cgraph-mutex`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/cgraph-mutex/)

## Lect.16：并发控制：同步与信号量

- [使用互斥锁实现计算图](demos/concurrency/cgraph-mutex/) — `concurrency/cgraph-mutex`；重复使用；首次见 Lect.15；[官方目录](https://jyywiki.cn/OS/demos/concurrency/cgraph-mutex/)
- [使用信号量实现线程 join](demos/concurrency/join-sem/) — `concurrency/join-sem`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/join-sem/)
- [使用信号量实现计算图](demos/concurrency/cgraph-sem/) — `concurrency/cgraph-sem`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/cgraph-sem/)
- [使用信号量实现生产者-消费者问题](demos/concurrency/pc-sem/) — `concurrency/pc-sem`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/pc-sem/)
- [哲学家吃饭问题](demos/concurrency/philosophers/) — `concurrency/philosophers`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/philosophers/)

## Lect.17：并发 Bug 和应对

- [死锁演示](demos/concurrency/deadlock/) — `concurrency/deadlock`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/deadlock/)
- [lockdep](demos/concurrency/lockdep/) — `concurrency/lockdep`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/lockdep/)
- [ThreadSanitizer](demos/concurrency/tsan/) — `concurrency/tsan`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/tsan/)
- [Therac-25 模拟器](demos/concurrency/therac-25/) — `concurrency/therac-25`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/therac-25/)

## Lect.18：并行算法与数据结构

- [使用不同方式求和](demos/concurrency/sum-experiment/) — `concurrency/sum-experiment`；重复使用；首次见 Lect.14；[官方目录](https://jyywiki.cn/OS/demos/concurrency/sum-experiment/)
- [绘制 Mandelbrot Set](demos/concurrency/mandelbrot/) — `concurrency/mandelbrot`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/mandelbrot/)
- [Thread-local Storage](demos/concurrency/tls/) — `concurrency/tls`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/tls/)

## Lect.19：异步编程模型

- [线程的代价](demos/concurrency/thread-cost/) — `concurrency/thread-cost`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/thread-cost/)
- [轻量级线程的实现](demos/concurrency/coroutine/) — `concurrency/coroutine`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/coroutine/)
- [Mandelbrot-Go](demos/concurrency/mandelbrot-go/) — `concurrency/mandelbrot-go`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/mandelbrot-go/)
- [Web 和事件编程](demos/concurrency/web/) — `concurrency/web`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/web/)

## Lect.20：CPU、GPU 和 SIMT 编程模型

- [RISC-V 处理器模拟器](demos/intro/mini-rv32ima/) — `intro/mini-rv32ima`；重复使用；首次见 Lect.1；[官方目录](https://jyywiki.cn/OS/demos/intro/mini-rv32ima/)
- [指令级并行 (ILP)](demos/concurrency/cpu-ilp/) — `concurrency/cpu-ilp`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/cpu-ilp/)
- [OpenGL Shader](demos/concurrency/gl-shader/) — `concurrency/gl-shader`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/gl-shader/)
- [CUDA 实现的 Mandelbrot Set](demos/concurrency/mandelbrot-cu/) — `concurrency/mandelbrot-cu`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/mandelbrot-cu/)

## Lect.21：一个 Token 的旅程

- [一个 LLM Request](demos/concurrency/llm-request/) — `concurrency/llm-request`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/concurrency/llm-request/)

## Lect.22：输入/输出设备原理

- [GPIO LED](demos/persistence/gpio-led/) — `persistence/gpio-led`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/persistence/gpio-led/)
- [PostScript](demos/persistence/postscript/) — `persistence/postscript`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/persistence/postscript/)
- [一个设备驱动程序](demos/persistence/launcher/) — `persistence/launcher`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/persistence/launcher/)
- [KVM Device](demos/persistence/kvm/) — `persistence/kvm`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/persistence/kvm/)
- [WebCam](demos/persistence/webcam/) — `persistence/webcam`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/persistence/webcam/)

## Lect.23：存储设备的抽象

- [打开 Linux Block I/O](demos/persistence/bio/) — `persistence/bio`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/persistence/bio/)

## Lect.24：文件系统 API (1)

- [最小 Linux](demos/virtualization/linux-minimal/) — `virtualization/linux-minimal`；重复使用；首次见 Lect.12；[官方目录](https://jyywiki.cn/OS/demos/virtualization/linux-minimal/)
- [globbing](demos/persistence/globbing/) — `persistence/globbing`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/persistence/globbing/)
- [Symlink Game](demos/persistence/ggmaker/) — `persistence/ggmaker`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/persistence/ggmaker/)

## Lect.25：文件系统 API (2)

- [watchdog](demos/persistence/watchdog/) — `persistence/watchdog`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/persistence/watchdog/)
- [打开 Linux Block I/O](demos/persistence/bio/) — `persistence/bio`；重复使用；首次见 Lect.23；[官方目录](https://jyywiki.cn/OS/demos/persistence/bio/)
- [OverlayFS](demos/persistence/overlay/) — `persistence/overlay`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/persistence/overlay/)
- [Symlink Game](demos/persistence/ggmaker/) — `persistence/ggmaker`；重复使用；首次见 Lect.24；[官方目录](https://jyywiki.cn/OS/demos/persistence/ggmaker/)

## Lect.26：文件系统实现

- [Logic Volume Manager](demos/persistence/lvm/) — `persistence/lvm`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/persistence/lvm/)
- [readfat](demos/persistence/readfat/) — `persistence/readfat`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/persistence/readfat/)
- [Debug File Systems](demos/persistence/ext4/) — `persistence/ext4`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/persistence/ext4/)
- [Crash Consistency Checker](demos/persistence/ccheck/) — `persistence/ccheck`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/persistence/ccheck/)

## Lect.27：数据库系统

- [Memory-mapped 数据结构](demos/persistence/mmds/) — `persistence/mmds`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/persistence/mmds/)

## Lect.28：计算机安全简介

- [Stack Buffer Overflow](demos/intro/stackoverflow/) — `intro/stackoverflow`；首次出现；[官方目录](https://jyywiki.cn/OS/demos/intro/stackoverflow/)

## Lect.29：虚拟机和容器

- 本讲未链接官方 `/OS/demos/` 课堂代码。

## Lect.30：课程总结

- 全课程代码总索引；对应上面所有 demo。
