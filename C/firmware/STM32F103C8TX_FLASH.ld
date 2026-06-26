/**
  ******************************************************************************
  * @file      STM32F103C8TX_FLASH.ld
  * @brief     STM32F103C8Tx 链接脚本
  * @details   FLASH: 64KB (0x08000000 - 0x0800FFFF)
  *            RAM:   20KB (0x20000000 - 0x20004FFF)
  *            最小堆: 0x200, 最小栈: 0x400
  ******************************************************************************
  */

/* ======================== 内存布局 ======================== */

MEMORY
{
    FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 64K
    RAM   (xrw) : ORIGIN = 0x20000000, LENGTH = 20K
}

/* ======================== 栈和堆配置 ======================== */

/* 最小栈大小 (1KB) */
__StackSize = 0x400;
PROVIDE(__StackSize = __StackSize);

/* 最小堆大小 (512B) */
__HeapSize = 0x200;
PROVIDE(__HeapSize = __HeapSize);

/* ======================== Section 定义 ======================== */

SECTIONS
{
    /* 中断向量表 - 位于 Flash 起始地址 */
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

    /* 初始化数组 */
    .init_array :
    {
        PROVIDE_HIDDEN(__init_array_start = .);
        KEEP(*(SORT(.init_array.*)))
        KEEP(*(.init_array*))
        PROVIDE_HIDDEN(__init_array_end = .);
    } >FLASH

    /* 结束数组 */
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

    /* BSS 段 - 未初始化数据 */
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

    /* 丢弃的段 */
    /DISCARD/ :
    {
        libc.a(*)
        libm.a(*)
        libgcc.a(*)
    }
}