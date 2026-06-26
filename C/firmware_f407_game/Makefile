# =============================================================================
#   STM32F407ZGT6 打地鼠游戏 - Makefile
#   适用于正点原子探索者开发板 + 4.3寸触摸屏
# =============================================================================

# 工具链配置
TOOLCHAIN := arm-none-eabi-
CC := $(TOOLCHAIN)gcc
AS := $(TOOLCHAIN)gcc -x assembler-with-cpp
LD := $(TOOLCHAIN)gcc
OBJCOPY := $(TOOLCHAIN)objcopy
SIZE := $(TOOLCHAIN)size

# 目标名称
TARGET := whack_mole

# 构建目录
BUILD_DIR := build

# =============================================================================
# MCU 配置
# =============================================================================
MCU_FLAGS := -mcpu=cortex-m4 -mthumb -mfloat-abi=soft
FPU_FLAGS :=

# =============================================================================
# 包含路径
# =============================================================================
INCLUDE_DIRS := \
  Inc \
  Core/Inc \
  Drivers/STM32F4xx_HAL_Driver/Inc \
  Drivers/CMSIS/Device/ST/STM32F4xx/Include \
  Drivers/CMSIS/Core/Include

INCLUDE_FLAGS := $(addprefix -I,$(INCLUDE_DIRS))

# =============================================================================
# 预定义符号
# =============================================================================
DEFINES := \
  -DSTM32 \
  -DSTM32F4 \
  -DSTM32F407xx \
  -DSTM32F407ZGTx \
  -DUSE_HAL_DRIVER

# =============================================================================
# 链接脚本
# =============================================================================
LINKER_SCRIPT := STM32F407ZGTX_FLASH.ld

# =============================================================================
# 源文件列表
# =============================================================================

# 应用层源文件
CORE_SRC := \
  Core/Src/main.c \
  Core/Src/lcd.c \
  Core/Src/touch.c \
  Core/Src/game.c

# 系统源文件
SYS_SRC := \
  Src/system_stm32f4xx.c \
  Src/syscalls.c \
  Src/sysmem.c \
  Src/stm32f4xx_it.c

# HAL 源文件 (仅必需的模块)
HAL_SRC := \
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal.c \
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_cortex.c \
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_dma.c \
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_gpio.c \
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_i2c.c \
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_pwr.c \
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_rcc.c \
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_sram.c \
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_tim.c \
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_tim_ex.c

# 启动文件
STARTUP_SRC := Startup/startup_stm32f407zgtx.s

# =============================================================================
# 对象文件
# =============================================================================
ALL_C_SRC := $(CORE_SRC) $(SYS_SRC) $(HAL_SRC)
ALL_S_SRC := $(STARTUP_SRC)

C_OBJS := $(addprefix $(BUILD_DIR)/obj/, $(ALL_C_SRC:.c=.o))
S_OBJS := $(addprefix $(BUILD_DIR)/obj/, $(ALL_S_SRC:.s=.o))
OBJECTS := $(C_OBJS) $(S_OBJS)

# =============================================================================
# 编译选项
# =============================================================================
CFLAGS := $(MCU_FLAGS) $(FPU_FLAGS) -Wall -Wextra -Werror -g3 -O1
CFLAGS += $(INCLUDE_FLAGS) $(DEFINES)
CFLAGS += -ffunction-sections -fdata-sections
CFLAGS += -std=c99

ASFLAGS := $(MCU_FLAGS) $(FPU_FLAGS) -g3

LDFLAGS := $(MCU_FLAGS) $(FPU_FLAGS) -specs=nano.specs -specs=nosys.specs
LDFLAGS += -Wl,-Map=$(BUILD_DIR)/$(TARGET).map,--cref
LDFLAGS += -Wl,--gc-sections
LDFLAGS += -T$(LINKER_SCRIPT)

# =============================================================================
# 目标规则
# =============================================================================

.PHONY: all clean size

all: $(BUILD_DIR)/$(TARGET).elf $(BUILD_DIR)/$(TARGET).hex $(BUILD_DIR)/$(TARGET).bin

# 链接
$(BUILD_DIR)/$(TARGET).elf: $(OBJECTS) $(LINKER_SCRIPT)
	@mkdir -p $(dir $@)
	$(LD) $(LDFLAGS) -o $@ $(OBJECTS) $(LIBS)
	$(SIZE) $@

# 生成 hex 文件
$(BUILD_DIR)/$(TARGET).hex: $(BUILD_DIR)/$(TARGET).elf
	$(OBJCOPY) -O ihex $< $@

# 生成 bin 文件
$(BUILD_DIR)/$(TARGET).bin: $(BUILD_DIR)/$(TARGET).elf
	$(OBJCOPY) -O binary $< $@

# 编译 C 文件
$(BUILD_DIR)/obj/%.o: %.c
	@mkdir -p $(dir $@)
	$(CC) -c $(CFLAGS) -o $@ $<

# 编译汇编文件
$(BUILD_DIR)/obj/%.o: %.s
	@mkdir -p $(dir $@)
	$(AS) -c $(ASFLAGS) -o $@ $<

# 清理
clean:
	rm -rf $(BUILD_DIR)

# 显示固件大小
size: $(BUILD_DIR)/$(TARGET).elf
	$(SIZE) $<