# LCD 显示修复 + 串口通信修复 + 状态指示优化 — 规格说明书

## Why
JLX12864G-086 LCD 显示屏集成后存在以下问题：
1. LCD 显示内容仅占屏幕 2/3 宽度，未充分利用 128×64 像素
2. 串口指令（S/P/T/C/M）无响应，仅回显字符，无法控制小车
3. 分压比仍为 2.0，用户实际使用 4.0
4. 缺少系统状态指示说明（LED 颜色/闪烁 + 蜂鸣器行为），用户烧录后无法判断程序是否正常运行

## What Changes
- 修复 `lcd_jlx12864g.c`：LCD 初始化序列，确保 128 列全部可寻址；修复 LCD_ShowChar 字符宽度为 8 像素
- 修复 `lcd_display.c`：使用 8×16 ASCII 字体充分利用屏幕宽度，每行显示更多信息
- 修复 `main.c`：调整 LCD 初始化顺序，确保 UART 中断正常工作
- 修改 `power_manager.h`：分压比从 2.0 改为 4.0
- 新增 `SYSTEM_STATUS_GUIDE.md`：详细描述各系统状态下 LED 颜色、闪烁模式、蜂鸣器行为
- 修改 `indicator.c`：在系统状态切换时增加蜂鸣器提示
- 更新 `WIRING_GUIDE.md`：更新分压比说明
- **BREAKING**: 无

## Impact
- Affected specs: jlx12864g-lcd-display
- Affected code: `Core/Src/lcd_jlx12864g.c`, `Core/Src/lcd_display.c`, `Core/Src/main.c`, `Core/Inc/power_manager.h`, `Core/Src/indicator.c`, `Core/Inc/indicator.h`, `WIRING_GUIDE.md`
- 新增文件: `SYSTEM_STATUS_GUIDE.md`

## MODIFIED Requirements

### Requirement: LCD 全屏显示
系统 SHALL 利用 LCD 128×64 全部像素区域显示内容，每行使用 8×16 ASCII 字体占满 128 像素宽度（16 个字符）。

#### Scenario: 正常模式全屏显示
- **WHEN** 系统处于正常模式
- **THEN** 每行显示 16 个 ASCII 字符（8×16 字体），充分利用 128 像素宽度
- **THEN** 第 1 行：显示系统状态标题（居中）
- **THEN** 第 2 行：左轮速度 + 右轮速度
- **THEN** 第 3 行：倾角 + 电池电压
- **THEN** 第 4 行：目标速度 + 转向值

#### Scenario: 调参模式全屏显示
- **WHEN** 系统处于调参模式
- **THEN** 第 1 行："-- Tuning Mode --"
- **THEN** 第 2 行：平衡环 Kp/Ki/Kd
- **THEN** 第 3 行：速度环 Kp/Ki/Kd
- **THEN** 第 4 行：转向环 Kp/Ki/Kd

### Requirement: 串口指令正常响应
系统 SHALL 正确响应所有串口单字符指令（S/P/T/C/M），发送指令后立即收到确认回复。

#### Scenario: 串口指令响应
- **WHEN** 用户通过串口发送 'S'
- **THEN** 系统立即回复 "Balancing started." 或 "System error, cannot start." 等状态消息
- **WHEN** 用户发送 'P'
- **THEN** 系统回复传感器数据 "A:XX|S:XX|V:XX|B:X"
- **WHEN** 用户发送 'M'
- **THEN** 系统切换显示模式并回复 "Mode: Normal" 或 "Mode: Tuning"
- **WHEN** 用户发送 'T'
- **THEN** 系统回复 "System sleep."

### Requirement: 分压比配置
系统 SHALL 使用分压比 4.0 计算电池电压，支持 3S 锂电池（最高 12.6V）。

#### Scenario: 电池电压计算
- **WHEN** ADC 读取 PA4 电压值
- **THEN** 电池电压 = ADC 电压 × 4.0（分压比）
- **THEN** 3S 锂电池 12.6V 时 PA4 = 3.15V（安全，不超 3.3V）

## ADDED Requirements

### Requirement: 系统状态指示
系统 SHALL 通过 RGB LED 和蜂鸣器明确指示当前系统状态，使用户烧录后无需串口即可判断程序运行状态。

#### Scenario: 各状态指示行为

| 状态 | LED 颜色 | LED 模式 | 蜂鸣器 |
|------|----------|----------|--------|
| SYSTEM_INIT | 蓝色 | 常亮 | 短响 1 声（100ms） |
| SYSTEM_STARTUP | 蓝色 | 常亮 | 短响 2 声（表示就绪） |
| SYSTEM_BALANCING | 绿色 | 常亮 | 无 |
| SYSTEM_LOW_BAT | 黄色 | 慢闪（500ms） | 每 5s 短响 1 声 |
| SYSTEM_FALLEN | 红色 | 常亮 | 长响 500ms 后停止 |
| SYSTEM_SLEEP | 熄灭 | — | 无 |
| SYSTEM_ERROR | 红色 | 快闪（200ms） | 连续短响 3 声后停止 |

#### Scenario: 烧录后判断程序运行
- **WHEN** 烧录完成后上电
- **THEN** LED 蓝色常亮 = 程序正常启动
- **THEN** LED 蓝色常亮 + 蜂鸣器短响 2 声 = 初始化完成，等待启动
- **THEN** LED 红色快闪 = 系统错误（MPU6050 或外设故障）
- **THEN** LED 熄灭 = 程序未运行或硬件故障

### Requirement: 烧录后运行状态判断文档
系统 SHALL 提供 `SYSTEM_STATUS_GUIDE.md` 文档，详细描述单片机程序运行的各种状态及对应的灯光、蜂鸣器、LCD 显示反应。

## Pin 冲突检查

无新增引脚占用，现有引脚分配无冲突。