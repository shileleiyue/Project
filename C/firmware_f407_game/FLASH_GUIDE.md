# 打地鼠游戏 - 烧录流程说明

## 适用硬件
- 正点原子探索者 STM32F407ZGT6 开发板
- 4.3寸 TFT LCD 电容触摸屏 (ILI9341 + FT5206)
- ST-Link/V2 下载器 (或板载 ST-Link)

---

## 一、准备工作

### 1.1 安装 ARM GCC 工具链

下载并安装 `arm-none-eabi-gcc`：

```
https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain
```

选择 Windows 版本，下载后安装到默认路径，安装时勾选 **"Add to PATH"**。

验证安装：
```powershell
arm-none-eabi-gcc --version
```

### 1.2 安装烧录工具 (任选其一)

**方案 A: STM32CubeProgrammer (推荐)**
```
https://www.st.com/en/development-tools/stm32cubeprog.html
```
下载安装后，默认路径: `C:\Program Files\STMicroelectronics\STM32Cube\STM32CubeProgrammer\`

**方案 B: ST-LINK Utility (轻量)**
```
https://www.st.com/en/development-tools/stsw-link004.html
```

**方案 C: OpenOCD (开源)**
```
https://openocd.org/
```

### 1.3 准备 HAL 驱动库

本项目需要 STM32F4xx HAL 驱动库。从 STM32CubeF4 固件包中复制以下文件到项目的 `Drivers/` 目录：

```
Drivers/
├── CMSIS/
│   ├── Core/Include/          (CMSIS 核心头文件)
│   └── Device/ST/STM32F4xx/Include/  (STM32F4 设备头文件)
└── STM32F4xx_HAL_Driver/
    ├── Inc/                    (HAL 头文件)
    └── Src/                    (HAL 源文件，Makefile 中列出的文件)
```

**获取方式：**

1. 下载 STM32CubeF4 固件包：
   - https://github.com/STMicroelectronics/STM32CubeF4
   - 或使用 STM32CubeMX 下载

2. 复制驱动文件到项目目录：
   ```powershell
   # 假设 STM32CubeF4 解压到 C:\STM32Cube_FW_F4_V1.27.0
   # 在项目根目录执行:
   mkdir Drivers

   # 复制 CMSIS
   xcopy /E C:\STM32Cube_FW_F4_V1.27.0\Drivers\CMSIS Drivers\CMSIS\

   # 复制 HAL 驱动
   xcopy /E C:\STM32Cube_FW_F4_V1.27.0\Drivers\STM32F4xx_HAL_Driver Drivers\STM32F4xx_HAL_Driver\
   ```

3. **重要**: 在 `Drivers/STM32F4xx_HAL_Driver/Src/` 目录中，只保留 Makefile 中列出的 10 个 HAL 源文件，删除其余文件以避免编译错误。

---

## 二、硬件连接

### 2.1 ST-Link 连接 (SWD 方式)

| ST-Link 引脚 | 开发板引脚 | 说明 |
|-------------|-----------|------|
| SWDIO | PA13 (JTMS/SWDIO) | 数据线 |
| SWCLK | PA14 (JTCK/SWCLK) | 时钟线 |
| GND | GND | 地线 |
| 3.3V | 3.3V | 供电 (可选，可用 USB 供电) |

### 2.2 LCD 屏幕连接

将 4.3寸 LCD 屏幕直接插入开发板的 LCD 排座接口 (34P FPC 座)，注意方向，金属触点朝下。

### 2.3 供电

- 使用 USB 供电：将 USB 线插入开发板的 **USB_232** 接口 (USB 转串口口)
- 或使用 DC 电源：6-24V 直流电源插入 DC 接口
- 开发板电源指示灯 (蓝色) 亮起表示供电正常

---

## 三、编译固件

### 3.1 命令行编译

打开 PowerShell 或 CMD，进入项目目录：

```powershell
cd D:\IST\Project\C\firmware_f407_game
```

运行构建脚本：
```powershell
.\build.bat
```

或直接使用 Make：
```powershell
make clean
make -j4 all
```

### 3.2 编译输出

编译成功后在 `build\` 目录下生成三个文件：
- `whack_mole.elf` - ELF 调试文件
- `whack_mole.hex` - Intel HEX 格式 (常用烧录格式)
- `whack_mole.bin` - 二进制格式

---

## 四、烧录固件

### 方法 A: STM32CubeProgrammer (推荐)

**GUI 方式：**

1. 打开 STM32CubeProgrammer
2. 连接 ST-Link 到电脑和开发板
3. 在界面右侧选择 **ST-LINK** 连接方式
4. 点击 **Connect** 按钮
5. 点击 **Open file** 按钮，选择 `build\whack_mole.hex`
6. 点击 **Download** 按钮开始烧录
7. 烧录完成后点击 **Disconnect**

**CLI 方式：**

```powershell
# 进入 STM32CubeProgrammer 安装目录
cd "C:\Program Files\STMicroelectronics\STM32Cube\STM32CubeProgrammer\bin"

# 烧录 (根据实际 COM 口或 ST-Link 序列号调整)
.\STM32_Programmer_CLI.exe -c port=SWD -w "D:\IST\Project\C\firmware_f407_game\build\whack_mole.hex" -v -s
```

### 方法 B: ST-LINK Utility

1. 打开 STM32 ST-LINK Utility
2. 菜单: **Target -> Connect**
3. 菜单: **File -> Open file...** 选择 `build\whack_mole.hex`
4. 菜单: **Target -> Program & Verify...**
5. 点击 **Start** 开始烧录

### 方法 C: OpenOCD + st-flash

```powershell
# 使用 st-flash (ST-Link 开源工具)
st-flash --format ihex write build\whack_mole.hex

# 或使用 OpenOCD
openocd -f interface/stlink.cfg -f target/stm32f4x.cfg -c "program build\whack_mole.hex verify reset exit"
```

---

## 五、运行游戏

### 5.1 启动

烧录完成后，按开发板上的 **RESET** 按钮 (或重新上电)，游戏开始运行。

### 5.2 游戏画面

- **启动界面**: 显示 "WHACK-A-MOLE" 标题和绿色 "START GAME" 按钮
- **游戏界面**: 4x3 网格布局，12 个洞口，顶部显示分数、时间和连击
- **结束界面**: 显示最终分数、最高连击和评级

### 5.3 操作方式

| 操作 | 方式 |
|------|------|
| 开始游戏 | 点击屏幕上的 "START GAME" 按钮，或按 KEY0 按键 |
| 打地鼠 | 点击屏幕上的地鼠 (棕色圆形) |
| 重新开始 | 游戏结束后点击 "PLAY AGAIN" 按钮，或按 KEY0 |

### 5.4 游戏规则

- 游戏时长 30 秒
- 地鼠随机从洞中出现，持续约 1.5 秒后消失
- 点击地鼠得分：基础 10 分，连击加分 (连击数 x 5)
- 漏掉地鼠会重置连击
- 最终根据得分评级：S >= 200, A >= 120, B >= 60, C < 60

---

## 六、故障排查

### 6.1 编译失败

| 错误 | 解决方案 |
|------|---------|
| `arm-none-eabi-gcc: command not found` | 安装 ARM GCC 工具链并添加到 PATH |
| `fatal error: stm32f4xx_hal.h: No such file` | 检查 Drivers 目录是否完整，INCLUDE_DIRS 路径是否正确 |
| 链接错误: undefined reference | 检查 HAL 源文件是否缺失，Makefile 中 HAL_SRC 列表是否完整 |

### 6.2 烧录失败

| 错误 | 解决方案 |
|------|---------|
| ST-Link 未识别 | 检查 SWD 接线 (3.3V, GND, SWDIO, SWCLK)，检查驱动是否安装 |
| 芯片被写保护 | 在 STM32CubeProgrammer 中执行 "Option Bytes" 解除写保护 |
| 烧录后无反应 | 按 RESET 按钮，检查 BOOT0 是否接地 (Flash 启动模式) |

### 6.3 屏幕不显示

| 现象 | 可能原因 |
|------|---------|
| 白屏 | FSMC 未正确初始化，检查 FSMC 引脚配置 |
| 花屏 | 初始化序列不正确，或 FSMC 时序参数需调整 |
| 黑屏但有背光 | LCD 复位信号问题，检查 LCD_RST 连接 |
| 完全无显示 | 背光未开启，检查 PB0 (TIM3_CH3) PWM 输出 |

### 6.4 触摸不响应

| 现象 | 可能原因 |
|------|---------|
| 触摸完全无反应 | I2C2 通信失败，检查 PB10/PB11 是否有上拉电阻 |
| 触摸坐标偏移 | 需要坐标映射校准，FT5206 扫描方向与 LCD 不一致 |
| 触摸偶尔失灵 | I2C 总线干扰，降低 I2C 速度或增加延时 |

---

## 七、Keil MDK 用户替代方案

如果使用 Keil MDK-ARM 而非 GCC：

1. 创建新工程，选择 STM32F407ZGTx
2. 将 `Core/Src/` 和 `Core/Inc/` 中的文件添加到工程
3. 在 Keil 中配置 CMSIS 和 HAL 驱动路径
4. 在 `Options for Target -> C/C++` 中添加宏定义: `STM32F407xx,USE_HAL_DRIVER`
5. 在 `Options for Target -> Debug` 中选择 ST-Link Debugger
6. 编译 (F7) 后点击下载 (F8) 即可烧录

---

## 八、项目文件清单

```
firmware_f407_game/
├── Core/
│   ├── Inc/
│   │   ├── main.h          # 主头文件 (引脚定义)
│   │   ├── lcd.h            # LCD 驱动头文件
│   │   ├── touch.h          # 触摸驱动头文件
│   │   └── game.h           # 游戏逻辑头文件
│   └── Src/
│       ├── main.c           # 主程序 (初始化 + 主循环)
│       ├── lcd.c            # LCD 驱动 (ILI9341 FSMC)
│       ├── touch.c          # 触摸驱动 (FT5206 I2C)
│       └── game.c           # 游戏逻辑 (打地鼠)
├── Drivers/                 # HAL 库 (需手动从 STM32CubeF4 复制)
├── Inc/
│   ├── stm32f4xx_hal_conf.h # HAL 配置
│   └── stm32f4xx_it.h       # 中断声明
├── Src/
│   ├── stm32f4xx_it.c       # 中断处理
│   ├── system_stm32f4xx.c   # 系统初始化
│   ├── syscalls.c           # newlib 系统调用
│   └── sysmem.c             # 内存管理
├── Startup/
│   └── startup_stm32f407zgtx.s  # 启动文件
├── STM32F407ZGTX_FLASH.ld   # 链接脚本
├── Makefile                 # 构建规则
└── build.bat                # 一键构建脚本
```