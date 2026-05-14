.intel_syntax noprefix
.globl _start

.section .text

_start:


    #socket
    mov rdi, 2     # AF_INET
    mov rsi, 1     # SOCK_STREAM
    mov rdx, 0
    mov rax, 41
    syscall

    #exit
    mov rdi, 0
    mov rax, 60
    syscall

.section .data
