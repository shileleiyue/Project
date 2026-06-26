/**
  ******************************************************************************
  * @file    stm32f1xx_it.c
  * @brief   中断服务函数实现
  * @details 提供系统所需的中断处理程序
  *          - SysTick_Handler: 调用 HAL_IncTick
  *          - TIM1_UP_IRQHandler: 调用 HAL_TIM_IRQHandler
  *          - USART1_IRQHandler: 调用 HAL_UART_IRQHandler
  *          - USART2_IRQHandler: 调用 HAL_UART_IRQHandler
  * @note    HAL_IncTick 在 stm32f1xx_hal.c 中定义
  *          TIM1_UP_IRQHandler 在 main.c 中也有定义（使用寄存器版本），
  *          此文件中的实现使用 HAL 库版本，二者选其一。
  *          main.c 中直接使用寄存器操作处理 TIM1 中断，
  *          因此此文件中的 TIM1_UP_IRQHandler 不会被链接。
  ******************************************************************************
  */

#include "stm32f1xx_it.h"
#include "stm32f1xx_hal.h"
#include "main.h"

/* ======================== 外部变量声明 ======================== */

/* ======================== SysTick_Handler ======================== */

/**
  * @brief 系统滴答定时器中断处理
  * @note  HAL_Init 中配置 SysTick 为 1ms 间隔
  *        HAL_IncTick 在 stm32f1xx_hal.c 中定义
  */
void SysTick_Handler(void)
{
    HAL_IncTick();
}

/* ======================== TIM1_UP_IRQHandler ======================== */

/**
  * @brief TIM1 更新中断处理
  * @note  main.c 中已使用寄存器版本处理 TIM1 中断，
  *        此函数作为 weak 实现存在，main.c 中的定义会覆盖此实现
  *        如果使用 HAL 库的 TIM 中断方式，可取消注释下方代码
  */
#if 0
void TIM1_UP_IRQHandler(void)
{
    HAL_TIM_IRQHandler(&htim1);
}
#endif

/* ======================== USART1_IRQHandler ======================== */

/**
  * @brief USART1 中断处理
  * @note  调用 HAL_UART_IRQHandler 唤醒 HAL 库的中断处理流程
  *        HAL_UART_RxCpltCallback 回调在 main.c 中实现
  */
void USART1_IRQHandler(void)
{
    HAL_UART_IRQHandler(&huart1);
}

/* ======================== USART2_IRQHandler ======================== */

/**
  * @brief USART2 中断处理
  * @note  调用 HAL_UART_IRQHandler 唤醒 HAL 库的中断处理流程
  */
void USART2_IRQHandler(void)
{
    HAL_UART_IRQHandler(&huart2);
}