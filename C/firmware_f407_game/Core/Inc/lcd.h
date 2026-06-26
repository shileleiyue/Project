#ifndef __LCD_H
#define __LCD_H

#include "stm32f4xx_hal.h"
#include <stdint.h>

/* ILI9341 4.3寸 TFT LCD 驱动 (480x800) */

/* LCD 尺寸 */
#define LCD_WIDTH   480
#define LCD_HEIGHT  800

/* FSMC 基地址 (Bank1, Region4, NE4) */
#define LCD_BASE_ADDR   0x6C000000

/* 命令/数据选择: FSMC_A6 连接 LCD_RS */
#define LCD_REG  (*(__IO uint16_t *)(LCD_BASE_ADDR))
#define LCD_RAM  (*(__IO uint16_t *)(LCD_BASE_ADDR | (1 << 7)))

/* 颜色定义 (RGB565) */
#define COLOR_WHITE       0xFFFF
#define COLOR_BLACK       0x0000
#define COLOR_RED         0xF800
#define COLOR_GREEN       0x07E0
#define COLOR_BLUE        0x001F
#define COLOR_YELLOW      0xFFE0
#define COLOR_CYAN        0x07FF
#define COLOR_MAGENTA     0xF81F
#define COLOR_GRAY        0x8410
#define COLOR_BROWN       0xA145
#define COLOR_ORANGE      0xFD20
#define COLOR_DARKGREEN   0x03E0
#define COLOR_LIGHTGRAY   0xC618

/* 背光控制引脚: PB0 */
#define LCD_BL_PORT     GPIOB
#define LCD_BL_PIN      GPIO_PIN_0

/* 背光 PWM 定时器: TIM3_CH3 */
#define LCD_BL_TIM      TIM3
#define LCD_BL_CHANNEL  TIM_CHANNEL_3

/* 函数声明 */
void LCD_Init(void);
void LCD_WriteCmd(uint16_t cmd);
void LCD_WriteData(uint16_t data);
uint16_t LCD_ReadData(void);
void LCD_SetWindow(uint16_t x1, uint16_t y1, uint16_t x2, uint16_t y2);
void LCD_Fill(uint16_t x1, uint16_t y1, uint16_t x2, uint16_t y2, uint16_t color);
void LCD_Clear(uint16_t color);
void LCD_DrawPixel(uint16_t x, uint16_t y, uint16_t color);
void LCD_DrawLine(uint16_t x1, uint16_t y1, uint16_t x2, uint16_t y2, uint16_t color);
void LCD_DrawRect(uint16_t x1, uint16_t y1, uint16_t x2, uint16_t y2, uint16_t color);
void LCD_FillRect(uint16_t x1, uint16_t y1, uint16_t x2, uint16_t y2, uint16_t color);
void LCD_DrawCircle(uint16_t cx, uint16_t cy, uint16_t r, uint16_t color);
void LCD_FillCircle(uint16_t cx, uint16_t cy, uint16_t r, uint16_t color);
void LCD_SetBackLight(uint8_t brightness);
void LCD_ShowChar(uint16_t x, uint16_t y, char ch, uint16_t color, uint16_t bgcolor, uint8_t size);
void LCD_ShowString(uint16_t x, uint16_t y, const char *str, uint16_t color, uint16_t bgcolor, uint8_t size);
void LCD_ShowNum(uint16_t x, uint16_t y, int32_t num, uint8_t len, uint16_t color, uint16_t bgcolor, uint8_t size);

#endif /* __LCD_H */