/**
  ******************************************************************************
  * @file    lcd.c
  * @brief   ILI9341 4.3寸 TFT LCD 驱动 (480x800, FSMC 16位并行接口)
  * @note    适用于正点原子探索者 STM32F407ZGT6 开发板
  ******************************************************************************
  */

#include "lcd.h"
#include <string.h>

/* 内联函数: 快速写像素 */
static inline void LCD_WritePixel(uint16_t color) {
    LCD_RAM = color;
}

/* 内联函数: 快速读像素 */
static inline uint16_t LCD_ReadPixel(void) {
    return LCD_RAM;
}

/* ======================== ILI9341 初始化序列 ======================== */

void LCD_Init(void) {
    /* 硬件复位: 拉低再拉高(如果 LCD_RST 连接到 NRST 则跳过) */

    /* 软件复位 */
    LCD_WriteCmd(0x01);
    HAL_Delay(120);

    /* 电源控制 A */
    LCD_WriteCmd(0xCB);
    LCD_WriteData(0x39);
    LCD_WriteData(0x2C);
    LCD_WriteData(0x00);
    LCD_WriteData(0x34);
    LCD_WriteData(0x02);

    /* 电源控制 B */
    LCD_WriteCmd(0xCF);
    LCD_WriteData(0x00);
    LCD_WriteData(0xC1);
    LCD_WriteData(0x30);

    /* 驱动时序控制 A */
    LCD_WriteCmd(0xE8);
    LCD_WriteData(0x85);
    LCD_WriteData(0x00);
    LCD_WriteData(0x78);

    /* 驱动时序控制 B */
    LCD_WriteCmd(0xEA);
    LCD_WriteData(0x00);
    LCD_WriteData(0x00);

    /* 电源时序控制 */
    LCD_WriteCmd(0xED);
    LCD_WriteData(0x64);
    LCD_WriteData(0x03);
    LCD_WriteData(0x12);
    LCD_WriteData(0x81);

    /* 泵比率控制 */
    LCD_WriteCmd(0xF7);
    LCD_WriteData(0x20);

    /* 电源控制 1 */
    LCD_WriteCmd(0xC0);
    LCD_WriteData(0x23);

    /* 电源控制 2 */
    LCD_WriteCmd(0xC1);
    LCD_WriteData(0x10);

    /* VCOM 控制 1 */
    LCD_WriteCmd(0xC5);
    LCD_WriteData(0x3E);
    LCD_WriteData(0x28);

    /* VCOM 控制 2 */
    LCD_WriteCmd(0xC7);
    LCD_WriteData(0x86);

    /* 内存访问控制: 竖屏 MY=1, MX=1, MV=0, BGR=1 */
    LCD_WriteCmd(0x36);
    LCD_WriteData(0x48);

    /* 像素格式: 16位 RGB565 */
    LCD_WriteCmd(0x3A);
    LCD_WriteData(0x55);

    /* 帧速率控制 */
    LCD_WriteCmd(0xB1);
    LCD_WriteData(0x00);
    LCD_WriteData(0x18);

    /* 显示功能控制 */
    LCD_WriteCmd(0xB6);
    LCD_WriteData(0x08);
    LCD_WriteData(0x82);
    LCD_WriteData(0x27);

    /* 启用 Gamma 校正 */
    LCD_WriteCmd(0xF2);
    LCD_WriteData(0x00);

    /* Gamma 曲线设置 */
    LCD_WriteCmd(0x26);
    LCD_WriteData(0x01);

    /* 正 Gamma 校正 */
    LCD_WriteCmd(0xE0);
    LCD_WriteData(0x0F);
    LCD_WriteData(0x31);
    LCD_WriteData(0x2B);
    LCD_WriteData(0x0C);
    LCD_WriteData(0x0E);
    LCD_WriteData(0x08);
    LCD_WriteData(0x4E);
    LCD_WriteData(0xF1);
    LCD_WriteData(0x37);
    LCD_WriteData(0x07);
    LCD_WriteData(0x10);
    LCD_WriteData(0x03);
    LCD_WriteData(0x0E);
    LCD_WriteData(0x09);
    LCD_WriteData(0x00);

    /* 负 Gamma 校正 */
    LCD_WriteCmd(0xE1);
    LCD_WriteData(0x00);
    LCD_WriteData(0x0E);
    LCD_WriteData(0x14);
    LCD_WriteData(0x03);
    LCD_WriteData(0x11);
    LCD_WriteData(0x07);
    LCD_WriteData(0x31);
    LCD_WriteData(0xC1);
    LCD_WriteData(0x48);
    LCD_WriteData(0x08);
    LCD_WriteData(0x0F);
    LCD_WriteData(0x0C);
    LCD_WriteData(0x31);
    LCD_WriteData(0x36);
    LCD_WriteData(0x0F);

    /* 退出睡眠模式 */
    LCD_WriteCmd(0x11);
    HAL_Delay(120);

    /* 开启显示 */
    LCD_WriteCmd(0x29);

    /* 设置显示区域为全屏 */
    LCD_SetWindow(0, 0, LCD_WIDTH - 1, LCD_HEIGHT - 1);

    /* 开启背光 */
    LCD_SetBackLight(100);
}

/* ======================== 基础操作函数 ======================== */

void LCD_WriteCmd(uint16_t cmd) {
    LCD_REG = cmd;
}

void LCD_WriteData(uint16_t data) {
    LCD_RAM = data;
}

uint16_t LCD_ReadData(void) {
    return LCD_RAM;
}

/* ======================== 窗口设置 ======================== */

void LCD_SetWindow(uint16_t x1, uint16_t y1, uint16_t x2, uint16_t y2) {
    LCD_WriteCmd(0x2A);  /* 列地址设置 */
    LCD_WriteData(x1 >> 8);
    LCD_WriteData(x1 & 0xFF);
    LCD_WriteData(x2 >> 8);
    LCD_WriteData(x2 & 0xFF);

    LCD_WriteCmd(0x2B);  /* 行地址设置 */
    LCD_WriteData(y1 >> 8);
    LCD_WriteData(y1 & 0xFF);
    LCD_WriteData(y2 >> 8);
    LCD_WriteData(y2 & 0xFF);

    LCD_WriteCmd(0x2C);  /* 内存写入 */
}

/* ======================== 填充函数 ======================== */

void LCD_Fill(uint16_t x1, uint16_t y1, uint16_t x2, uint16_t y2, uint16_t color) {
    uint32_t pixel_count = (uint32_t)(x2 - x1 + 1) * (y2 - y1 + 1);
    uint32_t i;

    LCD_SetWindow(x1, y1, x2, y2);

    for (i = 0; i < pixel_count; i++) {
        LCD_WritePixel(color);
    }
}

void LCD_Clear(uint16_t color) {
    LCD_Fill(0, 0, LCD_WIDTH - 1, LCD_HEIGHT - 1, color);
}

/* ======================== 像素绘制 ======================== */

void LCD_DrawPixel(uint16_t x, uint16_t y, uint16_t color) {
    if (x >= LCD_WIDTH || y >= LCD_HEIGHT) return;
    LCD_SetWindow(x, y, x, y);
    LCD_WritePixel(color);
}

/* ======================== 直线绘制 ======================== */

void LCD_DrawLine(uint16_t x1, uint16_t y1, uint16_t x2, uint16_t y2, uint16_t color) {
    int16_t dx = (int16_t)x2 - (int16_t)x1;
    int16_t dy = (int16_t)y2 - (int16_t)y1;
    int16_t sx = dx > 0 ? 1 : -1;
    int16_t sy = dy > 0 ? 1 : -1;
    int16_t err;

    dx = dx > 0 ? dx : -dx;
    dy = dy > 0 ? dy : -dy;
    err = dx - dy;

    while (1) {
        LCD_DrawPixel(x1, y1, color);
        if (x1 == x2 && y1 == y2) break;
        int16_t e2 = err * 2;
        if (e2 > -dy) { err -= dy; x1 += sx; }
        if (e2 < dx)  { err += dx; y1 += sy; }
    }
}

/* ======================== 矩形绘制 ======================== */

void LCD_DrawRect(uint16_t x1, uint16_t y1, uint16_t x2, uint16_t y2, uint16_t color) {
    LCD_DrawLine(x1, y1, x2, y1, color);
    LCD_DrawLine(x2, y1, x2, y2, color);
    LCD_DrawLine(x2, y2, x1, y2, color);
    LCD_DrawLine(x1, y2, x1, y1, color);
}

void LCD_FillRect(uint16_t x1, uint16_t y1, uint16_t x2, uint16_t y2, uint16_t color) {
    LCD_Fill(x1, y1, x2, y2, color);
}

/* ======================== 圆形绘制 (Bresenham) ======================== */

void LCD_DrawCircle(uint16_t cx, uint16_t cy, uint16_t r, uint16_t color) {
    int16_t x = 0, y = r;
    int16_t d = 3 - 2 * r;

    while (x <= y) {
        LCD_DrawPixel(cx + x, cy + y, color);
        LCD_DrawPixel(cx - x, cy + y, color);
        LCD_DrawPixel(cx + x, cy - y, color);
        LCD_DrawPixel(cx - x, cy - y, color);
        LCD_DrawPixel(cx + y, cy + x, color);
        LCD_DrawPixel(cx - y, cy + x, color);
        LCD_DrawPixel(cx + y, cy - x, color);
        LCD_DrawPixel(cx - y, cy - x, color);

        if (d < 0) {
            d = d + 4 * x + 6;
        } else {
            d = d + 4 * (x - y) + 10;
            y--;
        }
        x++;
    }
}

void LCD_FillCircle(uint16_t cx, uint16_t cy, uint16_t r, uint16_t color) {
    int16_t x = 0, y = r;
    int16_t d = 3 - 2 * r;

    while (x <= y) {
        /* 绘制水平填充线 */
        LCD_DrawLine(cx - x, cy + y, cx + x, cy + y, color);
        LCD_DrawLine(cx - x, cy - y, cx + x, cy - y, color);
        LCD_DrawLine(cx - y, cy + x, cx + y, cy + x, color);
        LCD_DrawLine(cx - y, cy - x, cx + y, cy - x, color);

        if (d < 0) {
            d = d + 4 * x + 6;
        } else {
            d = d + 4 * (x - y) + 10;
            y--;
        }
        x++;
    }
}

/* ======================== 背光控制 ======================== */

void LCD_SetBackLight(uint8_t brightness) {
    if (brightness > 100) brightness = 100;
    /* 使用 TIM3_CH3 PWM 控制背光 */
    __HAL_TIM_SET_COMPARE(&LCD_BL_TIM, LCD_BL_CHANNEL,
                          (uint32_t)(1000 * brightness / 100));
}

/* ======================== 字符显示 (5x7 字体) ======================== */

/* ASCII 5x7 字体表 (仅可打印字符 32-127) */
static const uint8_t font5x7[][5] = {
    {0x00,0x00,0x00,0x00,0x00}, /* space */
    {0x00,0x00,0x5F,0x00,0x00}, /* ! */
    {0x00,0x07,0x00,0x07,0x00}, /* " */
    {0x14,0x7F,0x14,0x7F,0x14}, /* # */
    {0x24,0x2A,0x7F,0x2A,0x12}, /* $ */
    {0x23,0x13,0x08,0x64,0x62}, /* % */
    {0x36,0x49,0x55,0x22,0x50}, /* & */
    {0x00,0x05,0x03,0x00,0x00}, /* ' */
    {0x00,0x1C,0x22,0x41,0x00}, /* ( */
    {0x00,0x41,0x22,0x1C,0x00}, /* ) */
    {0x08,0x2A,0x1C,0x2A,0x08}, /* * */
    {0x08,0x08,0x3E,0x08,0x08}, /* + */
    {0x00,0x50,0x30,0x00,0x00}, /* , */
    {0x08,0x08,0x08,0x08,0x08}, /* - */
    {0x00,0x60,0x60,0x00,0x00}, /* . */
    {0x20,0x10,0x08,0x04,0x02}, /* / */
    {0x3E,0x51,0x49,0x45,0x3E}, /* 0 */
    {0x00,0x42,0x7F,0x40,0x00}, /* 1 */
    {0x42,0x61,0x51,0x49,0x46}, /* 2 */
    {0x21,0x41,0x45,0x4B,0x31}, /* 3 */
    {0x18,0x14,0x12,0x7F,0x10}, /* 4 */
    {0x27,0x45,0x45,0x45,0x39}, /* 5 */
    {0x3C,0x4A,0x49,0x49,0x30}, /* 6 */
    {0x01,0x71,0x09,0x05,0x03}, /* 7 */
    {0x36,0x49,0x49,0x49,0x36}, /* 8 */
    {0x06,0x49,0x49,0x29,0x1E}, /* 9 */
    {0x00,0x36,0x36,0x00,0x00}, /* : */
    {0x00,0x56,0x36,0x00,0x00}, /* ; */
    {0x00,0x08,0x14,0x22,0x41}, /* < */
    {0x14,0x14,0x14,0x14,0x14}, /* = */
    {0x41,0x22,0x14,0x08,0x00}, /* > */
    {0x02,0x01,0x51,0x09,0x06}, /* ? */
    {0x32,0x49,0x79,0x41,0x3E}, /* @ */
    {0x7E,0x11,0x11,0x11,0x7E}, /* A */
    {0x7F,0x49,0x49,0x49,0x36}, /* B */
    {0x3E,0x41,0x41,0x41,0x22}, /* C */
    {0x7F,0x41,0x41,0x22,0x1C}, /* D */
    {0x7F,0x49,0x49,0x49,0x41}, /* E */
    {0x7F,0x09,0x09,0x01,0x01}, /* F */
    {0x3E,0x41,0x41,0x51,0x32}, /* G */
    {0x7F,0x08,0x08,0x08,0x7F}, /* H */
    {0x00,0x41,0x7F,0x41,0x00}, /* I */
    {0x20,0x40,0x41,0x3F,0x01}, /* J */
    {0x7F,0x08,0x14,0x22,0x41}, /* K */
    {0x7F,0x40,0x40,0x40,0x40}, /* L */
    {0x7F,0x02,0x04,0x02,0x7F}, /* M */
    {0x7F,0x04,0x08,0x10,0x7F}, /* N */
    {0x3E,0x41,0x41,0x41,0x3E}, /* O */
    {0x7F,0x09,0x09,0x09,0x06}, /* P */
    {0x3E,0x41,0x51,0x21,0x5E}, /* Q */
    {0x7F,0x09,0x19,0x29,0x46}, /* R */
    {0x46,0x49,0x49,0x49,0x31}, /* S */
    {0x01,0x01,0x7F,0x01,0x01}, /* T */
    {0x3F,0x40,0x40,0x40,0x3F}, /* U */
    {0x1F,0x20,0x40,0x20,0x1F}, /* V */
    {0x7F,0x20,0x18,0x20,0x7F}, /* W */
    {0x63,0x14,0x08,0x14,0x63}, /* X */
    {0x03,0x04,0x78,0x04,0x03}, /* Y */
    {0x61,0x51,0x49,0x45,0x43}, /* Z */
    {0x00,0x00,0x7F,0x41,0x41}, /* [ */
    {0x02,0x04,0x08,0x10,0x20}, /* \ */
    {0x41,0x41,0x7F,0x00,0x00}, /* ] */
    {0x04,0x02,0x01,0x02,0x04}, /* ^ */
    {0x40,0x40,0x40,0x40,0x40}, /* _ */
    {0x00,0x01,0x02,0x04,0x00}, /* ` */
    {0x20,0x54,0x54,0x54,0x78}, /* a */
    {0x7F,0x48,0x44,0x44,0x38}, /* b */
    {0x38,0x44,0x44,0x44,0x20}, /* c */
    {0x38,0x44,0x44,0x48,0x7F}, /* d */
    {0x38,0x54,0x54,0x54,0x18}, /* e */
    {0x08,0x7E,0x09,0x01,0x02}, /* f */
    {0x08,0x14,0x54,0x54,0x3C}, /* g */
    {0x7F,0x08,0x04,0x04,0x78}, /* h */
    {0x00,0x44,0x7D,0x40,0x00}, /* i */
    {0x20,0x40,0x44,0x3D,0x00}, /* j */
    {0x00,0x7F,0x10,0x28,0x44}, /* k */
    {0x00,0x41,0x7F,0x40,0x00}, /* l */
    {0x7C,0x04,0x18,0x04,0x78}, /* m */
    {0x7C,0x08,0x04,0x04,0x78}, /* n */
    {0x38,0x44,0x44,0x44,0x38}, /* o */
    {0x7C,0x14,0x14,0x14,0x08}, /* p */
    {0x08,0x14,0x14,0x18,0x7C}, /* q */
    {0x7C,0x08,0x04,0x04,0x08}, /* r */
    {0x48,0x54,0x54,0x54,0x20}, /* s */
    {0x04,0x3F,0x44,0x40,0x20}, /* t */
    {0x3C,0x40,0x40,0x20,0x7C}, /* u */
    {0x1C,0x20,0x40,0x20,0x1C}, /* v */
    {0x3C,0x40,0x30,0x40,0x3C}, /* w */
    {0x44,0x28,0x10,0x28,0x44}, /* x */
    {0x0C,0x50,0x50,0x50,0x3C}, /* y */
    {0x44,0x64,0x54,0x4C,0x44}, /* z */
    {0x00,0x08,0x36,0x41,0x00}, /* { */
    {0x00,0x00,0x7F,0x00,0x00}, /* | */
    {0x00,0x41,0x36,0x08,0x00}, /* } */
    {0x08,0x08,0x2A,0x1C,0x08}, /* ~ */
    {0x08,0x1C,0x2A,0x08,0x08}, /* ~ */
};

void LCD_ShowChar(uint16_t x, uint16_t y, char ch, uint16_t color, uint16_t bgcolor, uint8_t size) {
    uint8_t i, j;
    uint8_t row_data;
    uint8_t idx;

    if (ch < ' ' || ch > '~') ch = ' ';  /* 不可打印字符替换为空格 */
    idx = ch - ' ';

    for (i = 0; i < 5; i++) {
        row_data = font5x7[idx][i];
        for (j = 0; j < 7; j++) {
            if (row_data & (1 << j)) {
                if (size == 1) {
                    LCD_DrawPixel(x + i, y + j, color);
                } else {
                    LCD_Fill(x + i * size, y + j * size,
                             x + i * size + size - 1, y + j * size + size - 1, color);
                }
            } else {
                if (size > 1) {
                    LCD_Fill(x + i * size, y + j * size,
                             x + i * size + size - 1, y + j * size + size - 1, bgcolor);
                }
            }
        }
    }
}

void LCD_ShowString(uint16_t x, uint16_t y, const char *str, uint16_t color, uint16_t bgcolor, uint8_t size) {
    uint16_t cx = x;
    while (*str) {
        if (*str == '\n') {
            cx = x;
            y += 8 * size;
        } else {
            LCD_ShowChar(cx, y, *str, color, bgcolor, size);
            cx += 6 * size;
        }
        str++;
    }
}

void LCD_ShowNum(uint16_t x, uint16_t y, int32_t num, uint8_t len, uint16_t color, uint16_t bgcolor, uint8_t size) {
    char buf[12];
    uint8_t i;

    if (num < 0) {
        LCD_ShowChar(x, y, '-', color, bgcolor, size);
        num = -num;
        x += 6 * size;
    }

    for (i = 0; i < len; i++) {
        buf[len - 1 - i] = (num % 10) + '0';
        num /= 10;
    }

    for (i = 0; i < len; i++) {
        LCD_ShowChar(x + i * 6 * size, y, buf[i], color, bgcolor, size);
    }
}