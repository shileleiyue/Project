/**
  ******************************************************************************
  * @file      startup_stm32f103c8tx.s
  * @brief     STM32F103C8Tx 启动文件 - GCC 汇编
  * @details   STM32F103C8Tx (Medium Density) 中断向量表 + 启动流程
  *            - 初始化栈指针
  *            - 调用 SystemInit
  *            - 复制 .data 段到 RAM
  *            - 清零 .bss 段
  *            - 调用 main 进入主循环
  ******************************************************************************
  */

.syntax  unified
.cpu     cortex-m3
.fpu     softvfp
.thumb

/* ======================== 全局符号声明 ======================== */
.global g_pfnVectors
.global Default_Handler

/* 启动入口 */
.global Reset_Handler

/* 外部引用 - 由链接脚本或 C 代码提供 */
.extern __StackTop
.extern SystemInit
.extern main
.extern __data_start
.extern __data_end
.extern __data_load
.extern __bss_start
.extern __bss_end
.extern __HeapBase
.extern __HeapLimit
.extern __StackLimit

/* ======================== 中断向量表 ======================== */
.section  .isr_vector, "a", %progbits
.type     g_pfnVectors, %object
.size     g_pfnVectors, .-g_pfnVectors

g_pfnVectors:
    .word  __StackTop
    .word  Reset_Handler
    .word  NMI_Handler
    .word  HardFault_Handler
    .word  MemManage_Handler
    .word  BusFault_Handler
    .word  UsageFault_Handler
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  SVC_Handler
    .word  DebugMon_Handler
    .word  0                         /* 保留 */
    .word  PendSV_Handler
    .word  SysTick_Handler

    /* 外部中断向量 */
    .word  WWDG_IRQHandler           /* 窗口看门狗 */
    .word  PVD_IRQHandler            /* PVD 检测 */
    .word  TAMPER_IRQHandler         /* TAMPER */
    .word  RTC_IRQHandler            /* RTC */
    .word  FLASH_IRQHandler          /* Flash */
    .word  RCC_IRQHandler            /* RCC */
    .word  EXTI0_IRQHandler          /* EXTI Line 0 */
    .word  EXTI1_IRQHandler          /* EXTI Line 1 */
    .word  EXTI2_IRQHandler          /* EXTI Line 2 */
    .word  EXTI3_IRQHandler          /* EXTI Line 3 */
    .word  EXTI4_IRQHandler          /* EXTI Line 4 */
    .word  DMA1_Channel1_IRQHandler   /* DMA1 Channel 1 */
    .word  DMA1_Channel2_IRQHandler   /* DMA1 Channel 2 */
    .word  DMA1_Channel3_IRQHandler   /* DMA1 Channel 3 */
    .word  DMA1_Channel4_IRQHandler   /* DMA1 Channel 4 */
    .word  DMA1_Channel5_IRQHandler   /* DMA1 Channel 5 */
    .word  DMA1_Channel6_IRQHandler   /* DMA1 Channel 6 */
    .word  DMA1_Channel7_IRQHandler   /* DMA1 Channel 7 */
    .word  ADC1_2_IRQHandler         /* ADC1 & ADC2 */
    .word  USB_HP_CAN1_TX_IRQHandler  /* USB High Priority / CAN1 TX */
    .word  USB_LP_CAN1_RX0_IRQHandler /* USB Low Priority / CAN1 RX0 */
    .word  CAN1_RX1_IRQHandler       /* CAN1 RX1 */
    .word  CAN1_SCE_IRQHandler       /* CAN1 SCE */
    .word  EXTI9_5_IRQHandler        /* EXTI Line 9..5 */
    .word  TIM1_BRK_IRQHandler       /* TIM1 Break */
    .word  TIM1_UP_IRQHandler        /* TIM1 Update */
    .word  TIM1_TRG_COM_IRQHandler   /* TIM1 Trigger / Commutation */
    .word  TIM1_CC_IRQHandler        /* TIM1 Capture Compare */
    .word  TIM2_IRQHandler           /* TIM2 */
    .word  TIM3_IRQHandler           /* TIM3 */
    .word  TIM4_IRQHandler           /* TIM4 */
    .word  I2C1_EV_IRQHandler        /* I2C1 Event */
    .word  I2C1_ER_IRQHandler        /* I2C1 Error */
    .word  I2C2_EV_IRQHandler        /* I2C2 Event */
    .word  I2C2_ER_IRQHandler        /* I2C2 Error */
    .word  SPI1_IRQHandler           /* SPI1 */
    .word  SPI2_IRQHandler           /* SPI2 */
    .word  USART1_IRQHandler         /* USART1 */
    .word  USART2_IRQHandler         /* USART2 */
    .word  USART3_IRQHandler         /* USART3 */
    .word  EXTI15_10_IRQHandler      /* EXTI Line 15..10 */
    .word  RTC_Alarm_IRQHandler      /* RTC Alarm */
    .word  USBWakeUp_IRQHandler      /* USB Wakeup */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */
    .word  0                         /* 保留 */

/* ======================== Reset_Handler ======================== */
.section  .text.Reset_Handler, "ax", %progbits
.type     Reset_Handler, %function
.weak     Reset_Handler

Reset_Handler:
    /* 设置栈指针 */
    ldr   r0, =__StackTop
    msr   msp, r0

    /* 调用 SystemInit 初始化系统时钟 */
    bl    SystemInit

    /* 复制 .data 段从 Flash 到 RAM */
    ldr   r0, =__data_load
    ldr   r1, =__data_start
    ldr   r2, =__data_end

    subs  r3, r0, r1
    beq   .L_clear_bss

.L_copy_data:
    subs  r3, r2, r1
    ble   .L_clear_bss
    ldrb  r4, [r0]
    strb  r4, [r1]
    adds  r0, #1
    adds  r1, #1
    b     .L_copy_data

    /* 清零 .bss 段 */
.L_clear_bss:
    ldr   r0, =__bss_start
    ldr   r1, =__bss_end
    movs  r2, #0

.L_bss_loop:
    subs  r3, r1, r0
    ble   .L_call_main
    str   r2, [r0]
    adds  r0, #4
    b     .L_bss_loop

    /* 跳转到 main */
.L_call_main:
    bl    main

    /* main 返回后的死循环 */
.L_loop:
    b     .L_loop

.size  Reset_Handler, .-Reset_Handler

/* ======================== Default_Handler ======================== */
.section  .text.Default_Handler, "ax", %progbits
.type     Default_Handler, %function

Default_Handler:
    b     Default_Handler

.size  Default_Handler, .-Default_Handler

/* ======================== Weak 别名定义 ======================== */

/* 核心异常处理程序 */
.weak   NMI_Handler
.thumb_set NMI_Handler, Default_Handler

.weak   HardFault_Handler
.thumb_set HardFault_Handler, Default_Handler

.weak   MemManage_Handler
.thumb_set MemManage_Handler, Default_Handler

.weak   BusFault_Handler
.thumb_set BusFault_Handler, Default_Handler

.weak   UsageFault_Handler
.thumb_set UsageFault_Handler, Default_Handler

.weak   SVC_Handler
.thumb_set SVC_Handler, Default_Handler

.weak   DebugMon_Handler
.thumb_set DebugMon_Handler, Default_Handler

.weak   PendSV_Handler
.thumb_set PendSV_Handler, Default_Handler

.weak   SysTick_Handler
.thumb_set SysTick_Handler, Default_Handler

/* 外部中断处理程序 */
.weak   WWDG_IRQHandler
.thumb_set WWDG_IRQHandler, Default_Handler

.weak   PVD_IRQHandler
.thumb_set PVD_IRQHandler, Default_Handler

.weak   TAMPER_IRQHandler
.thumb_set TAMPER_IRQHandler, Default_Handler

.weak   RTC_IRQHandler
.thumb_set RTC_IRQHandler, Default_Handler

.weak   FLASH_IRQHandler
.thumb_set FLASH_IRQHandler, Default_Handler

.weak   RCC_IRQHandler
.thumb_set RCC_IRQHandler, Default_Handler

.weak   EXTI0_IRQHandler
.thumb_set EXTI0_IRQHandler, Default_Handler

.weak   EXTI1_IRQHandler
.thumb_set EXTI1_IRQHandler, Default_Handler

.weak   EXTI2_IRQHandler
.thumb_set EXTI2_IRQHandler, Default_Handler

.weak   EXTI3_IRQHandler
.thumb_set EXTI3_IRQHandler, Default_Handler

.weak   EXTI4_IRQHandler
.thumb_set EXTI4_IRQHandler, Default_Handler

.weak   DMA1_Channel1_IRQHandler
.thumb_set DMA1_Channel1_IRQHandler, Default_Handler

.weak   DMA1_Channel2_IRQHandler
.thumb_set DMA1_Channel2_IRQHandler, Default_Handler

.weak   DMA1_Channel3_IRQHandler
.thumb_set DMA1_Channel3_IRQHandler, Default_Handler

.weak   DMA1_Channel4_IRQHandler
.thumb_set DMA1_Channel4_IRQHandler, Default_Handler

.weak   DMA1_Channel5_IRQHandler
.thumb_set DMA1_Channel5_IRQHandler, Default_Handler

.weak   DMA1_Channel6_IRQHandler
.thumb_set DMA1_Channel6_IRQHandler, Default_Handler

.weak   DMA1_Channel7_IRQHandler
.thumb_set DMA1_Channel7_IRQHandler, Default_Handler

.weak   ADC1_2_IRQHandler
.thumb_set ADC1_2_IRQHandler, Default_Handler

.weak   USB_HP_CAN1_TX_IRQHandler
.thumb_set USB_HP_CAN1_TX_IRQHandler, Default_Handler

.weak   USB_LP_CAN1_RX0_IRQHandler
.thumb_set USB_LP_CAN1_RX0_IRQHandler, Default_Handler

.weak   CAN1_RX1_IRQHandler
.thumb_set CAN1_RX1_IRQHandler, Default_Handler

.weak   CAN1_SCE_IRQHandler
.thumb_set CAN1_SCE_IRQHandler, Default_Handler

.weak   EXTI9_5_IRQHandler
.thumb_set EXTI9_5_IRQHandler, Default_Handler

.weak   TIM1_BRK_IRQHandler
.thumb_set TIM1_BRK_IRQHandler, Default_Handler

.weak   TIM1_UP_IRQHandler
.thumb_set TIM1_UP_IRQHandler, Default_Handler

.weak   TIM1_TRG_COM_IRQHandler
.thumb_set TIM1_TRG_COM_IRQHandler, Default_Handler

.weak   TIM1_CC_IRQHandler
.thumb_set TIM1_CC_IRQHandler, Default_Handler

.weak   TIM2_IRQHandler
.thumb_set TIM2_IRQHandler, Default_Handler

.weak   TIM3_IRQHandler
.thumb_set TIM3_IRQHandler, Default_Handler

.weak   TIM4_IRQHandler
.thumb_set TIM4_IRQHandler, Default_Handler

.weak   I2C1_EV_IRQHandler
.thumb_set I2C1_EV_IRQHandler, Default_Handler

.weak   I2C1_ER_IRQHandler
.thumb_set I2C1_ER_IRQHandler, Default_Handler

.weak   I2C2_EV_IRQHandler
.thumb_set I2C2_EV_IRQHandler, Default_Handler

.weak   I2C2_ER_IRQHandler
.thumb_set I2C2_ER_IRQHandler, Default_Handler

.weak   SPI1_IRQHandler
.thumb_set SPI1_IRQHandler, Default_Handler

.weak   SPI2_IRQHandler
.thumb_set SPI2_IRQHandler, Default_Handler

.weak   USART1_IRQHandler
.thumb_set USART1_IRQHandler, Default_Handler

.weak   USART2_IRQHandler
.thumb_set USART2_IRQHandler, Default_Handler

.weak   USART3_IRQHandler
.thumb_set USART3_IRQHandler, Default_Handler

.weak   EXTI15_10_IRQHandler
.thumb_set EXTI15_10_IRQHandler, Default_Handler

.weak   RTC_Alarm_IRQHandler
.thumb_set RTC_Alarm_IRQHandler, Default_Handler

.weak   USBWakeUp_IRQHandler
.thumb_set USBWakeUp_IRQHandler, Default_Handler

.end