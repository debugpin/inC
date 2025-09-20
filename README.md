# inC
![icon](inC-small.png)

## Smallest GNU GCC ELF executable
~16K

That’s normal, because gcc by default links your program against:
glibc runtime and startup files (crt1.o, crti.o, etc.)
dynamic loader info (if dynamically linked)
Standard C library code
So your minimal program isn’t really “just your code” — it carries a lot of runtime baggage.

### 1. Avoid the C standard library

By default, calling printf or even having main drags in glibc.
If you just want the process to return immediately, you can bypass main and libc entirely.

`gcc -nostdlib -static -s tiny.c -o tiny`

### 2. Use -nostdlib and -nostartfiles

-nostartfiles: skips crt0, crti, crtn (startup files)
-nostdlib: skips libc entirely

You’re fully responsible for defining _start.


### 3. Use assembler directly

If you drop gcc and go raw assembly:

`nasm -f elf64 tiny.s && ld -o tiny tiny.o`


### 4. Static vs Dynamic linking

Dynamic linking (default) → binary depends on loader and libc → bigger size.
Static linking (-static) → all code in one binary, but larger (megabytes).
Manual syscall only → smallest possible.

`strip --strip-all tiny`

Removes symbols, sections, padding → gets you close to the theoretical minimum ELF size.

## Size ballpark
int main(){} with gcc defaults → ~16 KB (like you saw).
_start with manual syscall (-nostdlib) → ~400–600 bytes.
Hand-written assembly with ld and strip → ~200–300 bytes ELF binary.

## Going even smaller
After stripping symbols, a lot of zeros remain, can these be removed as well

Exactly — you’ve noticed the big zero padding that remains in the ELF after strip. That’s because strip only removes symbol/debug sections, but leaves the ELF layout unchanged (alignment, padding, unused program headers, etc.).
