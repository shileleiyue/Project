#ifndef __INDICATOR_H
#define __INDICATOR_H

#include "main.h"

/* ======================== RGB 颜色定义 ======================== */

#define RGB_OFF     0x000   // 全灭
#define RGB_RED     0x001   // 红色
#define RGB_GREEN   0x002   // 绿色
#define RGB_BLUE    0x004   // 蓝色
#define RGB_YELLOW  0x003   // 红+绿=黄
#define RGB_CYAN    0x006   // 绿+蓝=青
#define RGB_PURPLE  0x005   // 红+蓝=紫
#define RGB_WHITE   0x007   // 全亮=白

/* ======================== 状态-颜色映射 ======================== */

// 初始化: 蓝色
// 平衡中: 绿色
// 低电量: 黄色（闪烁）
// 摔倒: 红色
// 休眠: 熄灭
// 错误: 红色（闪烁）

/* ======================== 函数声明 ======================== */

// 初始化指示灯和蜂鸣器GPIO
void Indicator_Init(void);

// 设置RGB颜色
// color: RGB_RED, RGB_GREEN, RGB_BLUE 等的组合
void Indicator_SetColor(uint16_t color);

// 设置RGB颜色并闪烁
// color: 颜色, period_ms: 闪烁周期（ms）
void Indicator_SetBlink(uint16_t color, uint16_t period_ms);

// 关闭指示灯
void Indicator_Off(void);

// 蜂鸣器控制
void Buzzer_On(void);
void Buzzer_Off(void);
void Buzzer_Beep(uint16_t duration_ms);

// 根据系统状态更新指示灯
void Indicator_UpdateByState(SystemState_t state);

// 指示灯主处理（在主循环中调用，处理闪烁）
void Indicator_Process(void);

#endif /* __INDICATOR_H */