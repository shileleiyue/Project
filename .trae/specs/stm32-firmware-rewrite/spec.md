# STM32F103C8T6 固件框架重构 Spec

## Why
现有 `firmware/` 目录仅有应用层源码（Core/Inc, Core/Src），缺少完整的 STM32CubeIDE 项目结构（无 .cproject、无 Drivers、无 Startup、无链接脚本、无 HAL 配置），导致无法直接编译运行。需要从零搭建完整的、可编译可烧录的固件工程，并配套详细的操作指南。

## What Changes
- 在 `firmware/` 下创建完整的 STM32CubeIDE 项目结构（.cproject, .project）
- 添加 STM32F1xx HAL 驱动库（仅编译必需的模块，不含模板/LL 文件）
- 添加 CMSIS Core 和 Device 文件
- 添加 Startup 启动代码（startup_stm32f103c8tx.s）
- 添加链接脚本（STM32F103C8TX_FLASH.ld）
- 添加 HAL 配置文件（stm32f1xx_hal_conf.h）
- 添加系统时钟配置文件（system_stm32f1xx.c）
- 保留并优化现有 Core/ 应用层代码（main.c, motor, encoder, mpu6050, pid, uart_protocol, power_manager, indicator）
- 新增必要的系统文件（stm32f1xx_it.c, stm32f1xx_it.h, stm32f1xx_hal_msp.c）
- 重写 BUILD_GUIDE.md 为完整的项目构建与操作指南
- 确保工程在 STM32CubeIDE 和命令行 make 两种方式下均可编译通过

## Impact
- Affected specs: 无现有 spec 冲突
- Affected code: `firmware/` 下新增项目框架文件，Core/ 应用层代码优化调整

## ADDED Requirements

### Requirement: 完整的 STM32CubeIDE 项目结构
The system SHALL 包含以下项目文件：
- `.project` — Eclipse 项目描述文件，含 C 语言 Nature
- `.cproject` — STM32CubeIDE 构建配置，含 MCU 型号、编译选项、包含路径、源文件列表
- `.settings/` — IDE 设置目录

### Requirement: HAL 驱动与 CMSIS 核心库
The system SHALL 包含：
- `Drivers/STM32F1xx_HAL_Driver/Inc/` — HAL 驱动头文件
- `Drivers/CMSIS/Core/Include/` — CMSIS 核心头文件
- `Drivers/CMSIS/Device/ST/STM32F1xx/Include/` — STM32F1xx 设备头文件
- `Inc/stm32f1xx_hal_conf.h` — HAL 配置（仅启用 ADC, CORTEX, DMA, FLASH, GPIO, I2C, PWR, RCC, TIM, UART 模块）

### Requirement: 启动与链接文件
The system SHALL 包含：
- `Startup/startup_stm32f103c8tx.s` — 启动代码（中断向量表、Reset_Handler、SystemInit 调用）
- `STM32F103C8TX_FLASH.ld` — 链接脚本（Flash 64KB, RAM 20KB）
- `Src/system_stm32f1xx.c` — 系统时钟配置（72MHz HSE PLL）
- `Src/stm32f1xx_it.c` + `Src/stm32f1xx_it.h` — 中断服务函数
- `Src/stm32f1xx_hal_msp.c` — HAL MSP 初始化回调

### Requirement: 应用层代码优化
The system SHALL 保留并优化 Core/ 目录下的应用层代码：

#### Scenario: 代码结构保持
- **WHEN** 用户打开项目
- **THEN** 应看到 `Core/Inc/` 和 `Core/Src/` 中的模块化代码，包含：
  - `main.c/h` — 主程序、系统状态机、外设初始化
  - `motor.c/h` — TB6612 电机驱动（PWM + 方向控制）
  - `encoder.c/h` — 编码器速度测量
  - `mpu6050.c/h` — MPU6050 姿态传感器驱动
  - `pid.c/h` — 串级 PID 控制器（直立环、速度环、转向环）
  - `uart_protocol.c/h` — 串口通信协议
  - `power_manager.c/h` — 电源管理（电池检测、低电量保护）
  - `indicator.c/h` — RGB LED 指示灯控制

#### Scenario: 编译通过
- **WHEN** 用户在 STM32CubeIDE 中点击 Build
- **THEN** 编译应零错误零警告完成，生成 .elf 文件
- **WHEN** 用户在命令行运行 `make -j4 all`
- **THEN** 编译应零错误零警告完成

### Requirement: 操作指南文档
The system SHALL 提供 `BUILD_GUIDE.md` 操作指南，包含：
- 硬件材料清单与选型对比
- 逐引脚接线图与对应表
- 软件环境搭建（STM32CubeIDE 安装、项目导入、编译烧录）
- 代码文件功能说明与参数调优位置
- 动平衡 PID 调试步骤
- 常见问题排查表
- 远程控制与语音识别扩展指南
- 后续升级路径

## MODIFIED Requirements
无 — 此为全新项目搭建。

## REMOVED Requirements
无 — 保留所有现有应用层代码。