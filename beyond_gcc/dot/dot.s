global _start
section .text
_start:
    ; write(1, msg, 1)
    mov     rax, 1          ; syscall: write
    mov     rdi, 1          ; fd = 1 (stdout)
    lea     rsi, [rel msg]  ; buf = &msg
    mov     rdx, 1          ; count = 1
    syscall

    ; exit(0)
    mov     rax, 60         ; syscall: exit
    xor     rdi, rdi        ; status = 0
    syscall

section .rodata
msg: db ".", 0
