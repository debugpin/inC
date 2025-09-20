void _start() {
    __asm__("mov $60, %rax\n"  // syscall: exit
            "xor %rdi, %rdi\n" // exit code 0
            "syscall");
}
