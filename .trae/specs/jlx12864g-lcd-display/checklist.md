# Checklist

- [x] LCD 底层驱动文件 lcd_jlx12864g.c 和 lcd_jlx12864g.h 存在且编译通过
- [x] 软件 SPI 时序正确：SCLK 上升沿采样，高位在前
- [x] LCD_Init 初始化序列正确（复位 → 对比度设置 → 显示方向 → 清屏）
- [x] 中文字库 JLX-GB2312 读取函数正确实现
- [x] LCD_ShowString 能正确区分 ASCII 字符和 GB2312 汉字
- [x] 显示模式封装文件 lcd_display.c 和 lcd_display.h 存在且编译通过
- [x] 正常模式显示：速度、电压、倾角、状态信息正确
- [x] 调参模式显示：PID 参数、传感器原始数据正确
- [x] 'M' 串口指令能正确切换显示模式
- [x] main.c 中 LCD 初始化和刷新逻辑正确集成
- [x] 引脚分配无冲突：8 个 LCD 引脚均为空闲引脚
- [x] WIRING_GUIDE.md 已更新 LCD 接线章节和引脚汇总表
- [x] 完整项目编译通过（0 Error, 32 Warning：均为文件末尾换行警告）