# Crash Consistency Checker

一个 user-space 的 strace-based crash consistency checker。追踪一次程序所有对数据文件的写入，包括 fsync 系列的系统调用，生成一系列的 trace，并使用 LLM 判定是否存在数据不一致等。
