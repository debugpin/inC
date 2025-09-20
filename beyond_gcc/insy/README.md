# Tiny Assembly
`nasm -f elf64 tinsy.s && ld -o tinsy tinsy.o`

# Tiny Linker
## SEGV
Cool — let’s fix this. If your minimal binary still segfaults the usual causes are:

wrong ELF program headers (no PT_LOAD mapping),

entrypoint placed outside mapped memory,

wrong architecture (32-bit vs 64-bit),

or the loader being told to use an interpreter (PT_INTERP) that doesn’t exist.

Below I give a practically tested minimal linker script + asm and a short checklist / debugging commands so you can verify what’s wrong. Follow these exactly (they’re for x86-64 Linux).

## No SEGV
```bash
nasm -f elf64 tinsy.s -o tinsy.o
ld -T tinsy.ld -o tinsy tinsy.o --gc-sections -e _start
strip --strip-all tinsy
```

### Checking the ELF and program headers
```bash
readelf -h tinsy        # ELF header: class, machine, entry point
readelf -l tinsy        # program headers: must include PT_LOAD mapping containing entry
readelf -S tinsy        # section headers (if present)
```

# Stripping
`strip --strip-all tinsy`

# Super stripping

