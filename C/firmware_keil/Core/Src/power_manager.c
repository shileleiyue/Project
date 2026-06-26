/**
 * @file    power_manager.c
 * @brief   电源管理实现
 * @note    电池电压检测（ADC读取）
 *          摔倒保护检测
 *          低电量报警
 */

#include "power_manager.h"

/* ======================== 外部变量引用 ======================== */

extern float g_pitch_angle;
extern float g_battery_voltage;
extern SystemState_t g_system_state;

/* ======================== 私有变量 ======================== */

static uint32_t fall_start_time = 0;
static uint8_t fall_detected = 0;

/* ======================== 函数实现 ======================== */

/**
 * @brief 初始化电源管理
 */
void Power_Init(void)
{
    // ADC已在main.c中初始化
    // 这里可以读取一次初始电压
    g_battery_voltage = Power_ReadBatteryVoltage();
}

/**
 * @brief 读取电池电压（V）
 * @return 电压值 (V)
 * 
 * 读取步骤:
 *   1. 启动ADC转换
 *   2. 等待转换完成
 *   3. 读取ADC值
 *   4. 换算为电压: V = ADC值 * 3.3 / 4096 * 分压比
 */
float Power_ReadBatteryVoltage(void)
{
    uint32_t adc_value = 0;

    // 启动ADC转换
    HAL_ADC_Start(&BATTERY_ADC);

    // 等待转换完成（超时100ms）
    if (HAL_ADC_PollForConversion(&BATTERY_ADC, 100) == HAL_OK)
    {
        adc_value = HAL_ADC_GetValue(&BATTERY_ADC);
    }

    // 停止ADC
    HAL_ADC_Stop(&BATTERY_ADC);

    // 换算为电压
    // STM32F103 ADC是12位, 参考电压3.3V
    // ADC值范围: 0~4095, 对应 0~3.3V
    // 实际电压 = ADC值 * 3.3 / 4096 * 分压比
    float voltage = (float)adc_value * 3.3f / 4096.0f * VOLTAGE_DIVIDER_RATIO;

    return voltage;
}

/**
 * @brief 检查电池状态
 * @return 0=正常, 1=低电量, 2=临界
 */
uint8_t Power_CheckBattery(void)
{
    float voltage = Power_ReadBatteryVoltage();
    g_battery_voltage = voltage;

    if (voltage < BATTERY_CRITICAL_VOLT)
        return 2;  // 临界
    if (voltage < BATTERY_LOW_VOLTAGE)
        return 1;  // 低电量

    return 0;  // 正常
}

/**
 * @brief 摔倒检测
 * @param pitch 当前倾角（度）
 * @return 0=正常, 1=摔倒
 * 
 * 检测逻辑:
 *   - 倾角超过阈值持续一定时间才判定为摔倒
 *   - 防止瞬时抖动造成的误判
 */
uint8_t Power_CheckFall(float pitch)
{
    if (fabsf(pitch) > FALL_TILT_THRESHOLD)
    {
        if (!fall_detected)
        {
            fall_detected = 1;
            fall_start_time = HAL_GetTick();
        }
        else
        {
            // 持续超过设定时间才触发保护
            if (HAL_GetTick() - fall_start_time >= FALL_DETECT_TIME_MS)
            {
                return 1;  // 摔倒
            }
        }
    }
    else
    {
        // 倾角恢复正常，重置检测
        fall_detected = 0;
        fall_start_time = 0;
    }

    return 0;  // 正常
}

/**
 * @brief 电源管理主处理（在主循环中调用）
 * 每100ms检查一次电池和摔倒状态
 */
void Power_Process(void)
{
    static uint32_t last_check_ms = 0;
    uint32_t now = HAL_GetTick();

    // 每100ms检查一次
    if (now - last_check_ms < 100)
        return;

    last_check_ms = now;

    // 1. 检查电池电压
    uint8_t bat_status = Power_CheckBattery();
    if (bat_status == 2)
    {
        // 临界电压，立即进入低电量状态
        g_system_state = SYSTEM_LOW_BAT;
        return;
    }
    else if (bat_status == 1)
    {
        // 低电量，如果正在平衡中则提示
        if (g_system_state == SYSTEM_BALANCING)
        {
            g_system_state = SYSTEM_LOW_BAT;
        }
    }

    // 2. 检查摔倒
    if (g_system_state == SYSTEM_BALANCING)
    {
        if (Power_CheckFall(g_pitch_angle))
        {
            g_system_state = SYSTEM_FALLEN;
        }
    }

    // 3. 如果状态是低电量或摔倒，但条件已恢复，回到启动状态
    if (g_system_state == SYSTEM_LOW_BAT)
    {
        if (bat_status == 0)
        {
            g_system_state = SYSTEM_STARTUP;
        }
    }
    else if (g_system_state == SYSTEM_FALLEN)
    {
        if (!Power_CheckFall(g_pitch_angle))
        {
            // 倾角恢复正常，等待用户重新启动
            g_system_state = SYSTEM_STARTUP;
        }
    }
}