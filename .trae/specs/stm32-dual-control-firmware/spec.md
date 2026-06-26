# STM32 双控架构下位机固件 Spec

## Why
双控架构机器人需要 STM32 作为下位机负责实时姿态控制与电机驱动，树莓派作为上位机负责高级决策与视觉处理。本规范定义 STM32 固件的功能需求，确保下位机满足 1kHz 实时控制周期要求，并与树莓派稳定通信。

## What Changes
- 新增 STM32 固件项目，基于 STM32F103C8T6 / STM32F405RGT6
- 实现 MPU6050 姿态采集与串级 PID 自平衡控制
- 实现 TB6612 电机驱动与 N20 编码器反馈
- 实现 UART 通信协议与树莓派双向数据交换
- 实现电源管理、摔倒检测与断联保护安全逻辑
- 实现 RGB 指示灯/蜂鸣器状态指示与扩展接口预留

## Impact
- Affected specs: 下位机固件（STM32）
- Affected code: 新建 STM32 固件项目（STM32CubeMX + Keil MDK / STM32CubeIDE）

## ADDED Requirements

### Requirement: 姿态采集与自平衡控制
The system SHALL 通过 MPU6050 采集姿态数据并运行串级 PID 算法实现自平衡。

- **WHEN** 系统上电启动并完成初始化
- **THEN** STM32 以 1kHz 频率通过 I²C 读取 MPU6050 的加速度计和陀螺仪数据
- **AND** 使用互补滤波或卡尔曼滤波解算俯仰角（Pitch）和角速度
- **AND** 运行串级 PID 控制算法（直立环为主，速度环/转向环为辅）
- **AND** 输出 PWM 信号控制左右电机，维持车身平衡

#### Scenario: 1kHz 控制周期保证
- **WHEN** 系统正常运行
- **THEN** 姿态读取与 PID 计算总耗时 ≤ 1ms，控制周期稳定在 1kHz

### Requirement: 电机驱动与编码器反馈
The system SHALL 通过 TB6612 驱动 N20 微型直流电机，并读取编码器反馈。

- **WHEN** PID 控制器输出控制量
- **THEN** STM32 通过 PWM 和方向 IO 引脚控制 TB6612 驱动两个 N20 电机
- **AND** 读取电机编码器脉冲信号，换算为轮速和行驶距离
- **AND** 将轮速数据反馈给速度环 PID 控制器

### Requirement: 与树莓派通信（UART）
The system SHALL 通过 UART 与树莓派进行双向通信，波特率 115200 或更高。

- **WHEN** 树莓派通过串口下发指令
- **THEN** STM32 接收并解析以下指令：
  - 目标速度（前进/后退/旋转）
  - 目标表情/指示灯控制
  - 休眠/唤醒
- **WHEN** STM32 收到数据请求或周期性上报
- **THEN** STM32 向树莓派发送以下数据：
  - 当前倾角（Pitch）
  - 电池电压
  - 电机实时转速
  - 系统状态（平衡/摔倒/低电量）

### Requirement: 电源管理与安全逻辑
The system SHALL 实现锂电池电压监测、摔倒检测和断联保护。

- **WHEN** 电池电压低于设定阈值
- **THEN** 系统自动减速并向上位机上报低电量状态
- **WHEN** 检测到车身倾角超过安全阈值（摔倒）
- **THEN** 系统立即停止电机输出，进入保护模式
- **WHEN** 连续 1 秒未收到树莓派的心跳或指令
- **THEN** 系统自动减速至停止并保持直立姿态

### Requirement: 辅助功能与扩展接口
The system SHALL 提供状态指示和扩展接口。

- **WHEN** 系统状态发生变化（启动、平衡、报警、低电量）
- **THEN** RGB 指示灯/蜂鸣器输出对应的状态信号
- **AND** 预留 I²C 或 GPIO 接口供扩展模块使用（如舵机控制耳朵/尾巴）

## MODIFIED Requirements
无

## REMOVED Requirements
无