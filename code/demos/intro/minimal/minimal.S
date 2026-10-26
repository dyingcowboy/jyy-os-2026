#include <sys/syscall.h>

    .text
    .globl _start

_start:
    mov     $SYS_write, %rax
    mov     $1, %rdi
    lea     addr1(%rip), %rsi
    mov     $(addr2-addr1), %rdx
    syscall

    mov     $SYS_exit, %rax
    mov     $1, %rdi
    syscall


addr1:
    .ascii "\033[01;31mHello, OS World\033[0m\n"
addr2:
