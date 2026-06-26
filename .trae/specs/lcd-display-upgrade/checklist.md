# Checklist

- [x] LCD 8×16 ASCII 字库包含 95 个字符（0x20-0x7E），每字符 16 字节
- [x] 字库为列优先格式（column-major），匹配 UC1701X 页显存布局
- [x] LCD_ShowChar 上半页写入 page_upper(y+1)，下半页写入 page_lower(y)
- [x] LCD_ShowString 每行显示 16 个字符，占满 128 像素宽度
- [x] LCD_DisplayTest 硬件自检函数：全屏点亮→横线→棋盘格→"OK"
- [x] main.c 中 LCD_Display_Init 后调用 LCD_DisplayTest()
- [x] 上电后 LED 自检序列执行：红 200ms → 绿 200ms → 蓝 200ms → 灭 200ms
- [x] 自检序列末尾蜂鸣器短响 1 声（100ms）
- [x] 上电后串口发送 "=== STM32 Balance Car ===" 标识消息
- [x] 串口发送 "System init OK!" 或 "MPU6050 init failed!" 状态消息
- [x] USART1_IRQHandler 正确调用 HAL_UART_IRQHandler(&huart1)
- [x] HAL_UART_Receive_IT 在 LCD_Init 之前调用
- [x] SYSTEM_STATUS_GUIDE.md 包含上电自检 LED 序列说明
- [x] SYSTEM_STATUS_GUIDE.md 包含各状态完整时序描述
- [x] SYSTEM_STATUS_GUIDE.md 包含 LCD 引脚接线表（9 引脚 + 电压/测试方法）
- [x] SYSTEM_STATUS_GUIDE.md 包含 8 种显示故障诊断表
- [x] SYSTEM_STATUS_GUIDE.md 包含无万用表时的 LED 辅助引脚测试方法
- [x] 完整项目编译通过（0 Error, 32 Warning）