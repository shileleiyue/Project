#ifndef __MPU6050_H
#define __MPU6050_H

#include "main.h"

/* ======================== MPU6050 寄存器地址 ======================== */

#define MPU6050_SMPLRT_DIV      0x19    // 采样率分频
#define MPU6050_CONFIG          0x1A    // 配置寄存器
#define MPU6050_GYRO_CONFIG     0x1B    // 陀螺仪配置
#define MPU6050_ACCEL_CONFIG    0x1C    // 加速度计配置
#define MPU6050_ACCEL_XOUT_H    0x3B    // 加速度计X轴高8位（数据起始寄存器）
#define MPU6050_TEMP_OUT_H      0x41    // 温度高8位
#define MPU6050_GYRO_XOUT_H     0x43    // 陀螺仪X轴高8位
#define MPU6050_PWR_MGMT_1      0x6B    // 电源管理1
#define MPU6050_WHO_AM_I        0x75    // 设备ID寄存器

/* ======================== 数据结构 ======================== */

typedef struct {
    int16_t accel_x;
    int16_t accel_y;
    int16_t accel_z;
    int16_t temp;
    int16_t gyro_x;
    int16_t gyro_y;
    int16_t gyro_z;
} MPU6050_DataRaw_t;

typedef struct {
    float accel_x;      // 单位 g
    float accel_y;
    float accel_z;
    float temp;         // 单位 °C
    float gyro_x;       // 单位 °/s
    float gyro_y;
    float gyro_z;
} MPU6050_DataScaled_t;

/* ======================== 函数声明 ======================== */

// MPU6050 初始化（返回0成功，非0失败）
uint8_t MPU6050_Init(I2C_HandleTypeDef *hi2c);

// 一次性读取所有原始数据
void MPU6050_ReadAll(MPU6050_DataRaw_t *raw);

// 将原始数据换算为物理量
void MPU6050_ScaleData(const MPU6050_DataRaw_t *raw, MPU6050_DataScaled_t *scaled);

// 从加速度计数据计算俯仰角（Pitch）
float MPU6050_CalcAccPitch(float ax, float ay, float az);

// 互补滤波解算角度
// gyro_rate: 陀螺仪角速度(°/s), acc_angle: 加速度计角度(°), dt: 采样间隔(s)
float MPU6050_ComplementaryFilter(float gyro_rate, float acc_angle, float dt);

// 读取设备ID（用于验证连接）
uint8_t MPU6050_ReadID(void);

// 设置陀螺仪量程
void MPU6050_SetGyroRange(uint8_t range);

// 设置加速度计量程
void MPU6050_SetAccelRange(uint8_t range);

#endif /* __MPU6050_H */