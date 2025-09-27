# Insy Assembly

## No SEGV
```bash
nasm -f elf64 insy.s -o insy.o
ld -T insy.ld -o insy insy.o --gc-sections -e _start
strip --strip-all insy
```

### Checking the ELF and program headers
```bash
readelf -h insy        # ELF header: class, machine, entry point
readelf -l insy        # program headers: must include PT_LOAD mapping containing entry
readelf -S insy        # section headers (if present)
```

# Stripping
`strip --strip-all insy`

# Super stripping
`sstrip insy`
