# Tasks

- [x] Task 1: 创建 LCD 底层驱动 (lcd_jlx12864g.c/h)
  - [x] 定义 LCD 引脚宏（PA5/PA6/PA7/PA8/PA11 用于 LCD SPI，PA12/PA15/PB9 用于字库 SPI）
  - [x] 实现软件 SPI 底层函数（SCLK/SDA 时序控制）
  - [x] 实现 LCD_WriteCmd 和 LCD_WriteData 函数
  - [x] 实现 LCD_Init 初始化函数（复位、对比度、显示方向、清屏）
  - [x] 实现 LCD_SetCursor 设置显示位置
  - [x] 实现 LCD_Clear 清屏函数
  - [x] 实现中文字库读取函数 LCD_ReadFont（从 JLX-GB2312 字库读取字模）
  - [x] 实现 LCD_ShowString 中英文字符串显示（自动区分 ASCII 和 GB2312 汉字）
  - [x] 实现 LCD_ShowNum 数字显示函数

- [x] Task 2: 创建显示模式封装 (lcd_display.c/h)
  - [x] 定义显示模式枚举（DISPLAY_MODE_NORMAL, DISPLAY_MODE_TUNING）
  - [x] 实现 LCD_DisplayNormalMode：显示速度、电池电压、倾角、系统状态
  - [x] 实现 LCD_DisplayTuningMode：显示 PID 参数、传感器原始数据
  - [x] 实现模式切换函数 LCD_Display_SetMode
  - [x] 实现不同系统状态下的显示适配（ERROR 状态显示错误信息，LOW_BAT 显示电量警告）

- [x] Task 3: 集成到主程序
  - [x] 修改 main.h：添加 LCD 引脚宏定义，声明 LCD 相关 extern 变量
  - [x] 修改 main.c：在 main() 中调用 LCD_Init() 和 LCD_Display_Init()
  - [x] 修改 main.c：在主循环 while(1) 中添加 200ms LCD 刷新逻辑
  - [x] 新增 'M' 串口指令：在 uart_protocol.h 中定义 CMD_MODE，在 uart_protocol.c 中实现模式切换

- [x] Task 4: 更新接线文档
  - [x] 在 WIRING_GUIDE.md 中新增 LCD 接线章节（引脚对照、电压要求、SPI 接线注意事项）
  - [x] 更新完整引脚汇总表，添加 LCD 占用的 8 个引脚
  - [x] 更新上电检查清单，添加 LCD 相关检查项

# Task Dependencies
- Task 2 依赖 Task 1
- Task 3 依赖 Task 1 和 Task 2
- Task 4 可并行执行