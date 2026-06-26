#ifndef __STM32F4xx_HAL_CONF_H
#define __STM32F4xx_HAL_CONF_H

#ifdef __cplusplus
extern "C" {
#endif

/* 使能 HAL 模块 */
#define HAL_MODULE_ENABLED
#define HAL_GPIO_MODULE_ENABLED
#define HAL_RCC_MODULE_ENABLED
#define HAL_CORTEX_MODULE_ENABLED
#define HAL_DMA_MODULE_ENABLED
#define HAL_SRAM_MODULE_ENABLED
#define HAL_I2C_MODULE_ENABLED
#define HAL_TIM_MODULE_ENABLED
#define HAL_PWR_MODULE_ENABLED

/* HSE 晶振频率 */
#define HSE_VALUE    8000000U
#define HSE_STARTUP_TIMEOUT 100U

/* HSI 内部振荡器 */
#define HSI_VALUE    16000000U

/* LSE 外部低速晶振 */
#define LSE_VALUE    32768U
#define LSE_STARTUP_TIMEOUT 5000U

/* 系统时钟: 168MHz */
#define SYSTEM_CLOCK  168000000U

/* 使用 SysTick 作为 HAL 时钟源 */
#define TICK_INT_PRIORITY  0x00U

#include "stm32f4xx_hal.h"

#ifdef __cplusplus
}
#endif

#endif /* __STM32F4xx_HAL_CONF_H */