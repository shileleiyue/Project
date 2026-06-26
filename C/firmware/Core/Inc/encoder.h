#ifndef __ENCODER_H
#define __ENCODER_H

#include "main.h"

/* ======================== 编码器常量 ======================== */

// 编码器每转脉冲数（根据实际编码器修改）
#define ENCODER_PULSES_PER_REV   390

// 减速比（根据实际电机修改）
#define MOTOR_GEAR_RATIO         30.0f

/* ======================== 编码器结构体 ======================== */

typedef struct {
    TIM_HandleTypeDef *timer;   // 编码器定时器
    int16_t last_count;         // 上次读取的计数值
    float speed;                // 换算后的速度（mm/s）
    float total_distance;       // 累计距离（mm）
} Encoder_TypeDef;

/* ======================== 全局编码器实例 ======================== */

extern Encoder_TypeDef g_encoder_left;
extern Encoder_TypeDef g_encoder_right;

/* ======================== 函数声明 ======================== */

// 初始化编码器定时器
void Encoder_Init(void);

// 读取编码器速度（mm/s），每1ms调用一次
float Encoder_ReadSpeed(Encoder_TypeDef *enc);

// 读取累计距离（mm）
float Encoder_GetDistance(Encoder_TypeDef *enc);

// 重置累计距离
void Encoder_ResetDistance(Encoder_TypeDef *enc);

#endif /* __ENCODER_H */