# Tasks

- [x] Task 1: 替换 LCD 5×7 字库为 8×16 字库
  - [x] 编写 8×16 ASCII 字库数据（95 字符 × 16 字节 = 1520 字节），覆盖 0x20-0x7E
  - [x] 修改 `LCD_ShowChar` 函数：从 5 列字模 + 3 列空白改为 8 列字模，每页 8 字节
  - [x] 修改 `LCD_ShowNum` 函数：适配新的字符宽度（仍为 8 像素/字符，无需改动）
  - [x] 修改 `LCD_ShowFloat` 函数：适配新的字符宽度（无需改动）
  - [x] 验证全屏显示：每行 16 字符，共 4 行，字符清晰占满屏幕

- [x] Task 2: 增加上电自检序列
  - [x] 在 `main.c` 的 `main()` 函数开头（GPIO 初始化后）增加 LED 自检序列：R→G→B→灭，各 200ms
  - [x] 在自检序列末尾增加蜂鸣器短响 1 声（100ms）
  - [x] 确保自检序列在 LCD 初始化之前执行，让用户第一时间看到 LED 反馈

- [x] Task 3: 修复/验证串口通信
  - [x] 在 `main.c` 中 UART 初始化后立即发送 "=== STM32 Balance Car ===\r\n" 标识消息
  - [x] 检查 `stm32f1xx_it.c` 中 USART1_IRQHandler 是否正确调用 HAL_UART_IRQHandler
  - [x] 检查 `HAL_UART_MspInit` 中 USART1 NVIC 优先级和使能配置
  - [x] 在 `main.c` 中确保 `HAL_UART_Receive_IT` 在所有可能阻塞的操作之前调用

- [x] Task 4: 更新 SYSTEM_STATUS_GUIDE.md
  - [x] 补充上电自检 LED 序列说明（R→G→B→灭 各 200ms）
  - [x] 补充各状态完整时序描述（LED 闪烁频率、蜂鸣器响/停时间、LCD 刷新间隔）
  - [x] 更新烧录后判断流程，增加自检序列观察步骤
  - [x] 补充串口验证步骤：启动后应看到标识消息

# Task Dependencies
- Task 1 可独立执行
- Task 2 可独立执行
- Task 3 可独立执行
- Task 4 可独立执行
- 所有任务可并行执行