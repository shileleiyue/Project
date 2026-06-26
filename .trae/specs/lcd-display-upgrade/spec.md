# LCD 字体升级 + 串口调试修复 + 状态指示完善 — 规格说明书

## Why
`lcd-serial-fix` 实施后仍存在以下问题：
1. LCD 使用 5×7 ASCII 字模渲染在 8×16 单元格中，字符仅占屏幕宽度的 62.5%、高度的 43.75%，实际观感仅约占屏幕 2/3
2. 串口通信仅显示终端本地回显，MCU 未实际响应串口指令（S/P/T/C/M），可能是 UART 中断未触发或配置问题
3. 用户烧录后无法判断程序运行状态，虽有 LED/蜂鸣器但缺乏直观的上电自检流程
4. 分压比已改为 4.0，但需确认生效

## What Changes
- 修改 `lcd_jlx12864g.c`：将 5×7 ASCII 字库替换为 8×16 字库（每字符 16 字节），修改 `LCD_ShowChar` 适配新字库
- 修改 `lcd_display.c`：适配新字体后的显示布局（每行仍为 16 字符，但字符更大更清晰）
- 修改 `main.c`：增加上电自检序列（LED 依次亮 R→G→B→灭 → 蜂鸣器短响），确保用户可直观判断程序启动
- 确认/修复串口中断：在 `main.c` 上电后立即发送启动消息，验证 UART TX 正常；检查 USART1 RX 中断配置
- 更新 `SYSTEM_STATUS_GUIDE.md`：补充上电自检流程说明，增加各状态 LED/蜂鸣器/LCD 的详细时序描述
- **BREAKING**: 无

## Impact
- Affected specs: lcd-serial-fix, jlx12864g-lcd-display
- Affected code: `Core/Src/lcd_jlx12864g.c`, `Core/Src/lcd_display.c`, `Core/Src/main.c`, `Core/Src/stm32f1xx_it.c`, `SYSTEM_STATUS_GUIDE.md`
- 新增文件: 无

## MODIFIED Requirements

### Requirement: LCD 8×16 ASCII 字体显示
系统 SHALL 使用 8×16 像素 ASCII 字库渲染字符，充分利用 128×64 像素显示区域。

#### Scenario: 8×16 字体全屏显示
- **WHEN** 系统调用 `LCD_ShowChar` 或 `LCD_ShowString` 显示 ASCII 文本
- **THEN** 每个字符占据 8×16 像素（宽 8 列，高 2 页），字模数据为 16 字节/字符
- **THEN** 每行最多显示 16 个字符（128 / 8 = 16），共 4 行（64 / 16 = 4）
- **THEN** 字符清晰可辨，占满单元格

#### Scenario: 字库数据格式
- **WHEN** 定义 8×16 ASCII 字库
- **THEN** 每字符 16 字节，前 8 字节为上半页（page y），后 8 字节为下半页（page y+1）
- **THEN** 字库覆盖 0x20-0x7E（95 个可打印 ASCII 字符），总大小 95 × 16 = 1520 字节

### Requirement: 上电自检序列
系统 SHALL 在上电后执行自检序列，通过 LED 和蜂鸣器明确指示启动状态。

#### Scenario: 上电自检 LED 序列
- **WHEN** 系统上电复位后进入 `main()` 函数
- **THEN** LED 依次执行：红色亮 200ms → 绿色亮 200ms → 蓝色亮 200ms → 全灭 200ms
- **THEN** 自检通过后蜂鸣器短响 1 声（100ms）
- **THEN** 自检序列完成后进入正常状态指示

#### Scenario: 自检序列含义
- **WHEN** 用户观察上电自检序列
- **THEN** LED 依次亮 R→G→B = LED 硬件正常，程序已启动
- **THEN** LED 全灭 + 蜂鸣器响 = 自检通过，进入初始化
- **THEN** LED 停在红色 = 自检失败（MPU6050 或外设故障）

### Requirement: 串口启动验证
系统 SHALL 在上电后立即通过串口发送启动消息，验证 UART TX 功能正常。

#### Scenario: 启动消息发送
- **WHEN** 系统完成 UART 初始化
- **THEN** 立即发送 "\r\n=== STM32 Balance Car ===\r\n" 标识消息
- **THEN** 发送 "System init OK!\r\n" 或 "MPU6050 init failed!\r\n"
- **THEN** 用户可通过串口助手确认 MCU 是否正常响应

## ADDED Requirements

### Requirement: 系统状态指示详细时序
系统 SHALL 在 `SYSTEM_STATUS_GUIDE.md` 中提供各状态的完整时序描述。

#### Scenario: 各状态时序描述
- **WHEN** 用户查阅 SYSTEM_STATUS_GUIDE.md
- **THEN** 每个状态包含：LED 颜色/模式/时序、蜂鸣器模式/时序、LCD 显示内容、持续时间、触发条件、退出条件
- **THEN** 包含烧录后判断流程：从 LED 自检 → 蜂鸣器确认 → LCD 显示 → 串口验证的完整步骤