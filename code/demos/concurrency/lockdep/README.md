# lockdep

通过 `LD_PRELOAD` 拦截 `pthread_mutex_lock` / `pthread_mutex_unlock`，在运行时构建锁的依赖图（邻接矩阵）来检测潜在的 ABBA 死锁：每次加锁时记录 “已持有锁 → 新获取锁” 的有向边，加边前检查是否形成环，发现环则报告潜在死锁。
