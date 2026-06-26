#ifndef __PID_H
#define __PID_H

#include "main.h"

/* ======================== PID 结构体 ======================== */

typedef struct {
    float kp;                   // 比例系数
    float ki;                   // 积分系数
    float kd;                   // 微分系数

    float integral;             // 积分累计值
    float last_error;           // 上一次误差
    float derivative;           // 微分项（可外部赋值）

    float integral_limit;       // 积分限幅
    float output_limit;         // 输出限幅

    float output;               // 当前输出值
} PID_TypeDef;

/* ======================== PID 默认参数 ======================== */

// 直立环（内环）
#define PID_BALANCE_KP          150.0f
#define PID_BALANCE_KI          0.8f
#define PID_BALANCE_KD          3.5f
#define PID_BALANCE_ILIMIT      200.0f
#define PID_BALANCE_OLIMIT      800.0f

// 速度环（外环）
#define PID_SPEED_KP            40.0f
#define PID_SPEED_KI            0.2f
#define PID_SPEED_KD            0.0f
#define PID_SPEED_ILIMIT        50.0f
#define PID_SPEED_OLIMIT        200.0f

// 转向环
#define PID_TURN_KP             65.0f
#define PID_TURN_KI             0.0f
#define PID_TURN_KD             0.0f
#define PID_TURN_ILIMIT         50.0f
#define PID_TURN_OLIMIT         300.0f

/* ======================== 全局 PID 实例 ======================== */

extern PID_TypeDef g_pidBalance;   // 直立环
extern PID_TypeDef g_pidSpeed;     // 速度环
extern PID_TypeDef g_pidTurn;      // 转向环

/* ======================== 函数声明 ======================== */

// 初始化PID参数为默认值
void PID_Init(PID_TypeDef *pid, float kp, float ki, float kd,
              float integral_limit, float output_limit);

// PID计算函数（位置式PID）
// pid: PID结构体指针, error: 当前误差（目标值 - 当前值）
// 返回: 控制输出值
float PID_Calc(PID_TypeDef *pid, float error);

// 重置PID（清零积分和上次误差）
void PID_Reset(PID_TypeDef *pid);

// 串级PID控制（每1ms调用一次）
// target_speed: 目标速度, current_pitch: 当前倾角
// gyro_y: 陀螺仪Y轴角速度, left_speed/right_speed: 左右轮速
void PID_CascadeControl(float target_speed, float current_pitch, float gyro_y,
                        float left_speed, float right_speed);

#endif /* __PID_H */