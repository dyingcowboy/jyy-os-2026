# 使用互斥锁实现计算图

为每一条边分配一把互斥锁——对于 u->v 的一条边，通过在 main 函数 acquire(lock of u -> v)，u release -> v acquire 来实现 happens-before。注意虽然这个程序可以正常运行，但这是 pthread mutex 不允许的 undefined behavior。
