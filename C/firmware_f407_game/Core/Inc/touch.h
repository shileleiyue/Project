#ifndef __TOUCH_H
#define __TOUCH_H

#include "stm32f4xx_hal.h"
#include <stdint.h>

/* FT5206 电容触摸屏驱动 */

/* I2C 地址 */
#define FT5206_ADDR        0x38

/* FT5206 寄存器 */
#define FT5206_REG_MODE        0x00
#define FT5206_REG_TD_STATUS   0x02
#define FT5206_REG_TOUCH1_XH   0x03
#define FT5206_REG_TOUCH1_XL   0x04
#define FT5206_REG_TOUCH1_YH   0x05
#define FT5206_REG_TOUCH1_YL   0x06
#define FT5206_REG_ID_MODE     0xA4
#define FT5206_REG_PERIOD      0x88

/* I2C 句柄 */
extern I2C_HandleTypeDef hi2c2;

/* 触摸点结构体 */
typedef struct {
    uint16_t x;
    uint16_t y;
    uint8_t  pressed;
} TouchPoint_t;

/* 函数声明 */
void Touch_Init(void);
uint8_t Touch_Scan(void);
TouchPoint_t Touch_GetPoint(void);
uint8_t Touch_IsPressed(void);

#endif /* __TOUCH_H */