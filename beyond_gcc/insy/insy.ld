ENTRY(_start)

SECTIONS {
  . = SIZEOF_HEADERS;   /* place code right after ELF header */
  .text : { *(.text) }
}
