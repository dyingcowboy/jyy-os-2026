# JYY OS 2026 课堂代码

本目录归档了 [JYY《操作系统原理》2026 春季学期](https://jyywiki.cn/OS/2026/) Lect.1–30 讲义中链接的官方课堂 demo。代码于 2026-08-14 从 `https://jyywiki.cn/OS/demos/` 下载。

## 如何查找

- [LECTURES.md](LECTURES.md)：按 Lect.1–30 查找课堂代码，并标出重复使用的 demo 和首次出现的 lecture。
- [MANIFEST.tsv](MANIFEST.tsv)：每个 demo 一行，记录标题、对应 lecture、官方 URL、本地路径、文件数和字节数。
- [FILES.tsv](FILES.tsv)：每个下载文件一行，记录官方 URL、大小、SHA-256 和服务器 `Last-Modified`。
- [`demos/`](demos/)：官方目录结构的本地镜像，源码只保存一份。

Lect.30 是课程总结，其中重新列出了全课程 demo。为避免把所有代码都误标为“Lect.30 首次出现”，`LECTURES.md` 和 `MANIFEST.tsv` 使用 Lect.1–29 的实际出现位置，并把 Lect.30 标记为总索引。

## 如何构建

在 `code/` 目录下：

```sh
make            # 构建所有能在当前平台构建的 demo
make -j8        # 并行构建
make status     # 查看每个 demo 在本机的构建状态
make clean      # 清理全部构建产物
make concurrency/peterson   # 只构建某一个 demo
```

也可以进入任意 demo 目录单独 `make`，例如 `cd demos/concurrency/peterson && make`。

统一配置放在 [`mk/demo.mk`](mk/demo.mk)，各 demo 的 `Makefile` 用相对路径引入它，因此：

- 编译器统一取 `$(CC)` / `$(CXX)`，可用 `make CC=gcc-14` 覆盖；
- `TLIB_PATH` 默认指向 `demos/concurrency/thread-lib`，不再需要手动 export；
- 用到 pthread 的 demo 统一加 `-pthread`。

目录里有一部分 demo 依赖 Linux 专属接口、交叉工具链或外部程序（KVM、bpftrace、CUDA、
RISC-V/aarch64 交叉工具链、musl、qemu 等），在 macOS 上 `make` 会打印一行中文的
`[跳过]` 说明并以成功状态退出，`make status` 里标记为“跳过”；同一份 Makefile 在
满足条件的 Linux 环境下仍按原规则构建。

## 收录范围

收录讲义明确链接到 `/OS/demos/` 的课堂演示，包括源码、Makefile、README、脚本、示例资源和目录中已有的少量构建产物。未收录以下内容：

- 课程实验 M1–M9 的 GitLab 分支；它们是作业骨架，不是按 lecture 组织的课堂 demo。
- 讲义引用的第三方通用项目、论文和网页，例如 Linux、`llm.c` 或上游 OpenSBI 仓库。
- 讲义正文中的短代码片段；这些片段已经保留在相应的 `lectN.md` 中。

课程首页标注为 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)。部分 demo 含有第三方代码或独立许可证，使用时应以各目录内的许可证和上游项目条款为准。
