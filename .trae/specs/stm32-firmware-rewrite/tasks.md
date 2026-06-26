# Tasks

- [x] Task 1: 创建 STM32CubeIDE 项目文件
  - 创建 `.project` — Eclipse 项目描述文件（含 C 语言 Nature 和 STM32CubeIDE 构建器）
  - 创建 `.cproject` — 完整构建配置（MCU=STM32F103C8Tx, 编译选项, 包含路径, 源文件映射）
  - 创建 `.settings/org.eclipse.core.resources.prefs` — IDE 编码设置 UTF-8
  - 确保 `Core/` 目录下的源文件在 `.cproject` 的 sourceEntries 中正确映射

- [x] Task 2: 复制 HAL 驱动头文件与 CMSIS 核心库
  - 从 `D:\IST\STM32\STM32CubeF1\` 或 `D:\IST\STM32\STM32_Projects\STM32-project\` 复制：
    - `Drivers/STM32F1xx_HAL_Driver/Inc/` — 所有 HAL 头文件
    - `Drivers/CMSIS/Core/Include/` — CMSIS 核心头文件
    - `Drivers/CMSIS/Device/ST/STM32F1xx/Include/` — 设备头文件
  - 注意：只复制头文件，不复制源文件（使用命令行编译时再单独处理）

- [x] Task 3: 创建 HAL 配置文件
  - 创建 `Inc/stm32f1xx_hal_conf.h`
  - 仅启用需要的模块：HAL_MODULE, HAL_ADC, HAL_CORTEX, HAL_DMA, HAL_FLASH, HAL_GPIO, HAL_I2C, HAL_PWR, HAL_RCC, HAL_TIM, HAL_UART
  - 配置 HSE_VALUE=8000000, 时钟树参数, 断言设置

- [x] Task 4: 创建 Startup 启动文件和链接脚本
  - 创建 `Startup/startup_stm32f103c8tx.s` — 中断向量表 + Reset_Handler
  - 创建 `STM32F103C8TX_FLASH.ld` — 链接脚本（Flash 64KB 起始 0x08000000, RAM 20KB 起始 0x20000000）

- [x] Task 5: 创建系统文件和中断处理
  - 创建 `Src/system_stm32f1xx.c` — 系统时钟配置（72MHz HSE+PLL），含 SystemCoreClock 和 SystemInit
  - 创建 `Src/stm32f1xx_it.c` + `Inc/stm32f1xx_it.h` — 中断服务函数（TIM1_UP, USART1, USART2, SysTick）
  - 创建 `Src/stm32f1xx_hal_msp.c` — HAL MSP 初始化回调（GPIO、NVIC、DMA 配置）

- [x] Task 6: 优化应用层代码适配新框架
  - 检查并调整 `Core/` 下所有文件的 `#include` 路径适配新框架
  - 确保 `main.h` 的引脚定义、外设句柄、全局变量声明与新框架一致
  - 确保 `main.c` 中的 `SystemClock_Config`、`MX_*_Init` 函数与新框架一致
  - 验证所有模块间接口兼容性

- [x] Task 7: 创建命令行构建系统
  - 创建 `Makefile` — 支持 `make all` 和 `make clean`
  - 仅编译必要的 HAL 源文件（15 个模块，不含模板和 LL 驱动）
  - 编译 Core/ 应用层源码
  - 编译 Startup 启动代码
  - 链接生成 .elf 文件
  - 创建 `build.bat` — Windows 一键构建脚本

- [x] Task 8: 重写 BUILD_GUIDE.md 操作指南
  - 更新项目结构说明（文件树 + 功能说明表）
  - 更新编译说明（STM32CubeIDE 导入 + 命令行 make 两种方式）
  - 更新烧录说明（ST-Link 接线 + IDE 烧录 + 命令行烧录）
  - 保留原有材料清单、硬件接线、PID 调试、常见问题等章节
  - 增加新框架特有说明（如 HAL 模块配置、链接脚本说明）

- [x] Task 9: 编译验证
  - 清理旧构建产物
  - 运行 `make clean` + `make -j4 all` 验证零错误零警告
  - 验证生成 .elf 文件大小正常（text 约 30KB+）
  - 验证 `.map` 文件确认内存布局正确

# Task Dependencies
- [Task 2] 依赖于 [Task 1]（项目结构先就绪）
- [Task 3] 依赖于 [Task 2]（HAL 头文件就绪后才可配置）
- [Task 4] 独立于 Task 2/3
- [Task 5] 依赖于 [Task 2] [Task 3] [Task 4]
- [Task 6] 依赖于 [Task 5]（系统框架就绪后适配）
- [Task 7] 依赖于 [Task 6]（源码就绪后才可创建 Makefile）
- [Task 8] 可与其他任务并行
- [Task 9] 依赖于所有前置任务完成