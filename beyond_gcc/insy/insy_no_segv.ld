/* insy.ld - minimal but correct: creates a PT_LOAD for .text and places code
   just after the ELF headers so load addresses line up. Works on x86-64. */

OUTPUT_FORMAT("elf64-x86-64")
ENTRY(_start)

PHDRS {
  text PT_LOAD FLAGS(5); /* PF_R | PF_X */
}

SECTIONS
{
  /* Put the section right after ELF + program headers */
  . = 0x400000 + SIZEOF_HEADERS;

  .text : {
    *(.text)
  } :text

  /* discard some unneeded sections */
  /DISCARD/ : { *(.note*) *(.comment) *(.eh_frame*) }
}
