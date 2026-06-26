/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : 自平衡小车主程序头文件 - 引脚定义、系统参数、全局变量声明
  ******************************************************************************
  */
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f1xx_hal.h"

/* USER CODE BEGIN Includes */
#include <stdio.h>
#include <string.h>
#include <math.h>
/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* ======================== 系统状态枚举 ======================== */

typedef enum {
    SYSTEM_INIT      = 0,   // 初始化
    SYSTEM_STARTUP   = 1,   // 启动中
    SYSTEM_BALANCING = 2,   // 平衡中
    SYSTEM_LOW_BAT   = 3,   // 低电量
    SYSTEM_FALLEN    = 4,   // 摔倒保护
    SYSTEM_SLEEP     = 5,   // 休眠
    SYSTEM_ERROR     = 6    // 错误
} SystemState_t;

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* ======================== 引脚定义 ======================== */

// 左电机 PWM - PA2 (TIM2_CH3)
// 注意：TIM2 混合模式，CH1/CH2 用于编码器，CH3/CH4 用于 PWM
#define LEFT_MOTOR_PWM_PORT       GPIOA
#define LEFT_MOTOR_PWM_PIN        GPIO_PIN_2
#define LEFT_MOTOR_PWM_TIM        TIM2
#define LEFT_MOTOR_PWM_CHANNEL    TIM_CHANNEL_3

// 左电机方向 - PB0, PB1
#define LEFT_MOTOR_DIR1_PORT      GPIOB
#define LEFT_MOTOR_DIR1_PIN       GPIO_PIN_0
#define LEFT_MOTOR_DIR2_PORT      GPIOB
#define LEFT_MOTOR_DIR2_PIN       GPIO_PIN_1

// 右电机 PWM - PA3 (TIM2_CH4)
#define RIGHT_MOTOR_PWM_PORT      GPIOA
#define RIGHT_MOTOR_PWM_PIN       GPIO_PIN_3
#define RIGHT_MOTOR_PWM_TIM       TIM2
#define RIGHT_MOTOR_PWM_CHANNEL   TIM_CHANNEL_4

// 右电机方向 - PB12, PB13
#define RIGHT_MOTOR_DIR1_PORT     GPIOB
#define RIGHT_MOTOR_DIR1_PIN      GPIO_PIN_12
#define RIGHT_MOTOR_DIR2_PORT     GPIOB
#define RIGHT_MOTOR_DIR2_PIN      GPIO_PIN_13

// 左编码器 - PA0 (TIM2_CH1), PA1 (TIM2_CH2)
#define LEFT_ENCODER_TIM          TIM2
#define LEFT_ENCODER_CH1_PIN      GPIO_PIN_0
#define LEFT_ENCODER_CH2_PIN      GPIO_PIN_1

// 右编码器 - PB4 (TIM3_CH1), PB5 (TIM3_CH2)
#define RIGHT_ENCODER_TIM         TIM3
#define RIGHT_ENCODER_CH1_PIN     GPIO_PIN_4
#define RIGHT_ENCODER_CH2_PIN     GPIO_PIN_5

// MPU6050 - I2C1: PB6(SCL), PB7(SDA)
#define MPU6050_I2C               hi2c1
#define MPU6050_ADDR              0x68

// RGB LED - PB14(R), PB15(G), PB8(B)
// 注意：STM32F103C8T6(LQFP48) 没有 PC0~PC2 引脚，改用 PB 空闲引脚
#define LED_R_PORT                GPIOB
#define LED_R_PIN                 GPIO_PIN_14
#define LED_G_PORT                GPIOB
#define LED_G_PIN                 GPIO_PIN_15
#define LED_B_PORT                GPIOB
#define LED_B_PIN                 GPIO_PIN_8

// 蜂鸣器 - PB3（SWD 模式下 JTDO 空闲，可用作 GPIO）
#define BUZZER_PORT               GPIOB
#define BUZZER_PIN                GPIO_PIN_3

// UART1 - 蓝牙/调试: PA9(TX), PA10(RX)
#define UART_DEBUG                huart1

// UART2 - 语音模块: PB10(TX), PB11(RX)
#define UART_VOICE                huart2

/* ======================== 系统参数 ======================== */

// 控制频率 1kHz
#define CONTROL_FREQ_HZ           1000
#define CONTROL_PERIOD_MS         1

// PWM 参数
#define PWM_PERIOD                1000
#define PWM_MAX_OUTPUT            1000
#define PWM_MIN_OUTPUT            -1000

// 编码器参数（根据实际编码器修改）
#define ENCODER_PPR               390       // 编码器线数
#define WHEEL_DIAMETER_MM         65        // 轮径 mm
#define WHEEL_CIRCUMFERENCE_MM    (WHEEL_DIAMETER_MM * 3.14159f)

// 摔倒保护阈值
#define FALL_TILT_THRESHOLD       45.0f     // 倾角超过45度认为摔倒
#define BATTERY_LOW_THRESHOLD     3.5f      // 低电量阈值（单节锂电）

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

/* Exported functions prototypes ---------------------------------------------*/
void SystemClock_Config(void);
void MX_GPIO_Init(void);
void MX_I2C1_Init(void);
void MX_TIM2_Init(void);
void MX_TIM3_Init(void);
void MX_TIM4_Init(void);
void MX_USART1_UART_Init(void);
void MX_USART2_UART_Init(void);
void MX_ADC1_Init(void);
void Error_Handler(void);

/* USER CODE BEGIN EFP */
/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* USER CODE BEGIN 1 */

/* ======================== 全局变量声明 ======================== */

extern SystemState_t g_system_state;
extern float g_pitch_angle;         // 当前倾角
extern float g_left_speed;          // 左轮速度
extern float g_right_speed;         // 右轮速度
extern float g_target_speed;        // 目标速度
extern float g_target_turn;         // 目标转向
extern float g_battery_voltage;     // 电池电压
extern uint32_t g_sys_tick_ms;      // 系统运行毫秒

/* ======================== 外设句柄声明 ======================== */

extern ADC_HandleTypeDef    hadc1;   // 电池电压检测
extern I2C_HandleTypeDef    hi2c1;
extern TIM_HandleTypeDef    htim1;   // 1kHz控制定时器
extern TIM_HandleTypeDef    htim2;   // 左编码器
extern TIM_HandleTypeDef    htim3;   // 右编码器
extern TIM_HandleTypeDef    htim4;   // 保留，当前未使用
extern UART_HandleTypeDef   huart1;  // 调试/蓝牙
extern UART_HandleTypeDef   huart2;  // 语音模块

/* USER CODE END 1 */

#ifdef __cplusplus
}
#endif
#endif /* __MAIN_H */