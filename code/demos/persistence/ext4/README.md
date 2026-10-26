# Debug File Systems

debugfs 工具使我们能在用户态调试文件系统——这也给了我们 “可视化” 一个目录的机会，我们可以递归地 dump 出一个目录的 raw data structure，看到文件系统的 “内部”，例如符号链接是如何存储的，并且用合适的工具渲染成直接可视化的 diagram。
