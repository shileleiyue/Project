# STM32CubeMX + Keil5 自平衡小车固件搭建 Spec

## Why
现有项目使用 STM32CubeIDE + Makefile（GCC）构建，但 STM32CubeMX + Keil5（ARMCC）是业内更广泛使用的开发流程，尤其适合初学者入门。需要从零开始使用 CubeMX 生成 Keil5 工程，并编写一本详尽的操作手册（"书"），覆盖每一步 CubeMX 操作、代码含义、注意事项，帮助零基础用户从硬件配置到代码编写完整掌握整个流程。

## What Changes
- **废弃**现有 Makefile/GCC 构建体系，改用 CubeMX 生成 Keil5 MDK-ARM 项目
- 使用 CubeMX 图形化配置所有外设（RCC、GPIO、TIM、I2C、UART、ADC、SysTick、NVIC）
- 在 Keil5 中编写/移植应用层代码（main.c、motor、encoder、mpu6050、pid、uart_protocol、power_manager、indicator）
- 编写一本"自平衡小车从零入门书"，以 CubeMX 操作为主线，逐文件解释每个设置的目的、生成的代码含义、注意事项

## Impact
- Affected specs: `stm32-firmware-rewrite`（将被替代，旧项目保留不变）
- Affected code: `firmware/` 目录下重建，新项目结构遵循 Keil5 MDK 规范
- Affected docs: 重写 BUILD_GUIDE.md 为"从零入门书"风格

## ADDED Requirements

### Requirement: CubeMX 项目配置与 Keil5 工程生成
The system SHALL 使用 STM32CubeMX 完成以下配置并生成 Keil5 MDK-ARM v5 工程：

#### Scenario: RCC 时钟配置
- **WHEN** 用户在 CubeMX 中打开 RCC 选项卡
- **THEN** 配置 HSE 为 Crystal/Ceramic Resonator，LSE 禁用
- **THEN** 时钟树配置：HSE 8MHz → PLL(x9) → SYSCLK 72MHz，APB1=36MHz，APB2=72MHz
- **WHEN** 用户生成代码
- **THEN** Keil5 项目自动包含正确的 system_stm32f1xx.c 和时钟初始化代码

#### Scenario: GPIO 引脚配置
- **WHEN** 用户在 CubeMX 的 Pinout 视图中配置引脚
- **THEN** 应配置以下引脚功能：
  - PA0( TIM2_CH1)、PA1( TIM2_CH2) — 左编码器
  - PB4( TIM3_CH1)、PB5( TIM3_CH2) — 右编码器
  - PA2( TIM2_CH3)、PA3( TIM2_CH4) — 电机 PWM（TIM2 混合模式，CH1/CH2 编码器，CH3/CH4 PWM）
  - PB0、PB1 — 左电机方向
  - PB12、PB13 — 右电机方向
  - PB6( I2C1_SCL)、PB7( I2C1_SDA) — MPU6050
  - PA9( USART1_TX)、PA10( USART1_RX) — 蓝牙/调试串口
  - PB14、PB15、PB8 — RGB LED
  - PB3 — 蜂鸣器
  - PA4(ADC1_IN4) — 电池电压检测（注意：早期文档错误使用了 PA2，实际 PA2 已被 TIM2_CH3/PWM 占用，需改为 PA4(ADC1_IN4)）
- **THEN** 未使用的引脚应设置为 Analog 模式以降低功耗

#### Scenario: TIM 定时器配置
- **WHEN** 用户在 CubeMX 中配置 TIM
- **THEN** TIM2 配置为混合模式：编码器模式（CH1/CH2）+ PWM Generation CH3 & CH4（电机 PWM）
- **THEN** TIM3 配置为 Encoder Mode（编码器模式）
- **THEN** TIM1 配置为 1ms 中断（用于 PID 控制循环）
- **WHEN** 生成代码
- **THEN** Keil5 项目中自动包含 tim.c 和对应 HAL 初始化代码

#### Scenario: I2C 配置
- **WHEN** 用户在 CubeMX 中配置 I2C1
- **THEN** 设置为 Standard Mode（100kHz）或 Fast Mode（400kHz）
- **THEN** 地址长度为 7-bit
- **WHEN** 生成代码
- **THEN** Keil5 项目中自动包含 i2c.c 和对应 HAL 初始化代码

#### Scenario: USART 配置
- **WHEN** 用户在 CubeMX 中配置 USART1
- **THEN** 设置为 Asynchronous 模式，波特率 115200，8N1
- **THEN** 使能 USART1 全局中断（NVIC）
- **WHEN** 生成代码
- **THEN** Keil5 项目中自动包含 usart.c 和 HAL_UART_IRQHandler 回调

#### Scenario: ADC 配置
- **WHEN** 用户在 CubeMX 中配置 ADC1
- **THEN** 添加通道（如 PA4/ADC1_IN4），采样时间配置为 55.5 Cycles
- **THEN** 分辨率 12-bit，连续转换模式
- **WHEN** 生成代码
- **THEN** Keil5 项目中自动包含 adc.c 和对应初始化代码

#### Scenario: NVIC 中断优先级配置
- **WHEN** 用户在 CubeMX 中配置 NVIC
- **THEN** 设置中断优先级分组为 4 bits（16级抢占优先级）
- **THEN** 使能 TIM1_UP、USART1、USART2 中断
- **THEN** SysTick 优先级设为最低（15）

### Requirement: 应用层代码编写/移植
The system SHALL 在 Keil5 中编写完整的应用层代码，包含以下模块：

#### Scenario: 主程序
- **WHEN** 用户打开 main.c
- **THEN** 应看到 CubeMX 生成的初始化代码（MX_*_Init）和用户自定义的初始化与主循环
- **THEN** 主循环包含状态机（INIT → STARTUP → BALANCING → FALLEN/LOW_BAT/SLEEP）

#### Scenario: 模块化驱动
- **WHEN** 用户查看 Core 目录
- **THEN** 应看到 motor.c/h、encoder.c/h、mpu6050.c/h、pid.c/h、uart_protocol.c/h、power_manager.c/h、indicator.c/h
- **THEN** 每个模块应有清晰的函数接口和注释

#### Scenario: 编译通过
- **WHEN** 用户在 Keil5 中点击 Build（或按 F7）
- **THEN** 编译应零错误零警告完成，生成 .hex 和 .axf 文件

### Requirement: "从零入门书"操作手册
The system SHALL 提供一本完整的操作手册（BUILD_GUIDE.md），以"书"的形式逐章讲解：

#### Scenario: 第一章 — 准备工作
- **WHEN** 读者阅读第一章
- **THEN** 应了解所需材料清单、软件安装（CubeMX、Keil5、ST-Link 驱动）
- **THEN** 应有 CubeMX 和 Keil5 的安装截图和激活说明

#### Scenario: 第二章 — CubeMX 新建工程
- **WHEN** 读者按照第二章操作
- **THEN** 应学会在 CubeMX 中选择 STM32F103C8T6
- **THEN** 应学会配置 SYS（Debug Serial Wire）、RCC（HSE）
- **THEN** 每一步骤解释"为什么这样配置"和"其他选项的后果"

#### Scenario: 第三~六章 — 外设配置详解
- **WHEN** 读者按照章节顺序操作
- **THEN** 每章针对一个外设（GPIO、TIM、I2C、UART、ADC），包含：
  - CubeMX 操作步骤（截图或表格）
  - 每个参数的含义和推荐值
  - 生成代码后，解释 CubeMX 生成的代码在做什么
  - 用户需要添加/修改的代码位置
  - 常见错误和注意事项

#### Scenario: 第七章 — 应用层代码编写
- **WHEN** 读者阅读第七章
- **THEN** 应逐个文件讲解每个模块的代码逻辑
- **THEN** 每个函数说明其作用、输入输出、调用关系
- **THEN** 提供完整的代码清单

#### Scenario: 第八章 — 编译烧录与调试
- **WHEN** 读者阅读第八章
- **THEN** 应学会在 Keil5 中编译、设置 Debug 选项、连接 ST-Link 烧录
- **THEN** 应学会使用串口调试助手查看数据
- **THEN** 应学会 PID 参数调试方法

#### Scenario: 第九~十章 — 扩展功能
- **WHEN** 读者阅读第九~十章
- **THEN** 应了解蓝牙远程控制和语音识别扩展的实现方法
- **THEN** 应了解后续升级路径

## MODIFIED Requirements
无 — 此为全新项目方案。

## REMOVED Requirements
无 — 旧项目（firmware/ 使用 STM32CubeIDE + Makefile）保留不变作为参考。