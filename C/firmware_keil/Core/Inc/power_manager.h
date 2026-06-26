#ifndef __POWER_MANAGER_H
#define __POWER_MANAGER_H

#include "main.h"

/* ======================== 电源管理参数 ======================== */

// 电池电压检测引脚（ADC）
#define BATTERY_ADC             hadc1

// 电压阈值（单节锂电池）
#define BATTERY_FULL_VOLTAGE    4.2f    // 满电电压
#define BATTERY_LOW_VOLTAGE     3.5f    // 低电量报警阈值
#define BATTERY_CRITICAL_VOLT   3.3f    // 临界电压（自动关机）

// 分压比（根据实际分压电阻计算）
// Vout = Vin * R2 / (R1 + R2)
#define VOLTAGE_DIVIDER_RATIO   2.0f    // 如果R1=R2，分压比=2

// 摔倒检测
#define FALL_TILT_THRESHOLD     45.0f   // 倾角超过45度认为摔倒
#define FALL_DETECT_TIME_MS     2000    // 持续2秒以上才触发摔倒保护

/* ======================== 函数声明 ======================== */

// 初始化电源管理（ADC初始化）
void Power_Init(void);

// 读取电池电压（V）
float Power_ReadBatteryVoltage(void);

// 检查电池状态
// 返回: 0=正常, 1=低电量, 2=临界
uint8_t Power_CheckBattery(void);

// 摔倒检测
// pitch: 当前倾角
// 返回: 0=正常, 1=摔倒
uint8_t Power_CheckFall(float pitch);

// 电源管理主处理（在主循环中调用）
void Power_Process(void);

#endif /* __POWER_MANAGER_H */