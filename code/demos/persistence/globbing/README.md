# globbing

在 pstree 中，我们实现了目录树的遍历——我们几乎总是需要对底层文件系统 API 的封装，例如十分方便的 [glob()](https://www.gnu.org/software/libc/manual/html_node/Calling-Glob.html)。Globbing 也是 Agent 的 “四大技能”，Read, Write, Grep, Glob; 加上 Bash 就可以完成几乎所有的运维工作了。
