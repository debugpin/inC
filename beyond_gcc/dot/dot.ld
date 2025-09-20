OUTPUT_FORMAT("elf64-x86-64")
ENTRY(_start)

PHDRS {
  text PT_LOAD FLAGS(5); /* PF_R | PF_X */
}

SECTIONS
{
  /* Start after ELF headers */
  . = 0x400000 + SIZEOF_HEADERS;

  .text : {
    *(.text)
    *(.rodata)   /* include string inside same load segment */
  } :text

  /DISCARD/ : { *(.note*) *(.comment) *(.eh_frame*) }
}
