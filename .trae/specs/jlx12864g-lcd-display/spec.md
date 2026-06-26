# JLX12864G-086 LCD 显示屏集成 — 规格说明书

## Why
平衡小车当前仅通过串口输出调试信息，不便于在脱离电脑时查看电池电压、速度、PID 参数等关键信息。集成 JLX12864G-086 带中文字库的 128×64 点阵 LCD 可提供两种显示模式：正常使用模式（显示速度、电压等基本信息）和调参模式（显示 PID 参数、传感器原始数据），方便现场调试和日常使用。

## What Changes
- 新增 `lcd_jlx12864g.c` / `lcd_jlx12864g.h`：软件模拟 SPI 驱动 LCD 控制器 (UC1701X/ST7565R) 及中文字库 IC (JLX-GB2312)
- 新增 `lcd_display.c` / `lcd_display.h`：封装两种显示模式（正常模式、调参模式）的页面渲染逻辑
- 修改 `main.c`：初始化 LCD，在主循环中定时刷新 LCD 显示
- 修改 `uart_protocol.h` / `uart_protocol.c`：新增 'M' 指令切换显示模式
- 修改 `main.h`：新增 LCD 引脚宏定义
- 更新 `WIRING_GUIDE.md`：补充 LCD 接线章节
- **BREAKING**: 无

## Impact
- Affected specs: stm32-firmware-rewrite
- Affected code: `Core/Src/main.c`, `Core/Inc/main.h`, `Core/Src/uart_protocol.c`, `Core/Inc/uart_protocol.h`, `WIRING_GUIDE.md`
- 新增文件: `Core/Src/lcd_jlx12864g.c`, `Core/Inc/lcd_jlx12864g.h`, `Core/Src/lcd_display.c`, `Core/Inc/lcd_display.h`

## ADDED Requirements

### Requirement: LCD 硬件驱动
系统 SHALL 通过软件模拟 SPI 驱动 JLX12864G-086 液晶模块，包括 UC1701X/ST7565R 显示控制器和中文字库 IC (JLX-GB2312)。

#### Scenario: LCD 初始化成功
- **WHEN** 系统上电并执行 `LCD_Init()`
- **THEN** LCD 清屏，背光点亮，显示就绪

#### Scenario: LCD 写指令
- **WHEN** 调用 `LCD_WriteCmd(uint8_t cmd)`
- **THEN** RS 引脚拉低，CS 拉低，通过 SCLK/SDA 发送 8 位指令，CS 拉高

#### Scenario: LCD 写数据
- **WHEN** 调用 `LCD_WriteData(uint8_t data)`
- **THEN** RS 引脚拉高，CS 拉低，通过 SCLK/SDA 发送 8 位数据，CS 拉高

#### Scenario: 中文字库读取
- **WHEN** 调用 `LCD_ReadFont(uint8_t *buffer, uint32_t offset, uint16_t len)`
- **THEN** 通过 ROM_CS/ROM_SCK/ROM_SI 从字库 IC 读取指定偏移的 GB2312 字模数据

#### Scenario: 引脚分配
- **WHEN** 系统定义 LCD 引脚宏
- **THEN** 使用以下空闲引脚，不与现有外设冲突：
  - LCD_CS → PA5, LCD_RST → PA6, LCD_RS → PA7
  - LCD_SCLK → PA8, LCD_SDA → PA11
  - ROM_CS → PA12, ROM_SCK → PA15, ROM_SI → PB9

### Requirement: 正常使用模式显示
系统 SHALL 在正常使用模式下，在 LCD 上显示小车基本运行信息。

#### Scenario: 正常模式显示内容
- **WHEN** 系统处于正常使用模式且每 200ms 刷新一次
- **THEN** LCD 显示以下内容：
  - 第 1 行：标题 "平衡小车" 或系统状态文字
  - 第 2 行：速度 (cm/s) 和电池电压 (V)
  - 第 3 行：倾角 (度) 和转向值
  - 第 4 行：运行时间或状态指示

#### Scenario: 不同系统状态下的显示
- **WHEN** 系统状态为 SYSTEM_BALANCING
- **THEN** 显示速度、倾角、电压等实时数据
- **WHEN** 系统状态为 SYSTEM_ERROR
- **THEN** 显示 "系统错误" 及错误原因
- **WHEN** 系统状态为 SYSTEM_LOW_BAT
- **THEN** 显示 "电量不足" 及当前电压

### Requirement: 调参模式显示
系统 SHALL 在调参模式下，在 LCD 上显示 PID 参数和传感器原始数据，便于现场调试。

#### Scenario: 调参模式显示内容
- **WHEN** 系统处于调参模式且每 200ms 刷新一次
- **THEN** LCD 显示以下内容：
  - 第 1 行：标题 "调参模式" 及模式提示
  - 第 2 行：平衡环 PID 参数 (Kp, Ki, Kd)
  - 第 3 行：速度环 PID 参数 (Kp, Ki, Kd) 或转向环参数
  - 第 4 行：加速度计原始值 (X, Y, Z)

### Requirement: 显示模式切换
系统 SHALL 支持通过串口指令 'M' 在正常模式和调参模式之间切换。

#### Scenario: 串口切换模式
- **WHEN** 用户通过串口发送 'M' 指令
- **THEN** 系统在正常模式和调参模式之间切换
- **THEN** LCD 立即刷新为新模式的内容
- **THEN** 串口回复 "Mode: Normal" 或 "Mode: Tuning"

## Pin 冲突检查

| 引脚 | 当前用途 | LCD 用途 | 冲突 |
|------|----------|----------|------|
| PA5 | 空闲 | LCD_CS | 无 |
| PA6 | 空闲 | LCD_RST | 无 |
| PA7 | 空闲 | LCD_RS | 无 |
| PA8 | 空闲 | LCD_SCLK | 无 |
| PA11 | 空闲 | LCD_SDA | 无 |
| PA12 | 空闲 | ROM_CS | 无 |
| PA15 | 空闲 | ROM_SCK | 无 |
| PB9 | 空闲 | ROM_SI | 无 |

> 所有 8 个引脚均为空闲引脚，与现有外设（电机、编码器、MPU6050、LED、蜂鸣器、UART、ADC、SWD）无冲突。