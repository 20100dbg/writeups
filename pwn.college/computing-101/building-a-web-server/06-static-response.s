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

    #bind
    mov rdi, 3                # fd
    lea rsi, [rip+sockaddr]   # sockaddr
    mov rdx, 16               # addrlen
    mov rax, 49
    syscall

    #listen
    mov rdi, 3    # fd
    mov rsi, 0    # backlog
    mov rax, 50
    syscall

    #accept
    mov rdi, 3     # fd
    mov rsi, 0     # sockaddr client
    mov rdx, 0     # addrlen
    mov rax, 43
    syscall
    #rax is client fd

    #read
    mov rdi, 4
    mov rsi, rsp
    mov rdx, 256
    mov rax, 0
    syscall

    #write
    mov rdi, 4
    lea rsi, [rip+response_200]
    mov rdx, 19
    mov rax, 1
    syscall

    #close
    mov rdi, 4    #fd
    mov rax, 3
    syscall

    #exit
    mov rdi, 0
    mov rax, 60
    syscall

.section .data

sockaddr:
    .2byte 2       # AF_INET
    .2byte 0x5000  # port
    .4byte 0       # addr
    .8byte 0       # padding

response_200:
    .string "HTTP/1.0 200 OK\r\n\r\n"

