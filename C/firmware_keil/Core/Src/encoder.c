/**
 * @file    encoder.c
 * @brief   编码器读取实现
 * @note    左轮: TIM2 (PA0/PA1), 编码器模式TI1+TI2, 4倍频
 *          右轮: TIM3 (PB4/PB5), 编码器模式TI1+TI2, 4倍频
 *          速度计算: 每1ms读取一次, 计算差值得到速度
 */

#include "encoder.h"

/* ======================== 全局编码器实例 ======================== */

Encoder_TypeDef g_encoder_left;
Encoder_TypeDef g_encoder_right;

/* ======================== 函数实现 ======================== */

/**
 * @brief 初始化编码器
 * 编码器定时器已在 main.c 的 MX_TIM2_Init / MX_TIM3_Init 中初始化
 * 这里只需要初始化编码器结构体
 */
void Encoder_Init(void)
{
    // 左编码器
    g_encoder_left.timer = &htim2;
    g_encoder_left.last_count = 0;
    g_encoder_left.speed = 0.0f;
    g_encoder_left.total_distance = 0.0f;

    // 右编码器
    g_encoder_right.timer = &htim3;
    g_encoder_right.last_count = 0;
    g_encoder_right.speed = 0.0f;
    g_encoder_right.total_distance = 0.0f;
}

/**
 * @brief 读取编码器速度（mm/s）
 * 
 * 速度计算公式:
 *   脉冲数差值 = 当前计数值 - 上次计数值
 *   转速 = 脉冲数差值 / (编码器PPR * 4)   [4倍频]
 *   轮速 = 转速 * 轮胎周长 * 控制频率
 *         = 脉冲数差值 * 轮胎周长 / (编码器PPR * 4) * 1000
 * 
 * 注意: 编码器模式TI1+TI2模式下，定时器计数值自动实现4倍频
 *       所以实际脉冲数差值 = 定时器计数值差值
 * 
 * @param enc 编码器结构体指针
 * @return 速度 (mm/s), 正数前进, 负数后退
 */
float Encoder_ReadSpeed(Encoder_TypeDef *enc)
{
    // 读取当前编码器计数值（16位有符号）
    int16_t current_count = (int16_t)__HAL_TIM_GET_COUNTER(enc->timer);

    // 计算差值（注意处理溢出）
    int16_t delta = current_count - enc->last_count;
    enc->last_count = current_count;

    // 如果不是TI1+TI2编码器模式（4倍频），需要乘以4
    // 这里已经是4倍频模式，所以直接使用delta

    // 计算速度: 速度 = 脉冲数 * 轮胎周长 / (编码器PPR) * 控制频率
    // 控制频率 = 1000Hz (每1ms读取一次)
    // 速度单位: mm/s
    // 如果编码器PPR=390, 轮胎周长=65*pi=204.2mm
    // 速度 = delta * 204.2 / 390 * 1000 = delta * 523.6
    // 但实际减速比30:1, 所以实际速度 = delta * 523.6 / 30 = delta * 17.45
    float speed = (float)delta * WHEEL_CIRCUMFERENCE_MM / (ENCODER_PULSES_PER_REV * MOTOR_GEAR_RATIO) * 1000.0f;

    enc->speed = speed;
    return speed;
}

/**
 * @brief 读取累计距离（mm）
 * @param enc 编码器结构体指针
 * @return 累计距离 (mm)
 */
float Encoder_GetDistance(Encoder_TypeDef *enc)
{
    return enc->total_distance;
}

/**
 * @brief 重置累计距离
 * @param enc 编码器结构体指针
 */
void Encoder_ResetDistance(Encoder_TypeDef *enc)
{
    enc->total_distance = 0.0f;
}