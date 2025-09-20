# Smallest GCC

`gcc -o smallest_gcc smallest_gcc.c`

## Smaller still

`gcc -nostdlib -static -s smaller.c -o smaller`

### C Runtime

| File name | Description of its purpose                                                     |
| --------- | ------------------------------------------------------------------------------ |
| crt1.o    | Defines _start, sets up runtime, calls __libc_start_main(main, …).             |
| crti.o    | Provides prologue code for .init/.fini sections (initialization/finalization). |
| crtn.o    | Provides epilogue code for .init/.fini.                                        |

Together, they’re the scaffolding around your main. Without them, you’re in charge of _start and syscall exit.

If you compile with -nostartfiles or -nostdlib, you skip these and have to provide _start yourself, as shown above.

## Compiled and Assembled but not Linked
Perfect — you’ve asked for a **line-by-line breakdown** of the assembly output from compiling a minimal C program with GCC. Let’s go through this carefully.

This looks like the assembly produced by `gcc -S -fno-asynchronous-unwind-tables -fno-stack-protector smallest_gcc.c` or something close.

---

## 🔹 High-level overview

* The file is in **AT\&T syntax** (default for GCC/`as`).
* It defines a single function `main` that does almost nothing.
* GCC also emits metadata for debugging, stack unwinding, security features, and ELF notes.

---

## 🔹 Detailed breakdown

```asm
	.file	"smallest_gcc.c"
```

📄 Assembler directive: marks the original source file name.
Not machine code, just metadata.

---

```asm
	.text
```

📦 Switch to the `.text` section (where executable code lives).

---

```asm
	.globl	main
	.type	main, @function
```

* `main` should be globally visible (so linker can find it).
* Its symbol type is a function.

---

```asm
main:
.LFB0:
	.cfi_startproc
```

* `main:` is the function label.
* `.LFB0` is a local label used internally (function begin).
* `.cfi_startproc` begins **Call Frame Information** (used for stack unwinding in debugging/exception handling).

---

```asm
	endbr64
```

🔒 This is an instruction for Intel CET (Control-flow Enforcement Technology).
It marks a valid target for indirect branches (helps mitigate ROP/JOP attacks).
On older CPUs, it’s just a NOP.

---

```asm
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
```

Standard function **prologue**:

* Save old base pointer.
* Set up new stack frame (`rbp = rsp`).
* The `.cfi_*` directives describe this to the unwinder/debugger.

---

```asm
	nop
```

A no-operation instruction. Likely alignment filler.

---

```asm
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
```

Function **epilogue**:

* Restore old base pointer.
* Return to caller.
* `.cfi_def_cfa` updates unwind info (stack pointer restored).

So the body of `main` literally does *nothing*.

---

```asm
	.cfi_endproc
.LFE0:
```

Marks end of function and call frame info.

---

```asm
	.size	main, .-main
```

Tell assembler the size of `main` is the difference between current location and `main` label.

---

```asm
	.ident	"GCC: (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0"
```

Compiler identification string. Stored in ELF `.comment` section.
Not executable code.

---

```asm
	.section	.note.GNU-stack,"",@progbits
```

Marks that this object doesn’t need an executable stack.
Linux uses this for security (non-executable stack protection).

---

```asm
	.section	.note.gnu.property,"a"
	.align 8
	.long	1f - 0f
	.long	4f - 1f
	.long	5
0:
	.string	"GNU"
1:
	.align 8
	.long	0xc0000002
	.long	3f - 2f
2:
	.long	0x3
3:
	.align 8
4:
```

This is an ELF **note section** containing “GNU property notes” (used by glibc/loader).

Breaking it down:

* `.note.gnu.property` is an ELF note section.
* `"GNU"` string identifies vendor.
* `0xc0000002` means *GNU\_PROPERTY\_X86\_FEATURE\_1\_AND* → encodes required CPU features.
* Value `0x3` means CET (control-flow enforcement) and IBT (indirect branch tracking) are enabled.

These notes help the dynamic loader know what CPU/security features are expected.

---

## 🔹 Summary

So your file contains:

1. **Function `main`**: just prologue, epilogue, no body.
2. **Unwinding info** (`.cfi_*`): for debugging and stack traces.
3. **Security instruction**: `endbr64` for CET.
4. **Metadata**:

   * `.ident` (compiler info)
   * `.note.GNU-stack` (stack executable flag)
   * `.note.gnu.property` (CET / feature notes)

Only the `push`, `mov`, `pop`, `ret`, `endbr64`, and `nop` are real instructions executed at runtime.
Everything else is ELF bookkeeping.

---

👉 Do you want me to also show you what the **binary actually looks like in hex** (the machine code bytes only, stripped of directives), so you can compare how much of this assembly actually turns into runtime instructions?
