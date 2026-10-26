# JYY OS 2026 课堂代码

本目录归档了 [JYY《操作系统原理》2026 春季学期](https://jyywiki.cn/OS/2026/) Lect.1–30 讲义中链接的官方课堂 demo。代码于 2026-08-14 从 `https://jyywiki.cn/OS/demos/` 下载。

## 如何查找

- [LECTURES.md](LECTURES.md)：按 Lect.1–30 查找课堂代码，并标出重复使用的 demo 和首次出现的 lecture。
- [MANIFEST.tsv](MANIFEST.tsv)：每个 demo 一行，记录标题、对应 lecture、官方 URL、本地路径、文件数和字节数。
- [FILES.tsv](FILES.tsv)：每个下载文件一行，记录官方 URL、大小、SHA-256 和服务器 `Last-Modified`。
- [`demos/`](demos/)：官方目录结构的本地镜像，源码只保存一份。

Lect.30 是课程总结，其中重新列出了全课程 demo。为避免把所有代码都误标为“Lect.30 首次出现”，`LECTURES.md` 和 `MANIFEST.tsv` 使用 Lect.1–29 的实际出现位置，并把 Lect.30 标记为总索引。

## 收录范围

收录讲义明确链接到 `/OS/demos/` 的课堂演示，包括源码、Makefile、README、脚本、示例资源和目录中已有的少量构建产物。未收录以下内容：

- 课程实验 M1–M9 的 GitLab 分支；它们是作业骨架，不是按 lecture 组织的课堂 demo。
- 讲义引用的第三方通用项目、论文和网页，例如 Linux、`llm.c` 或上游 OpenSBI 仓库。
- 讲义正文中的短代码片段；这些片段已经保留在相应的 `lectN.md` 中。

课程首页标注为 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)。部分 demo 含有第三方代码或独立许可证，使用时应以各目录内的许可证和上游项目条款为准。
