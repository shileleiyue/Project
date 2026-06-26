# Tasks

- [x] Task 1: 修复 LCD 全屏显示
  - [x] 修复 LCD_ShowChar 函数：确保每个 ASCII 字符绘制为 8×16 像素（占满 2 个 page）
  - [x] 修复 LCD_ShowString 函数：确保每行显示 16 个 ASCII 字符（128 像素宽）
  - [x] 修改 lcd_display.c 正常模式：重新设计布局，每行显示更多信息（左轮速/右轮速、倾角/电压、目标速度/转向）
  - [x] 修改 lcd_display.c 调参模式：使用紧凑 ASCII 格式显示三环 PID 参数（每行一个环的 Kp/Ki/Kd）

- [x] Task 2: 修复串口通信
  - [x] 检查 main.c 中 UART 初始化顺序：将 HAL_UART_Receive_IT 移到 LCD_Init 之前
  - [x] 确认 HAL_UART_Receive_IT 在 LCD 初始化之前正确调用
  - [x] 验证 HAL_UART_RxCpltCallback 能正确触发
  - [x] 测试所有串口指令（S/P/T/C/M）的响应

- [x] Task 3: 更新分压比
  - [x] 修改 power_manager.h 中 VOLTAGE_DIVIDER_RATIO 从 2.0f 改为 4.0f
  - [x] 更新 WIRING_GUIDE.md 中分压比说明

- [x] Task 4: 增强系统状态指示
  - [x] 修改 indicator.c：在 Indicator_UpdateByState 中添加蜂鸣器提示
  - [x] 修改 indicator.h：添加蜂鸣器模式枚举（BEEP_SHORT, BEEP_LONG, BEEP_DOUBLE, BEEP_TRIPLE）
  - [x] 实现非阻塞蜂鸣器控制（Buzzer_Process 使用 HAL_GetTick 避免阻塞）
  - [x] 各状态切换时触发对应蜂鸣器提示

- [x] Task 5: 创建系统状态指示文档
  - [x] 创建 SYSTEM_STATUS_GUIDE.md：详细描述各状态下的 LED 颜色、闪烁模式、蜂鸣器行为、LCD 显示内容
  - [x] 添加烧录后判断程序是否正常运行的流程说明
  - [x] 添加常见故障的状态判断指南

# Task Dependencies
- Task 1 和 Task 2 可并行执行
- Task 3 独立执行
- Task 4 依赖 Task 1 和 Task 2（需要确保串口和 LCD 正常工作后再调蜂鸣器）
- Task 5 可并行执行