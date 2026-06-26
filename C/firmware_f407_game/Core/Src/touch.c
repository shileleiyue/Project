/**
  ******************************************************************************
  * @file    touch.c
  * @brief   FT5206 电容触摸屏驱动 (I2C2)
  * @note    适用于正点原子探索者 STM32F407ZGT6 开发板
  ******************************************************************************
  */

#include "touch.h"

I2C_HandleTypeDef hi2c2;

/* 当前触摸点 */
static TouchPoint_t g_touch_point;

/* I2C 写寄存器 */
static uint8_t FT5206_WriteReg(uint8_t reg, uint8_t value) {
    uint8_t buf[2] = {reg, value};
    return HAL_I2C_Master_Transmit(&hi2c2, FT5206_ADDR << 1, buf, 2, 100) == HAL_OK;
}

/* I2C 读寄存器 */
static uint8_t FT5206_ReadReg(uint8_t reg) {
    uint8_t value = 0;
    HAL_I2C_Master_Transmit(&hi2c2, FT5206_ADDR << 1, &reg, 1, 100);
    HAL_I2C_Master_Receive(&hi2c2, FT5206_ADDR << 1, &value, 1, 100);
    return value;
}

/* I2C 读多个寄存器 */
static uint8_t FT5206_ReadMulti(uint8_t reg, uint8_t *buf, uint8_t len) {
    return HAL_I2C_Master_Transmit(&hi2c2, FT5206_ADDR << 1, &reg, 1, 100) == HAL_OK &&
           HAL_I2C_Master_Receive(&hi2c2, FT5206_ADDR << 1, buf, len, 100) == HAL_OK;
}

/* ======================== 初始化 ======================== */

void Touch_Init(void) {
    uint8_t chip_id;

    /* 等待 FT5206 上电稳定 */
    HAL_Delay(50);

    /* 读取芯片 ID */
    chip_id = FT5206_ReadReg(FT5206_REG_ID_MODE);
    if (chip_id == 0) {
        /* 如果读取失败，重试一次 */
        HAL_Delay(10);
        chip_id = FT5206_ReadReg(FT5206_REG_ID_MODE);
    }

    /* 设置为正常工作模式 */
    FT5206_WriteReg(FT5206_REG_MODE, 0x00);

    /* 设置报告速率 (30ms) */
    FT5206_WriteReg(FT5206_REG_PERIOD, 0x1E);

    /* 初始化触摸点 */
    g_touch_point.x = 0;
    g_touch_point.y = 0;
    g_touch_point.pressed = 0;
}

/* ======================== 触摸扫描 ======================== */

uint8_t Touch_Scan(void) {
    uint8_t buf[5];
    uint8_t status;

    status = FT5206_ReadReg(FT5206_REG_TD_STATUS);

    if ((status & 0x0F) > 0) {
        /* 有触摸点，读取坐标 */
        if (FT5206_ReadMulti(FT5206_REG_TOUCH1_XH, buf, 5)) {
            g_touch_point.x = ((uint16_t)(buf[0] & 0x0F) << 8) | buf[1];
            g_touch_point.y = ((uint16_t)(buf[2] & 0x0F) << 8) | buf[3];
            g_touch_point.pressed = 1;

            /* 注意: FT5206 的坐标可能与 LCD 方向不同，需要映射 */
            /* 探索者 4.3寸屏: 触摸坐标已经是 480x800，无需映射 */
            return 1;
        }
    }

    g_touch_point.pressed = 0;
    return 0;
}

/* ======================== 获取触摸点 ======================== */

TouchPoint_t Touch_GetPoint(void) {
    return g_touch_point;
}

uint8_t Touch_IsPressed(void) {
    return g_touch_point.pressed;
}