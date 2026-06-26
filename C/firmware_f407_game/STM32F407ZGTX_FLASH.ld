/**
  ******************************************************************************
  * @file      STM32F407ZGTX_FLASH.ld
  * @brief     STM32F407ZGTx 链接脚本
  * @details   FLASH: 1024KB (0x08000000 - 0x080FFFFF)
  *            RAM:   128KB (0x20000000 - 0x2001FFFF)
  *            CCM:   64KB  (0x10000000 - 0x1000FFFF)
  *            最小堆: 0x800, 最小栈: 0x800
  ******************************************************************************
  */

MEMORY
{
    FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 1024K
    RAM   (xrw) : ORIGIN = 0x20000000, LENGTH = 128K
    CCMRAM (rw) : ORIGIN = 0x10000000, LENGTH = 64K
}

/* 栈和堆配置 */
__StackSize = 0x800;
PROVIDE(__StackSize = __StackSize);

__HeapSize = 0x800;
PROVIDE(__HeapSize = __HeapSize);

SECTIONS
{
    /* 中断向量表 */
    .isr_vector :
    {
        . = ALIGN(4);
        KEEP(*(.isr_vector))
        . = ALIGN(4);
    } >FLASH

    /* 代码段 */
    .text :
    {
        . = ALIGN(4);
        *(.text)
        *(.text*)
        *(.glue_7)
        *(.glue_7t)
        *(.eh_frame)
        KEEP(*(.init))
        KEEP(*(.fini))
        . = ALIGN(4);
        _etext = .;
        PROVIDE(__etext = .);
    } >FLASH

    /* 只读数据段 */
    .rodata :
    {
        . = ALIGN(4);
        *(.rodata)
        *(.rodata*)
        . = ALIGN(4);
    } >FLASH

    /* ARM 异常处理表 */
    .ARM.extab :
    {
        *(.ARM.extab*)
        *(.gnu.linkonce.armextab.*)
    } >FLASH

    .ARM :
    {
        __exidx_start = .;
        *(.ARM.exidx*)
        __exidx_end = .;
    } >FLASH

    /* 预初始化数组 */
    .preinit_array :
    {
        PROVIDE_HIDDEN(__preinit_array_start = .);
        KEEP(*(.preinit_array*))
        PROVIDE_HIDDEN(__preinit_array_end = .);
    } >FLASH

    .init_array :
    {
        PROVIDE_HIDDEN(__init_array_start = .);
        KEEP(*(SORT(.init_array.*)))
        KEEP(*(.init_array*))
        PROVIDE_HIDDEN(__init_array_end = .);
    } >FLASH

    .fini_array :
    {
        PROVIDE_HIDDEN(__fini_array_start = .);
        KEEP(*(SORT(.fini_array.*)))
        KEEP(*(.fini_array*))
        PROVIDE_HIDDEN(__fini_array_end = .);
    } >FLASH

    /* 数据段 - 初始值存储在 Flash，运行时复制到 RAM */
    _sidata = .;
    PROVIDE(__data_load = .);

    .data : AT(_sidata)
    {
        . = ALIGN(4);
        _sdata = .;
        PROVIDE(__data_start = .);
        *(.data)
        *(.data*)
        . = ALIGN(4);
        _edata = .;
        PROVIDE(__data_end = .);
    } >RAM

    /* BSS 段 */
    .bss :
    {
        . = ALIGN(4);
        _sbss = .;
        PROVIDE(__bss_start = .);
        *(.bss)
        *(.bss*)
        *(COMMON)
        . = ALIGN(4);
        _ebss = .;
        PROVIDE(__bss_end = .);
    } >RAM

    /* 用户堆栈 */
    ._user_heap_stack :
    {
        . = ALIGN(8);
        PROVIDE(__HeapBase = .);
        . = . + __HeapSize;
        . = ALIGN(8);
        PROVIDE(__HeapLimit = .);
        . = . + __StackSize;
        . = ALIGN(8);
        PROVIDE(__StackLimit = .);
        PROVIDE(__StackTop = .);
    } >RAM

    /* CCM RAM 段 (预留，本游戏不使用 CCM) */
    .ccmram (NOLOAD) :
    {
        . = ALIGN(4);
        *(.ccmram)
        *(.ccmram*)
        . = ALIGN(4);
    } >CCMRAM

    /* 丢弃的段 */
    /DISCARD/ :
    {
        libc.a(*)
        libm.a(*)
        libgcc.a(*)
    }
}