#ifndef __MOTOR_H
#define __MOTOR_H

#include "main.h"

/* ======================== 电机结构体 ======================== */

typedef struct {
    TIM_HandleTypeDef *pwm_tim;     // PWM定时器
    uint32_t pwm_channel;           // PWM通道
    TIM_HandleTypeDef *encoder_tim; // 编码器定时器

    GPIO_TypeDef *dir1_port;        // 方向1端口
    uint16_t dir1_pin;              // 方向1引脚
    GPIO_TypeDef *dir2_port;        // 方向2端口
    uint16_t dir2_pin;              // 方向2引脚

    int16_t current_pwm;            // 当前PWM值
    int16_t last_encoder_cnt;       // 上次编码器计数值
    float speed;                    // 当前速度
} Motor_TypeDef;

/* ======================== 全局电机实例 ======================== */

extern Motor_TypeDef g_motor_left;   // 左电机
extern Motor_TypeDef g_motor_right;  // 右电机

/* ======================== 函数声明 ======================== */

// 初始化电机GPIO和PWM
void Motor_Init(void);

// 设置电机速度（PWM输出）
// speed: -1000 ~ 1000, 正数前进，负数后退
void Motor_SetSpeed(Motor_TypeDef *motor, int16_t speed);

// 刹车
void Motor_Brake(Motor_TypeDef *motor);

// 停止（不刹车，自由滑行）
void Motor_Stop(Motor_TypeDef *motor);

// 停止所有电机
void Motor_StopAll(void);

#endif /* __MOTOR_H */