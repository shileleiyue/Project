# 验证清单

- [x] .project 文件包含正确的 C 语言 Nature 和 STM32CubeIDE 构建器
- [x] .cproject 文件包含 MCU 型号、编译选项、包含路径、源文件映射
- [x] HAL 驱动头文件目录结构完整（Drivers/STM32F1xx_HAL_Driver/Inc/）
- [x] CMSIS 核心头文件目录结构完整（Drivers/CMSIS/）
- [x] stm32f1xx_hal_conf.h 仅启用必需的硬件模块
- [x] startup_stm32f103c8tx.s 中断向量表完整
- [x] STM32F103C8TX_FLASH.ld 内存布局正确（Flash 64KB, RAM 20KB）
- [x] system_stm32f1xx.c 时钟配置正确（72MHz HSE PLL）
- [x] stm32f1xx_it.c 包含所有必需的中断服务函数
- [x] stm32f1xx_hal_msp.c — MSP 回调函数集成在 main.c 中，无需单独文件
- [x] Core/ 应用层代码与新框架兼容（无编译错误）
- [x] Makefile 可成功编译所有源文件并链接
- [x] make clean + make -j4 all 零错误零警告
- [x] 生成的 .elf 文件大小正常（text=43892, data=472, bss=2992）
- [x] BUILD_GUIDE.md 包含完整的项目结构和操作说明