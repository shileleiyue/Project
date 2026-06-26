/**
 * @file    indicator.c
 * @brief   指示灯和蜂鸣器实现
 * @note    RGB LED: PB14(R), PB15(G), PB8(B), 共阴极, 高电平点亮
 *          蜂鸣器: PB3, 有源蜂鸣器, 高电平发声
 *          注意：STM32F103C8T6(LQFP48) 无 PC0~PC4 引脚，改用 PB 空闲引脚
 *          状态-颜色映射:
 *            初始化: 蓝色 (常亮)
 *            平衡中: 绿色 (常亮)
 *            低电量: 黄色 (闪烁)
 *            摔倒:   红色 (常亮)
 *            休眠:   熄灭
 *            错误:   红色 (闪烁)
 */

#include "indicator.h"

/* ======================== 私有变量 ======================== */

static uint16_t blink_color = RGB_OFF;
static uint16_t blink_period = 500;  // 闪烁周期(ms)
static uint32_t last_blink_ms = 0;
static uint8_t blink_state = 0;

/* ======================== 函数实现 ======================== */

/**
 * @brief 初始化指示灯和蜂鸣器GPIO
 * GPIO已在main.c的MX_GPIO_Init中初始化
 * 这里只需要确保初始状态正确
 */
void Indicator_Init(void)
{
    // 确保所有LED和蜂鸣器关闭
    Indicator_Off();
    Buzzer_Off();
}

/**
 * @brief 设置RGB颜色
 * @param color RGB颜色组合 (RGB_RED, RGB_GREEN, RGB_BLUE等的按位或)
 * 
 * 共阴极RGB LED，对应引脚高电平点亮：
 *   PB14 = 红色通道
 *   PB15 = 绿色通道
 *   PB8  = 蓝色通道
 */
void Indicator_SetColor(uint16_t color)
{
    // 设置红色通道
    if (color & 0x001)
        HAL_GPIO_WritePin(LED_R_PORT, LED_R_PIN, GPIO_PIN_SET);
    else
        HAL_GPIO_WritePin(LED_R_PORT, LED_R_PIN, GPIO_PIN_RESET);

    // 设置绿色通道
    if (color & 0x002)
        HAL_GPIO_WritePin(LED_G_PORT, LED_G_PIN, GPIO_PIN_SET);
    else
        HAL_GPIO_WritePin(LED_G_PORT, LED_G_PIN, GPIO_PIN_RESET);

    // 设置蓝色通道
    if (color & 0x004)
        HAL_GPIO_WritePin(LED_B_PORT, LED_B_PIN, GPIO_PIN_SET);
    else
        HAL_GPIO_WritePin(LED_B_PORT, LED_B_PIN, GPIO_PIN_RESET);
}

/**
 * @brief 设置RGB颜色并闪烁
 * @param color 颜色
 * @param period_ms 闪烁周期（ms）
 */
void Indicator_SetBlink(uint16_t color, uint16_t period_ms)
{
    blink_color = color;
    blink_period = period_ms;
    blink_state = 0;
    last_blink_ms = HAL_GetTick();
}

/**
 * @brief 关闭所有指示灯
 */
void Indicator_Off(void)
{
    HAL_GPIO_WritePin(LED_R_PORT, LED_R_PIN, GPIO_PIN_RESET);
    HAL_GPIO_WritePin(LED_G_PORT, LED_G_PIN, GPIO_PIN_RESET);
    HAL_GPIO_WritePin(LED_B_PORT, LED_B_PIN, GPIO_PIN_RESET);
    blink_color = RGB_OFF;
}

/**
 * @brief 蜂鸣器开
 */
void Buzzer_On(void)
{
    HAL_GPIO_WritePin(BUZZER_PORT, BUZZER_PIN, GPIO_PIN_SET);
}

/**
 * @brief 蜂鸣器关
 */
void Buzzer_Off(void)
{
    HAL_GPIO_WritePin(BUZZER_PORT, BUZZER_PIN, GPIO_PIN_RESET);
}

/**
 * @brief 蜂鸣器响一声
 * @param duration_ms 持续时间 (ms)
 */
void Buzzer_Beep(uint16_t duration_ms)
{
    Buzzer_On();
    // 这里不能使用HAL_Delay阻塞，因为是在主循环中调用
    // 实际使用中需要配合定时器或者标志位
    // 简单起见，使用HAL_Delay（但会阻塞主循环）
    // 更优方案：使用非阻塞方式
    HAL_Delay(duration_ms);
    Buzzer_Off();
}

/**
 * @brief 根据系统状态更新指示灯
 * @param state 系统状态
 */
void Indicator_UpdateByState(SystemState_t state)
{
    switch (state)
    {
        case SYSTEM_INIT:
            Indicator_SetColor(RGB_BLUE);
            break;

        case SYSTEM_STARTUP:
            Indicator_SetColor(RGB_BLUE);
            break;

        case SYSTEM_BALANCING:
            Indicator_SetColor(RGB_GREEN);
            break;

        case SYSTEM_LOW_BAT:
            Indicator_SetBlink(RGB_YELLOW, 500);
            break;

        case SYSTEM_FALLEN:
            Indicator_SetColor(RGB_RED);
            break;

        case SYSTEM_SLEEP:
            Indicator_Off();
            break;

        case SYSTEM_ERROR:
            Indicator_SetBlink(RGB_RED, 200);
            break;
    }
}

/**
 * @brief 指示灯主处理（在主循环中调用，处理闪烁逻辑）
 */
void Indicator_Process(void)
{
    // 如果没有闪烁任务，直接返回
    if (blink_color == RGB_OFF)
        return;

    uint32_t now = HAL_GetTick();

    // 判断是否到了切换状态的时间
    if (now - last_blink_ms >= blink_period / 2)
    {
        last_blink_ms = now;
        blink_state = !blink_state;

        if (blink_state)
        {
            // 亮
            Indicator_SetColor(blink_color);
        }
        else
        {
            // 灭
            Indicator_Off();
        }
    }
}