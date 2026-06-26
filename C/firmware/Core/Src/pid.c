/**
 * @file    pid.c
 * @brief   PID控制器实现
 * @note    包含三个PID环：直立环（内环）、速度环（外环）、转向环
 *          串级控制结构：速度环 → 直立环 → 转向环 → 电机PWM
 */

#include "pid.h"
#include "motor.h"

/* ======================== 全局PID实例 ======================== */

PID_TypeDef g_pidBalance;   // 直立环
PID_TypeDef g_pidSpeed;     // 速度环
PID_TypeDef g_pidTurn;      // 转向环

/* ======================== 函数实现 ======================== */

/**
 * @brief 初始化PID参数为默认值
 * @param pid PID结构体指针
 * @param kp 比例系数
 * @param ki 积分系数
 * @param kd 微分系数
 * @param integral_limit 积分限幅
 * @param output_limit 输出限幅
 */
void PID_Init(PID_TypeDef *pid, float kp, float ki, float kd,
              float integral_limit, float output_limit)
{
    pid->kp = kp;
    pid->ki = ki;
    pid->kd = kd;
    pid->integral = 0.0f;
    pid->last_error = 0.0f;
    pid->derivative = 0.0f;
    pid->integral_limit = integral_limit;
    pid->output_limit = output_limit;
    pid->output = 0.0f;
}

/**
 * @brief PID计算函数（位置式PID）
 * @param pid PID结构体指针
 * @param error 当前误差（目标值 - 当前值）
 * @return 控制输出值
 */
float PID_Calc(PID_TypeDef *pid, float error)
{
    // 比例项
    float p_out = pid->kp * error;

    // 积分项（带积分分离：误差太大时不积分）
    if (fabsf(error) < 100.0f)
    {
        pid->integral += error * pid->ki;

        // 积分限幅
        if (pid->integral > pid->integral_limit)
            pid->integral = pid->integral_limit;
        if (pid->integral < -pid->integral_limit)
            pid->integral = -pid->integral_limit;
    }

    // 微分项（如果外部没有赋值derivative，则使用误差差分）
    float d_term;
    if (pid->derivative != 0.0f)
    {
        // 使用外部提供的微分项（如陀螺仪角速度）
        d_term = pid->kd * pid->derivative;
        pid->derivative = 0.0f;  // 使用后清零
    }
    else
    {
        // 使用误差差分作为微分项
        d_term = pid->kd * (error - pid->last_error);
    }

    pid->last_error = error;

    // 合成输出
    float output = p_out + pid->integral + d_term;

    // 输出限幅
    if (output > pid->output_limit)
        output = pid->output_limit;
    if (output < -pid->output_limit)
        output = -pid->output_limit;

    pid->output = output;
    return output;
}

/**
 * @brief 重置PID（清零积分和上次误差）
 * @param pid PID结构体指针
 */
void PID_Reset(PID_TypeDef *pid)
{
    pid->integral = 0.0f;
    pid->last_error = 0.0f;
    pid->derivative = 0.0f;
    pid->output = 0.0f;
}

/**
 * @brief 串级PID控制（每1ms调用一次）
 * 
 * 控制结构：
 *   速度环（外环）：目标速度 → 输出"倾角偏置"
 *                       ↓
 *   直立环（内环）：目标倾角(0° + 偏置) → 输出"PWM控制量"
 *                       ↓
 *   转向环（叠加）：左右轮差速 → 修正PWM
 *                       ↓
 *                   电机输出
 * 
 * @param target_speed 目标速度（正数前进，负数后退）
 * @param current_pitch 当前倾角
 * @param gyro_y 陀螺仪Y轴角速度（用于直立环微分项）
 * @param left_speed 左轮速度
 * @param right_speed 右轮速度
 */
void PID_CascadeControl(float target_speed, float current_pitch, float gyro_y,
                        float left_speed, float right_speed)
{
    // ========== 1. 速度环计算（外环） ==========
    // 速度误差 = 目标速度 - 平均速度
    float speed_error = target_speed - (left_speed + right_speed) / 2.0f;
    PID_Calc(&g_pidSpeed, speed_error);

    // 速度环输出作为直立环的目标倾角偏置
    // 比如速度环输出 2°，表示小车需要前倾2°才能获得前进速度
    float target_pitch = g_pidSpeed.output;

    // ========== 2. 直立环计算（内环） ==========
    // 误差 = 目标倾角 - 实际倾角
    float balance_error = target_pitch - current_pitch;

    // 把角速度作为微分项直接加入，提高响应速度
    // 陀螺仪Y轴角速度 = 倾斜角速度（负反馈，抑制震荡）
    g_pidBalance.derivative = -gyro_y;

    PID_Calc(&g_pidBalance, balance_error);

    // ========== 3. 转向环计算 ==========
    // 转向误差 = 左轮速度 - 右轮速度（差速控制）
    float turn_error = left_speed - right_speed;
    PID_Calc(&g_pidTurn, turn_error);

    // ========== 4. 合成左右电机PWM输出 ==========
    // 左电机 = 直立控制力 - 转向控制力
    // 右电机 = 直立控制力 + 转向控制力
    int16_t left_pwm = (int16_t)(g_pidBalance.output - g_pidTurn.output);
    int16_t right_pwm = (int16_t)(g_pidBalance.output + g_pidTurn.output);

    // 限幅输出
    if (left_pwm > PWM_MAX_OUTPUT) left_pwm = PWM_MAX_OUTPUT;
    if (left_pwm < PWM_MIN_OUTPUT) left_pwm = PWM_MIN_OUTPUT;
    if (right_pwm > PWM_MAX_OUTPUT) right_pwm = PWM_MAX_OUTPUT;
    if (right_pwm < PWM_MIN_OUTPUT) right_pwm = PWM_MIN_OUTPUT;

    // 输出到电机
    Motor_SetSpeed(&g_motor_left, left_pwm);
    Motor_SetSpeed(&g_motor_right, right_pwm);
}