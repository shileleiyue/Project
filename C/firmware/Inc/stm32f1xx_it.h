/**
  ******************************************************************************
  * @file    stm32f1xx_it.h
  * @brief   中断服务函数头文件
  ******************************************************************************
  */

#ifndef __STM32F1XX_IT_H
#define __STM32F1XX_IT_H

#ifdef __cplusplus
extern "C" {
#endif

/* ======================== 函数声明 ======================== */

/**
  * @brief 系统滴答定时器中断处理
  * @note  由 HAL_Init 配置，每 1ms 触发一次
  *        调用 HAL_IncTick 递增系统时钟
  */
void SysTick_Handler(void);

/**
  * @brief TIM1 更新中断处理 (1kHz 控制定时器)
  * @note  调用 HAL_TIM_IRQHandler 处理中断
  */
void TIM1_UP_IRQHandler(void);

/**
  * @brief USART1 中断处理 (调试/蓝牙)
  * @note  调用 HAL_UART_IRQHandler 处理中断
  */
void USART1_IRQHandler(void);

/**
  * @brief USART2 中断处理 (语音模块)
  * @note  调用 HAL_UART_IRQHandler 处理中断
  */
void USART2_IRQHandler(void);

#ifdef __cplusplus
}
#endif

#endif /* __STM32F1XX_IT_H */