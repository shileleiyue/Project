/**
  ******************************************************************************
  * @file    stm32f1xx_hal_conf.h
  * @brief   HAL 配置头文件
  * @details 启用所需外设模块，配置系统时钟参数
  ******************************************************************************
  */

#ifndef __STM32F1XX_HAL_CONF_H
#define __STM32F1XX_HAL_CONF_H

#ifdef __cplusplus
extern "C" {
#endif

/* ======================== 系统配置 ======================== */

/**
  * @brief 外部高速晶振频率 (Hz)
  *        开发板通常使用 8MHz 晶振
  */
#define HSE_VALUE                    8000000U

/**
  * @brief 内部高速振荡器频率 (Hz)
  *        STM32F1 内部 RC 振荡器为 8MHz
  */
#define HSI_VALUE                    8000000U

/**
  * @brief 内部低速振荡器频率 (Hz)
  *        STM32F1 内部 LSI 约为 40kHz
  */
#define LSI_VALUE                    40000U

/**
  * @brief 外部低速晶振频率 (Hz)
  *        通常为 32.768kHz (RTC 使用)
  */
#define LSE_VALUE                    32768U

/**
  * @brief 外部低速晶振起始超时时间 (ms)
  */
#define LSE_STARTUP_TIMEOUT          5000U

/**
  * @brief 系统工作电压 (mV)
  */
#define VDD_VALUE                    3300U

/**
  * @brief 滴答定时器中断优先级
  *        使用最低优先级 (15)，避免影响其他中断
  */
#define TICK_INT_PRIORITY            0x0FU

/**
  * @brief 是否使用 RTOS
  *        0: 不使用 RTOS (裸机)
  */
#define USE_RTOS                     0U

/**
  * @brief 预取缓冲使能
  *        1: 使能 Flash 预取缓冲，提高执行效率
  */
#define PREFETCH_ENABLE              1U

/**
  * @brief Flash 指令缓存使能
  */
#define INSTRUCTION_CACHE_ENABLE     0U

/**
  * @brief Flash 数据缓存使能
  */
#define DATA_CACHE_ENABLE            0U

/* ======================== 外设模块使能 ======================== */

/**
  * @brief 启用以下 HAL 外设模块
  *        未启用的模块不会被编译，以减小代码体积
  */
#define HAL_MODULE_ENABLED
#define HAL_ADC_MODULE_ENABLED
#define HAL_CORTEX_MODULE_ENABLED
#define HAL_DMA_MODULE_ENABLED
#define HAL_FLASH_MODULE_ENABLED
#define HAL_GPIO_MODULE_ENABLED
#define HAL_I2C_MODULE_ENABLED
#define HAL_PWR_MODULE_ENABLED
#define HAL_RCC_MODULE_ENABLED
#define HAL_TIM_MODULE_ENABLED
#define HAL_UART_MODULE_ENABLED

/* ======================== 回调注册配置 ======================== */

/**
  * @brief 是否使用外设注册回调功能
  *        0: 不使用 (使用传统的 HAL_PPP_MspInit 回调)
  *        HAL 库通过 weak 符号机制自动链接到用户定义的 MSP 函数
  */
#define USE_HAL_ADC_REGISTER_CALLBACKS     0U
#define USE_HAL_DMA_REGISTER_CALLBACKS     0U
#define USE_HAL_I2C_REGISTER_CALLBACKS     0U
#define USE_HAL_TIM_REGISTER_CALLBACKS     0U
#define USE_HAL_UART_REGISTER_CALLBACKS    0U

/* ======================== 包含 HAL 模块头文件 ======================== */

#include "stm32f1xx_hal.h"

#ifdef __cplusplus
}
#endif

#endif /* __STM32F1XX_HAL_CONF_H */