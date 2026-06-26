/**
  ******************************************************************************
  * @file      startup_stm32f407zgtx.s
  * @brief     STM32F407ZGTx 启动文件 (ARM GCC)
  * @note      Flash: 1MB, RAM: 192KB (128KB + 64KB CCM)
  ******************************************************************************
  */

  .syntax unified
  .cpu cortex-m4
  .fpu softvfp
  .thumb

.global  g_pfnVectors
.global  Default_Handler

/* start address for the initialization values of the .data section. */
.word  _sidata
/* start address for the .data section. */
.word  _sdata
/* end address for the .data section. */
.word  _edata
/* start address for the .bss section. */
.word  _sbss
/* end address for the .bss section. */
.word  _ebss

/* stack top */
.word  __StackTop

/**
 * @brief  This is the code that gets called when the processor first
 *          starts execution following a reset event.
 */
  .section  .text.Reset_Handler
  .weak  Reset_Handler
  .type  Reset_Handler, %function
Reset_Handler:
  ldr   sp, =__StackTop

/* Copy the data segment initializers from flash to SRAM */
  movs  r1, #0
  b  LoopCopyDataInit

CopyDataInit:
  ldr  r3, =_sidata
  ldr  r3, [r3, r1]
  str  r3, [r0, r1]
  adds  r1, r1, #4

LoopCopyDataInit:
  ldr  r0, =_sdata
  ldr  r3, =_edata
  adds  r2, r0, r1
  cmp  r2, r3
  bcc  CopyDataInit
  ldr  r2, =_sbss
  b  LoopFillZerobss

/* Zero fill the bss segment. */
FillZerobss:
  movs  r3, #0
  str  r3, [r2], #4

LoopFillZerobss:
  ldr  r3, = _ebss
  cmp  r2, r3
  bcc  FillZerobss

/* Call the clock system initialization function. */
  bl  SystemInit
/* Call static constructors */
  bl  __libc_init_array
/* Call the application's entry point. */
  bl  main
  bx  lr
.size  Reset_Handler, .-Reset_Handler

/**
 * @brief  This is the code that gets called when the processor receives an
 *         unexpected interrupt.
 */
  .section  .text.Default_Handler,"ax",%progbits
Default_Handler:
Infinite_Loop:
  b  Infinite_Loop
  .size  Default_Handler, .-Default_Handler


/* Macro to define weak alias for each exception handler */
  .macro  def_weak_alias  name
  .weak  \name
  .thumb_set \name, Default_Handler
  .endm

/* Exception handlers */
def_weak_alias  NMI_Handler
def_weak_alias  HardFault_Handler
def_weak_alias  MemManage_Handler
def_weak_alias  BusFault_Handler
def_weak_alias  UsageFault_Handler
def_weak_alias  SVC_Handler
def_weak_alias  DebugMon_Handler
def_weak_alias  PendSV_Handler
def_weak_alias  SysTick_Handler

/* IRQ handlers */
def_weak_alias  WWDG_IRQHandler
def_weak_alias  PVD_IRQHandler
def_weak_alias  TAMP_STAMP_IRQHandler
def_weak_alias  RTC_WKUP_IRQHandler
def_weak_alias  FLASH_IRQHandler
def_weak_alias  RCC_IRQHandler
def_weak_alias  EXTI0_IRQHandler
def_weak_alias  EXTI1_IRQHandler
def_weak_alias  EXTI2_IRQHandler
def_weak_alias  EXTI3_IRQHandler
def_weak_alias  EXTI4_IRQHandler
def_weak_alias  DMA1_Stream0_IRQHandler
def_weak_alias  DMA1_Stream1_IRQHandler
def_weak_alias  DMA1_Stream2_IRQHandler
def_weak_alias  DMA1_Stream3_IRQHandler
def_weak_alias  DMA1_Stream4_IRQHandler
def_weak_alias  DMA1_Stream5_IRQHandler
def_weak_alias  DMA1_Stream6_IRQHandler
def_weak_alias  ADC_IRQHandler
def_weak_alias  CAN1_TX_IRQHandler
def_weak_alias  CAN1_RX0_IRQHandler
def_weak_alias  CAN1_RX1_IRQHandler
def_weak_alias  CAN1_SCE_IRQHandler
def_weak_alias  EXTI9_5_IRQHandler
def_weak_alias  TIM1_BRK_TIM9_IRQHandler
def_weak_alias  TIM1_UP_TIM10_IRQHandler
def_weak_alias  TIM1_TRG_COM_TIM11_IRQHandler
def_weak_alias  TIM1_CC_IRQHandler
def_weak_alias  TIM2_IRQHandler
def_weak_alias  TIM3_IRQHandler
def_weak_alias  TIM4_IRQHandler
def_weak_alias  I2C1_EV_IRQHandler
def_weak_alias  I2C1_ER_IRQHandler
def_weak_alias  I2C2_EV_IRQHandler
def_weak_alias  I2C2_ER_IRQHandler
def_weak_alias  SPI1_IRQHandler
def_weak_alias  SPI2_IRQHandler
def_weak_alias  USART1_IRQHandler
def_weak_alias  USART2_IRQHandler
def_weak_alias  USART3_IRQHandler
def_weak_alias  EXTI15_10_IRQHandler
def_weak_alias  RTC_Alarm_IRQHandler
def_weak_alias  OTG_FS_WKUP_IRQHandler
def_weak_alias  TIM8_BRK_TIM12_IRQHandler
def_weak_alias  TIM8_UP_TIM13_IRQHandler
def_weak_alias  TIM8_TRG_COM_TIM14_IRQHandler
def_weak_alias  TIM8_CC_IRQHandler
def_weak_alias  DMA1_Stream7_IRQHandler
def_weak_alias  FSMC_IRQHandler
def_weak_alias  SDIO_IRQHandler
def_weak_alias  TIM5_IRQHandler
def_weak_alias  SPI3_IRQHandler
def_weak_alias  UART4_IRQHandler
def_weak_alias  UART5_IRQHandler
def_weak_alias  TIM6_DAC_IRQHandler
def_weak_alias  TIM7_IRQHandler
def_weak_alias  DMA2_Stream0_IRQHandler
def_weak_alias  DMA2_Stream1_IRQHandler
def_weak_alias  DMA2_Stream2_IRQHandler
def_weak_alias  DMA2_Stream3_IRQHandler
def_weak_alias  DMA2_Stream4_IRQHandler
def_weak_alias  ETH_IRQHandler
def_weak_alias  ETH_WKUP_IRQHandler
def_weak_alias  CAN2_TX_IRQHandler
def_weak_alias  CAN2_RX0_IRQHandler
def_weak_alias  CAN2_RX1_IRQHandler
def_weak_alias  CAN2_SCE_IRQHandler
def_weak_alias  OTG_FS_IRQHandler
def_weak_alias  DMA2_Stream5_IRQHandler
def_weak_alias  DMA2_Stream6_IRQHandler
def_weak_alias  DMA2_Stream7_IRQHandler
def_weak_alias  USART6_IRQHandler
def_weak_alias  I2C3_EV_IRQHandler
def_weak_alias  I2C3_ER_IRQHandler
def_weak_alias  OTG_HS_EP1_OUT_IRQHandler
def_weak_alias  OTG_HS_EP1_IN_IRQHandler
def_weak_alias  OTG_HS_WKUP_IRQHandler
def_weak_alias  OTG_HS_IRQHandler
def_weak_alias  DCMI_IRQHandler
def_weak_alias  HASH_RNG_IRQHandler
def_weak_alias  FPU_IRQHandler

  .section  .isr_vector,"a",%progbits
  .type  g_pfnVectors, %object
  .size  g_pfnVectors, .-g_pfnVectors

g_pfnVectors:
  .word  __StackTop
  .word  Reset_Handler
  .word  NMI_Handler
  .word  HardFault_Handler
  .word  MemManage_Handler
  .word  BusFault_Handler
  .word  UsageFault_Handler
  .word  0
  .word  0
  .word  0
  .word  0
  .word  SVC_Handler
  .word  DebugMon_Handler
  .word  0
  .word  PendSV_Handler
  .word  SysTick_Handler

  /* External Interrupts */
  .word  WWDG_IRQHandler
  .word  PVD_IRQHandler
  .word  TAMP_STAMP_IRQHandler
  .word  RTC_WKUP_IRQHandler
  .word  FLASH_IRQHandler
  .word  RCC_IRQHandler
  .word  EXTI0_IRQHandler
  .word  EXTI1_IRQHandler
  .word  EXTI2_IRQHandler
  .word  EXTI3_IRQHandler
  .word  EXTI4_IRQHandler
  .word  DMA1_Stream0_IRQHandler
  .word  DMA1_Stream1_IRQHandler
  .word  DMA1_Stream2_IRQHandler
  .word  DMA1_Stream3_IRQHandler
  .word  DMA1_Stream4_IRQHandler
  .word  DMA1_Stream5_IRQHandler
  .word  DMA1_Stream6_IRQHandler
  .word  ADC_IRQHandler
  .word  CAN1_TX_IRQHandler
  .word  CAN1_RX0_IRQHandler
  .word  CAN1_RX1_IRQHandler
  .word  CAN1_SCE_IRQHandler
  .word  EXTI9_5_IRQHandler
  .word  TIM1_BRK_TIM9_IRQHandler
  .word  TIM1_UP_TIM10_IRQHandler
  .word  TIM1_TRG_COM_TIM11_IRQHandler
  .word  TIM1_CC_IRQHandler
  .word  TIM2_IRQHandler
  .word  TIM3_IRQHandler
  .word  TIM4_IRQHandler
  .word  I2C1_EV_IRQHandler
  .word  I2C1_ER_IRQHandler
  .word  I2C2_EV_IRQHandler
  .word  I2C2_ER_IRQHandler
  .word  SPI1_IRQHandler
  .word  SPI2_IRQHandler
  .word  USART1_IRQHandler
  .word  USART2_IRQHandler
  .word  USART3_IRQHandler
  .word  EXTI15_10_IRQHandler
  .word  RTC_Alarm_IRQHandler
  .word  OTG_FS_WKUP_IRQHandler
  .word  TIM8_BRK_TIM12_IRQHandler
  .word  TIM8_UP_TIM13_IRQHandler
  .word  TIM8_TRG_COM_TIM14_IRQHandler
  .word  TIM8_CC_IRQHandler
  .word  DMA1_Stream7_IRQHandler
  .word  FSMC_IRQHandler
  .word  SDIO_IRQHandler
  .word  TIM5_IRQHandler
  .word  SPI3_IRQHandler
  .word  UART4_IRQHandler
  .word  UART5_IRQHandler
  .word  TIM6_DAC_IRQHandler
  .word  TIM7_IRQHandler
  .word  DMA2_Stream0_IRQHandler
  .word  DMA2_Stream1_IRQHandler
  .word  DMA2_Stream2_IRQHandler
  .word  DMA2_Stream3_IRQHandler
  .word  DMA2_Stream4_IRQHandler
  .word  ETH_IRQHandler
  .word  ETH_WKUP_IRQHandler
  .word  CAN2_TX_IRQHandler
  .word  CAN2_RX0_IRQHandler
  .word  CAN2_RX1_IRQHandler
  .word  CAN2_SCE_IRQHandler
  .word  OTG_FS_IRQHandler
  .word  DMA2_Stream5_IRQHandler
  .word  DMA2_Stream6_IRQHandler
  .word  DMA2_Stream7_IRQHandler
  .word  USART6_IRQHandler
  .word  I2C3_EV_IRQHandler
  .word  I2C3_ER_IRQHandler
  .word  OTG_HS_EP1_OUT_IRQHandler
  .word  OTG_HS_EP1_IN_IRQHandler
  .word  OTG_HS_WKUP_IRQHandler
  .word  OTG_HS_IRQHandler
  .word  DCMI_IRQHandler
  .word  HASH_RNG_IRQHandler
  .word  FPU_IRQHandler