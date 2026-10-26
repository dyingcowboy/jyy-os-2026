# Thread-local Storage

C/C++ 支持声明 “线程局部” 的变量，在编译器的配合下，会生成 “每个线程独立” 的拷贝，从而避免维护全局 `map<tid,thread_local_storage>` 映射的开销。
