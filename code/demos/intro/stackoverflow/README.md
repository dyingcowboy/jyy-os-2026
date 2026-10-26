# Stack Buffer Overflow

当输入的长度超过缓冲区大小时，vulnerable.c 的行为就变得危险。如果没有各类保护机制 (Stack Protector, ASLR 等)，这个程序就完全可以被利用执行任意代码。
