.intel_syntax noprefix
.globl _start

.section .text

_start:

    #exit
    mov rdi, 0
    mov rax, 60
    syscall

.section .data
