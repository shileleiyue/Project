/**
 * @file    motor.c
 * @brief   电机驱动实现 (TB6612FNG)
 * @note    使用TIM2产生PWM控制左右电机 (CH3/CH4)
 *          TIM2混合模式: CH1/CH2 编码器, CH3/CH4 PWM
 *          PWM频率: 1kHz
 *          方向控制: AIN1/AIN2 和 BIN1/BIN2
 */

#include "motor.h"

/* ======================== 全局电机实例 ======================== */

Motor_TypeDef g_motor_left;
Motor_TypeDef g_motor_right;

/* ======================== 函数实现 ======================== */

/**
 * @brief 初始化电机GPIO和PWM
 * PA2 = TIM2_CH3 (左电机PWM), PA3 = TIM2_CH4 (右电机PWM)
 * PB0, PB1 = 左电机方向, PB12, PB13 = 右电机方向
 */
void Motor_Init(void)
{
    // 左电机配置 (TIM2_CH3)
    g_motor_left.pwm_tim = &htim2;
    g_motor_left.pwm_channel = LEFT_MOTOR_PWM_CHANNEL;
    g_motor_left.dir1_port = LEFT_MOTOR_DIR1_PORT;
    g_motor_left.dir1_pin = LEFT_MOTOR_DIR1_PIN;
    g_motor_left.dir2_port = LEFT_MOTOR_DIR2_PORT;
    g_motor_left.dir2_pin = LEFT_MOTOR_DIR2_PIN;
    g_motor_left.current_pwm = 0;
    g_motor_left.speed = 0.0f;

    // 右电机配置 (TIM2_CH4)
    g_motor_right.pwm_tim = &htim2;
    g_motor_right.pwm_channel = RIGHT_MOTOR_PWM_CHANNEL;
    g_motor_right.dir1_port = RIGHT_MOTOR_DIR1_PORT;
    g_motor_right.dir1_pin = RIGHT_MOTOR_DIR1_PIN;
    g_motor_right.dir2_port = RIGHT_MOTOR_DIR2_PORT;
    g_motor_right.dir2_pin = RIGHT_MOTOR_DIR2_PIN;
    g_motor_right.current_pwm = 0;
    g_motor_right.speed = 0.0f;

    // 初始状态：刹车（两个方向引脚都输出低电平=刹车）
    Motor_StopAll();
}

/**
 * @brief 设置电机速度（PWM输出）
 * 
 * 方向控制逻辑:
 *   AIN1|AIN2  | 电机状态
 *   -----------|----------
 *   0     0    | 刹车
 *   1     0    | 正转（前进）
 *   0     1    | 反转（后退）
 *   1     1    | 刹车
 * 
 * @param motor 电机结构体指针
 * @param speed PWM值 (-1000 ~ 1000)
 *              >0 正转（前进）
 *              <0 反转（后退）
 *              =0 刹车
 */
void Motor_SetSpeed(Motor_TypeDef *motor, int16_t speed)
{
    // 限幅
    if (speed > PWM_MAX_OUTPUT) speed = PWM_MAX_OUTPUT;
    if (speed < PWM_MIN_OUTPUT) speed = PWM_MIN_OUTPUT;

    motor->current_pwm = speed;

    if (speed > 0)
    {
        // 正转：前进
        HAL_GPIO_WritePin(motor->dir1_port, motor->dir1_pin, GPIO_PIN_SET);
        HAL_GPIO_WritePin(motor->dir2_port, motor->dir2_pin, GPIO_PIN_RESET);
        // 设置PWM占空比
        __HAL_TIM_SET_COMPARE(motor->pwm_tim, motor->pwm_channel, speed);
    }
    else if (speed < 0)
    {
        // 反转：后退
        HAL_GPIO_WritePin(motor->dir1_port, motor->dir1_pin, GPIO_PIN_RESET);
        HAL_GPIO_WritePin(motor->dir2_port, motor->dir2_pin, GPIO_PIN_SET);
        // 设置PWM占空比（取绝对值）
        __HAL_TIM_SET_COMPARE(motor->pwm_tim, motor->pwm_channel, -speed);
    }
    else
    {
        // speed == 0: 刹车
        Motor_Brake(motor);
    }
}

/**
 * @brief 刹车（电机短接制动）
 * 两个方向引脚都输出高电平 = 电机两端短接 = 刹车
 */
void Motor_Brake(Motor_TypeDef *motor)
{
    HAL_GPIO_WritePin(motor->dir1_port, motor->dir1_pin, GPIO_PIN_SET);
    HAL_GPIO_WritePin(motor->dir2_port, motor->dir2_pin, GPIO_PIN_SET);
    __HAL_TIM_SET_COMPARE(motor->pwm_tim, motor->pwm_channel, 0);
    motor->current_pwm = 0;
}

/**
 * @brief 停止（不刹车，自由滑行）
 * 两个方向引脚都输出低电平 = 电机悬空 = 自由滑行
 */
void Motor_Stop(Motor_TypeDef *motor)
{
    HAL_GPIO_WritePin(motor->dir1_port, motor->dir1_pin, GPIO_PIN_RESET);
    HAL_GPIO_WritePin(motor->dir2_port, motor->dir2_pin, GPIO_PIN_RESET);
    __HAL_TIM_SET_COMPARE(motor->pwm_tim, motor->pwm_channel, 0);
    motor->current_pwm = 0;
}

/**
 * @brief 停止所有电机
 */
void Motor_StopAll(void)
{
    Motor_Stop(&g_motor_left);
    Motor_Stop(&g_motor_right);
}