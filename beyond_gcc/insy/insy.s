global _start

section .text
_start:
    mov rax, 60     ; syscall number for exit
    xor rdi, rdi    ; exit code 0
    syscall
