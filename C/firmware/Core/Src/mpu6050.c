/**
 * @file    mpu6050.c
 * @brief   MPU6050 姿态传感器驱动
 * @note    I2C接口, 设备地址 0x68
 *          加速度计量程: ±2g (灵敏度 16384 LSB/g)
 *          陀螺仪量程: ±250°/s (灵敏度 131 LSB/°/s)
 */

#include "mpu6050.h"

static I2C_HandleTypeDef *mpu_i2c;

/* ======================== 内部函数 ======================== */

/**
 * @brief 写一个字节到MPU6050寄存器
 */
static void MPU6050_WriteReg(uint8_t reg, uint8_t data)
{
    HAL_I2C_Mem_Write(mpu_i2c, MPU6050_ADDR << 1,
                      reg, I2C_MEMADD_SIZE_8BIT, &data, 1, 100);
}

/**
 * @brief 从MPU6050寄存器读取连续字节
 */
void MPU6050_ReadRegs(uint8_t reg, uint8_t *buf, uint8_t len)
{
    HAL_I2C_Mem_Read(mpu_i2c, MPU6050_ADDR << 1,
                     reg, I2C_MEMADD_SIZE_8BIT, buf, len, 100);
}

/* ======================== 公开函数 ======================== */

/**
 * @brief MPU6050 初始化
 * @param hi2c I2C句柄指针
 * @return 0=成功, 1=失败
 */
uint8_t MPU6050_Init(I2C_HandleTypeDef *hi2c)
{
    uint8_t id = 0;
    mpu_i2c = hi2c;

    // 检查设备ID（应为0x68）
    MPU6050_ReadRegs(MPU6050_WHO_AM_I, &id, 1);
    if (id != 0x68)
        return 1;

    // 退出睡眠模式
    // 寄存器0x6B: 位6=1进入睡眠, 写0x00退出睡眠
    MPU6050_WriteReg(MPU6050_PWR_MGMT_1, 0x00);
    HAL_Delay(10);

    // 设置采样率分频: 采样率 = 1kHz / (1 + SMPLRT_DIV)
    // 这里设为0, 即1kHz采样率
    MPU6050_WriteReg(MPU6050_SMPLRT_DIV, 0x00);

    // 配置寄存器: 设置数字低通滤波器(DLPF)
    // 0x00 = 260Hz, 0x01 = 184Hz, 0x02 = 94Hz,
    // 0x03 = 44Hz, 0x04 = 21Hz, 0x05 = 10Hz, 0x06 = 5Hz
    // 平衡车推荐 44Hz (0x03)
    MPU6050_WriteReg(MPU6050_CONFIG, 0x03);

    // 设置陀螺仪量程: ±250°/s (0x00)
    MPU6050_WriteReg(MPU6050_GYRO_CONFIG, 0x00);

    // 设置加速度计量程: ±2g (0x00)
    MPU6050_WriteReg(MPU6050_ACCEL_CONFIG, 0x00);

    return 0;
}

/**
 * @brief 一次性读取所有原始数据
 * @param raw 输出数据结构指针
 */
void MPU6050_ReadAll(MPU6050_DataRaw_t *raw)
{
    uint8_t buf[14];

    // 从寄存器0x3B开始连续读取14字节
    MPU6050_ReadRegs(MPU6050_ACCEL_XOUT_H, buf, 14);

    // 加速度计数据（高8位<<8 | 低8位）
    raw->accel_x = (int16_t)(buf[0] << 8 | buf[1]);
    raw->accel_y = (int16_t)(buf[2] << 8 | buf[3]);
    raw->accel_z = (int16_t)(buf[4] << 8 | buf[5]);

    // 温度数据
    raw->temp = (int16_t)(buf[6] << 8 | buf[7]);

    // 陀螺仪数据
    raw->gyro_x = (int16_t)(buf[8] << 8 | buf[9]);
    raw->gyro_y = (int16_t)(buf[10] << 8 | buf[11]);
    raw->gyro_z = (int16_t)(buf[12] << 8 | buf[13]);
}

/**
 * @brief 将原始数据换算为物理量
 * @param raw 原始数据指针
 * @param scaled 换算后数据指针
 */
void MPU6050_ScaleData(const MPU6050_DataRaw_t *raw, MPU6050_DataScaled_t *scaled)
{
    // 加速度: ±2g量程, 灵敏度 16384 LSB/g
    scaled->accel_x = (float)raw->accel_x / 16384.0f;
    scaled->accel_y = (float)raw->accel_y / 16384.0f;
    scaled->accel_z = (float)raw->accel_z / 16384.0f;

    // 温度: 温度 = 原始值/340 + 36.53 (°C)
    scaled->temp = (float)raw->temp / 340.0f + 36.53f;

    // 陀螺仪: ±250°/s量程, 灵敏度 131 LSB/°/s
    scaled->gyro_x = (float)raw->gyro_x / 131.0f;
    scaled->gyro_y = (float)raw->gyro_y / 131.0f;
    scaled->gyro_z = (float)raw->gyro_z / 131.0f;
}

/**
 * @brief 从加速度计数据计算俯仰角（Pitch）
 * @param ax 加速度X轴分量 (g)
 * @param ay 加速度Y轴分量 (g)
 * @param az 加速度Z轴分量 (g)
 * @return 俯仰角 (度)
 */
float MPU6050_CalcAccPitch(float ax, float ay, float az)
{
    // atan2(-ax, sqrt(ay^2 + az^2)) * 180/pi
    return atan2f(-ax, sqrtf(ay * ay + az * az)) * 57.2958f;
}

/**
 * @brief 互补滤波解算角度
 *        短期信任陀螺仪（积分），长期信任加速度计
 * @param gyro_rate 陀螺仪角速度 (°/s)
 * @param acc_angle 加速度计计算的角度 (°)
 * @param dt 采样时间间隔 (s)
 * @return 融合后的角度 (°)
 */
float MPU6050_ComplementaryFilter(float gyro_rate, float acc_angle, float dt)
{
    static float pitch = 0.0f;
    static uint8_t first_run = 1;

    // 第一次运行时用加速度计角度初始化
    if (first_run)
    {
        pitch = acc_angle;
        first_run = 0;
        return pitch;
    }

    // 陀螺仪积分：角度 = 上次角度 + 角速度 * 时间
    float gyro_angle = pitch + gyro_rate * dt;

    // 互补融合：0.98 信任陀螺仪，0.02 信任加速度计
    pitch = 0.98f * gyro_angle + 0.02f * acc_angle;

    return pitch;
}

/**
 * @brief 读取MPU6050设备ID
 * @return 设备ID (应为0x68)
 */
uint8_t MPU6050_ReadID(void)
{
    uint8_t id = 0;
    MPU6050_ReadRegs(MPU6050_WHO_AM_I, &id, 1);
    return id;
}

/**
 * @brief 设置陀螺仪量程
 * @param range 0=±250°/s, 1=±500°/s, 2=±1000°/s, 3=±2000°/s
 */
void MPU6050_SetGyroRange(uint8_t range)
{
    MPU6050_WriteReg(MPU6050_GYRO_CONFIG, range & 0x03);
}

/**
 * @brief 设置加速度计量程
 * @param range 0=±2g, 1=±4g, 2=±8g, 3=±16g
 */
void MPU6050_SetAccelRange(uint8_t range)
{
    MPU6050_WriteReg(MPU6050_ACCEL_CONFIG, range & 0x03);
}