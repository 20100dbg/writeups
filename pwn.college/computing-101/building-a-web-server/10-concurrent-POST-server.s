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



wait_client:

    #accept
    mov rdi, 3     # fd
    mov rsi, 0     # sockaddr client
    mov rdx, 0     # addrlen
    mov rax, 43
    syscall
    #rax is client fd

    #fork
    mov rax, 57
    syscall

    #rax = 0 means we are in parent process
    cmp rax, 0
    je child_process

    #close socket
    mov rdi, 4    #fd
    mov rax, 3
    syscall

    jmp wait_client


child_process:
 
    #close (duplicate) listen socket
    mov rdi, 3    #fd
    mov rax, 3
    syscall

    #read client request
    mov rdi, 4
    mov rsi, rsp
    mov rdx, 512
    mov rax, 0
    syscall
    mov r13, rax

# r8 method addr
# r9 filename addr
# r10 tmp index
# r12 fd file to send back
# r13 total request len
# r14 body len

    mov r8, rsp
    mov r10, rsp

parse_method:
    mov al, byte ptr [r10]
    cmp al, ' '
    je parse_method_done
    add r10, 1
    jmp parse_method

parse_method_done:
    #add r10, 1
    mov byte ptr[r10], 0

    add r10, 1
    mov r9, r10


parse_filename:
    mov al, byte ptr [r10]
    cmp al, ' '
    je parse_filename_done
    add r10, 1
    jmp parse_filename

parse_filename_done:
    #add r10, 1
    mov byte ptr[r10], 0


    # check method
    cmp byte ptr [r8], 'G'
    jne request_POST
    jmp request_GET


request_POST:
    
    mov r10, 0


compute_length:
    add r10, 1
    cmp byte ptr [rsp+r10], '\r'
    jne compute_length

    add r10, 1
    cmp byte ptr [rsp+r10], '\n'
    jne compute_length

    add r10, 1
    cmp byte ptr [rsp+r10], '\r'
    jne compute_length

    add r10, 1
    cmp byte ptr [rsp+r10], '\n'
    jne compute_length

    jmp compute_length_done

compute_length_done:

    add r10, 1
    mov r14, r13
    sub r14, r10 # total - headers = body len


# O_WRONLY 1
# O_CREAT 64
# S_IRWXU 448
# S_IRWXG 56
# S_IRWXO 7
    
    #open file
    mov rdi, r9    # filename
    mov rsi, 65    # flags
    mov rdx, 511   # mode
    mov rax, 2
    syscall
    #rax is file fd
    mov r12, rax

    #write file
    mov rdi, r12    #fd file
    lea rsi, [rsp+r10]
    mov rdx, r14
    mov rax, 1
    syscall

    #close file
    mov rdi, r12    #fd file
    mov rax, 3
    syscall

    #write 200
    mov rdi, 4    #fd client
    lea rsi, [rip+response_200]
    mov rdx, 19
    mov rax, 1
    syscall
    

    jmp end_request


request_GET:

    #open file
    mov rdi, r9   # filename
    mov rsi, 0    # flags
    mov rax, 2
    syscall
    #rax is file fd
    mov r12, rax

    #read file
    mov rdi, r12    #fd file
    mov rsi, rsp
    mov rdx, 256
    mov rax, 0
    syscall
    mov r10, rax  #read len

    #close file
    mov rdi, r12    #fd file
    mov rax, 3
    syscall

    #write response to client
    mov rdi, 4
    lea rsi, [rip+response_200]
    mov rdx, 19
    mov rax, 1
    syscall

    #write file to client
    mov rdi, 4
    mov rsi, rsp
    mov rdx, r10
    mov rax, 1
    syscall


end_request:

    #close client socket
    mov rdi, 4    #fd
    mov rax, 3
    syscall

    #the concurrent server serves ONE request per client
    #jmp wait_client

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

method_GET:
    .string "GET"

method_POST:
    .string "POST"

