# Tasks

- [ ] Task 1: 创建新项目目录结构
  - 在 `firmware_keil/` 下创建 Keil5 项目骨架
  - 创建 `MDK-ARM/`、`Core/Inc/`、`Core/Src/` 子目录
  - 创建 `Drivers/` 子目录（CubeMX 生成后会自动填充）

- [ ] Task 2: 编写 CubeMX 操作指南（第1~2章）
  - 第1章：材料清单、软件安装（CubeMX、Keil5、ST-Link 驱动、CH340 驱动）
  - 第2章：CubeMX 新建工程、选择芯片、SYS/RCC 基础配置
  - 每步解释"为什么"和"注意事项"

- [ ] Task 3: 编写外设配置指南（第3~6章）
  - 第3章：GPIO 引脚配置（电机方向、LED、蜂鸣器、未使用引脚处理）
  - 第4章：TIM 定时器配置（TIM2 编码器+PWM 混合模式、TIM3 编码器模式、TIM1 中断）
  - 第5章：I2C（MPU6050）和 USART（蓝牙/调试串口）配置
  - 第6章：ADC（电池检测）和 NVIC 中断优先级配置
  - 每章包含：CubeMX 操作步骤、参数含义、生成代码解读、用户自定义代码位置、注意事项

- [ ] Task 4: 在 Keil5 中编写应用层代码
  - 移植/编写 main.c/h — 主程序、状态机、外设初始化
  - 移植/编写 motor.c/h — TB6612 电机驱动
  - 移植/编写 encoder.c/h — 编码器速度测量
  - 移植/编写 mpu6050.c/h — MPU6050 姿态传感器
  - 移植/编写 pid.c/h — 串级 PID 控制
  - 移植/编写 uart_protocol.c/h — 串口通信协议
  - 移植/编写 power_manager.c/h — 电源管理
  - 移植/编写 indicator.c/h — RGB LED 指示灯

- [ ] Task 5: 编写应用层代码讲解（第7章）
  - 逐个文件讲解每个模块的代码逻辑
  - 每个函数说明作用、输入输出、调用关系
  - 提供完整的代码清单

- [ ] Task 6: 编写编译烧录与调试指南（第8章）
  - Keil5 编译设置（Output、Listing、C/C++ 选项）
  - Debug 配置（ST-Link 连接、烧录算法设置）
  - 串口调试助手使用方法
  - PID 参数调试方法

- [ ] Task 7: 编写扩展功能指南（第9~10章）
  - 第9章：蓝牙远程控制（HC-05 接线、手机 APP 控制）
  - 第10章：后续升级路径（传感器升级、算法优化、WiFi 控制）

- [ ] Task 8: 编译验证
  - 在 Keil5 中编译验证零错误零警告
  - 验证生成 .hex 文件
  - 验证代码逻辑完整性

# Task Dependencies
- [Task 2] 依赖于 [Task 1]（目录结构就绪后才可编写指南）
- [Task 3] 依赖于 [Task 1]
- [Task 4] 依赖于 [Task 3]（CubeMX 生成的 HAL 框架就绪后才可移植代码）
- [Task 5] 依赖于 [Task 4]（代码编写完成后才可讲解）
- [Task 6] 可独立于其他任务并行编写
- [Task 7] 可独立于其他任务并行编写
- [Task 8] 依赖于 [Task 4]（代码就绪后才可编译验证）