#ifndef __MAIN_H
#define __MAIN_H

#include "stm32f4xx_hal.h"
#include "lcd.h"
#include "touch.h"
#include "game.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/* 板载 LED */
#define LED0_PORT       GPIOF
#define LED0_PIN        GPIO_PIN_9
#define LED1_PORT       GPIOF
#define LED1_PIN        GPIO_PIN_10

/* 按键 */
#define KEY0_PORT       GPIOE
#define KEY0_PIN        GPIO_PIN_4
#define KEY1_PORT       GPIOE
#define KEY1_PIN        GPIO_PIN_3
#define KEY2_PORT       GPIOE
#define KEY2_PIN        GPIO_PIN_2
#define WKUP_PORT       GPIOA
#define WKUP_PIN        GPIO_PIN_0

/* 外设句柄 */
extern I2C_HandleTypeDef   hi2c2;
extern TIM_HandleTypeDef   htim3;
extern SRAM_HandleTypeDef  hsram1;

/* 系统函数 */
void SystemClock_Config(void);
void MX_GPIO_Init(void);
void MX_FSMC_Init(void);
void MX_I2C2_Init(void);
void MX_TIM3_Init(void);
void Error_Handler(void);

#endif /* __MAIN_H */