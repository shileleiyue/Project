# 自平衡小车制作指南

> 你好！欢迎来到自平衡小车的世界！这份指南是专门为零基础的小白准备的，我会像老师教学生一样，一步步带你从零开始，亲手打造一辆属于自己的自平衡小车。
>
> **别怕！** 就算你以前没接触过单片机、没写过代码，只要跟着这份指南一步步来，你一定能成功！

---

## 目录

- [第一章 准备工作](#第一章-准备工作)
- [第二章 CubeMX 新建工程](#第二章-cubemx-新建工程)
- [第三章 GPIO 配置（CubeMX 操作）](#第三章-gpio-配置cubemx-操作)
- [第四章 TIM 定时器配置（CubeMX 操作 + 代码修改）](#第四章-tim-定时器配置cubemx-操作--代码修改)
- [第五章 I2C 和 USART 配置（CubeMX 操作）](#第五章-i2c-和-usart-配置cubemx-操作)
- [第六章 ADC 和 NVIC 配置（CubeMX 操作）](#第六章-adc-和-nvic-配置cubemx-操作)
- [第七章 应用层代码编写](#第七章-应用层代码编写)
- [第八章 编译烧录与调试](#第八章-编译烧录与调试)
- [第九章 蓝牙远程控制](#第九章-蓝牙远程控制)
- [第十章 后续升级](#第十章-后续升级)
- [附录](#附录)

---

## 第一章 准备工作

"工欲善其事，必先利其器。"在开始动手之前，我们先要把需要的材料和软件都准备好。

### 1.1 材料清单

下面是你需要准备的所有硬件材料，建议先对照清单检查一遍，确保一样都不少。

| 编号 | 材料名称 | 数量 | 说明 |
|:---:|:---|:---:|:---|
| 1 | STM32F103C8T6 最小系统板 | 1块 | 小车的"大脑"，负责所有计算和控制 |
| 2 | MPU6050 姿态传感器模块 | 1个 | 小车的"感觉器官"，感知倾斜角度 |
| 3 | TB6612 电机驱动模块 | 1个 | 小车的"肌肉"，驱动电机转动 |
| 4 | N20 微型减速电机（带编码器） | 2个 | 小车的"腿"，带动车轮 |
| 5 | 车轮（65mm 直径） | 2个 | 配套 N20 电机使用 |
| 6 | 车架/底盘 | 1个 | 安装所有零件 |
| 7 | 7.4V 锂电池（2S） | 1块 | 给小车的"心脏"供血 |
| 8 | HC-05 蓝牙模块 | 1个 | 让小车听懂你的手机指令 |
| 9 | ST-Link 下载器 | 1个 | 把程序"烧录"进 STM32 |
| 10 | CH340 USB 转串口模块 | 1个 | 用于调试时查看数据 |
| 11 | RGB LED 共阴极 | 1个 | 指示小车当前状态 |
| 12 | 有源蜂鸣器 | 1个 | 发出声音提示 |
| 13 | 杜邦线（公对公、公对母、母对母） | 若干 | 连接各个模块的"电线" |
| 14 | 面包板 | 1块 | 方便搭建电路，不用焊接 |
| 15 | 电阻（1kΩ、10kΩ 等） | 若干 | 分压、限流用 |

> **💡 提示：** 以上材料可以在淘宝上搜索"自平衡小车套件"，通常有现成的打包出售，比自己一个个买要方便很多。

### 1.2 接线总表

**这是整个指南中最重要的一节！** 接线错了，小车就无法正常工作。下表列出了 STM32 每个引脚要连接什么设备，请务必仔细核对。

> **⚠️ 警告：** 这是本指南中最重要的引脚表，后续所有操作都基于此表。如果你用的是网上其他教程，引脚可能不同，**请以本表为准！**

| STM32 引脚 | 功能 | 连接到 | 说明 |
|:---:|:---|:---|:---|
| **PA0** | TIM2_CH1 | 左编码器 A 相 | 左边电机的编码器信号线 A |
| **PA1** | TIM2_CH2 | 左编码器 B 相 | 左边电机的编码器信号线 B |
| **PB4** | TIM3_CH1 | 右编码器 A 相 | 右边电机的编码器信号线 A |
| **PB5** | TIM3_CH2 | 右编码器 B 相 | 右边电机的编码器信号线 B |
| **PA2** | TIM2_CH3 | 左电机 PWM（TB6612的PWMA） | 控制左电机速度 |
| **PA3** | TIM2_CH4 | 右电机 PWM（TB6612的PWMB） | 控制右电机速度 |
| **PB0** | GPIO_Output | TB6612 AIN1 | 左电机方向控制 1 |
| **PB1** | GPIO_Output | TB6612 AIN2 | 左电机方向控制 2 |
| **PB12** | GPIO_Output | TB6612 BIN1 | 右电机方向控制 1 |
| **PB13** | GPIO_Output | TB6612 BIN2 | 右电机方向控制 2 |
| **PB6** | I2C1_SCL | MPU6050 SCL | I2C 时钟线 |
| **PB7** | I2C1_SDA | MPU6050 SDA | I2C 数据线 |
| **PA9** | USART1_TX | HC-05 RXD | 蓝牙发送（接蓝牙的接收） |
| **PA10** | USART1_RX | HC-05 TXD | 蓝牙接收（接蓝牙的发送） |
| **PB14** | GPIO_Output | RGB LED 红色引脚 | 红色通道 |
| **PB15** | GPIO_Output | RGB LED 绿色引脚 | 绿色通道 |
| **PB8** | GPIO_Output | RGB LED 蓝色引脚 | 蓝色通道 |
| **PB3** | GPIO_Output | 蜂鸣器正极 | 发声控制 |
| **PA4** | ADC1_IN4 | 电池电压检测（经分压电阻） | 检测电池电量 |

> **⚠️ 警告——非常重要的引脚修正！**
>
> 1. **电机 PWM 使用的是 PA2(TIM2_CH3) 和 PA3(TIM2_CH4)，不是 PA6/PA7！** 很多网上教程用的是 PA6/PA7（对应 TIM4），但本项目使用的是 TIM2 的混合模式（编码器 + PWM 共用一个定时器）。
>
> 2. **电池检测使用的是 PA4(ADC1_IN4)，不是 PA2！** PA2 已经被电机 PWM 占用了。
>
> 3. **STM32F103C8T6 没有 PC0~PC4 引脚！** 这个芯片是 LQFP48 封装的，只有 48 个引脚。RGB LED 和蜂鸣器都接在 PB 引脚上。

### 1.3 软件安装

在开始编写代码之前，我们需要安装以下软件。请按顺序安装。

#### 1.3.1 STM32CubeMX

> **🔗 下载地址：** 在 ST 官网搜索 "STM32CubeMX" 即可找到下载链接

- **它是做什么的？** 这是一个图形化配置工具，你可以用鼠标点击的方式，配置 STM32 芯片的所有功能，然后它会自动生成 C 语言代码。省去了你手动写配置代码的麻烦。
- **安装步骤：**
  1. 打开安装程序，一路点击 **Next**（下一步）
  2. 接受许可协议（勾选 "I accept..."）
  3. 选择安装路径（默认即可）
  4. 点击 **Install** 等待安装完成
  5. 安装完成后，桌面会出现 STM32CubeMX 的图标

> **💡 提示：** 安装 CubeMX 需要 Java 运行环境，安装程序会自动提示你安装，按提示操作即可。

#### 1.3.2 Keil MDK-ARM v5

> **🔗 下载地址：** 在 ARM 官网搜索 "MDK-ARM"

- **它是做什么的？** 这是一个集成开发环境（IDE），用来编写、编译、调试 STM32 的代码。简单说，它就是你的"代码编辑器+编译器"。
- **安装步骤：**
  1. 运行安装程序，点击 **Next**
  2. 勾选同意协议，点击 **Next**
  3. 选择安装路径（默认即可）
  4. 填写你的信息（名称、邮箱等，随便填即可）
  5. 点击 **Install**，等待安装完成
  6. 安装完成后，桌面会出现 Keil uVision5 的图标

> **⚠️ 注意：** Keil MDK 是一个商业软件，需要 License（许可证）。如果你没有正版 license，可以申请试用版（30 天评估版），基本够用了。

#### 1.3.3 ST-Link 驱动

- **它是做什么的？** ST-Link 下载器需要通过 USB 连接到电脑，这个驱动就是让电脑认识 ST-Link 的"翻译官"。
- **安装步骤：**
  1. 从 ST 官网搜索 "ST-Link driver" 下载驱动安装包
  2. 运行安装程序，点击 **Next** → **Install**
  3. 安装完成后，将 ST-Link 插入电脑 USB 口，电脑应该能识别到新硬件

> **✅ 验证方法：** 打开电脑的"设备管理器"，展开"通用串行总线设备"，应该能看到 "ST-Link" 相关的设备。

#### 1.3.4 CH340 驱动

- **它是做什么的？** CH340 是一个 USB 转串口芯片，我们用它来和 STM32 通信，查看调试信息。
- **安装步骤：**
  1. 搜索 "CH340 驱动下载"
  2. 下载对应你操作系统版本的驱动
  3. 运行安装程序，点击 **安装**
  4. 安装完成后，将 CH340 模块插入电脑 USB 口，设备管理器中会多出一个"COM 端口"

> **💡 提示：** 记下这个 COM 端口号（比如 COM3、COM5 等），后面调试时要用到。

---

## 第二章 CubeMX 新建工程

现在开始，我们就要动手操作了！打开 STM32CubeMX，开始创建我们的第一个项目。

### 2.1 打开 CubeMX 并新建工程

1. 双击桌面上的 **STM32CubeMX** 图标，启动软件
2. 软件启动后，你会看到一个欢迎界面。点击 **"New Project"** 按钮（或者点击菜单栏的 **File → New Project**）

> **💡 提示：** 如果软件提示你更新，可以先跳过，直接使用当前版本。

### 2.2 选择芯片型号

1. 在弹出的芯片选择窗口中，你会看到两个标签页：**MCU Selector**（单片机选择器）和 **Board Selector**（开发板选择器）
2. 确保你选中的是 **MCU Selector** 标签页
3. 在左上角的搜索框中输入：**STM32F103C8**
4. 在搜索结果列表中，找到 **STM32F103C8Tx**（注意看后面的封装是 LQFP48）
5. 双击这一行，或者选中后点击右上角的 **"Start Project"** 按钮

> **💡 为什么选择这款芯片？** STM32F103C8T6 是市面上最常见、最便宜的 ARM 单片机之一，性能足够驱动自平衡小车，而且资料丰富，非常适合入门。

### 2.3 配置 SYS（系统调试接口）

1. 在 CubeMX 的 **Pinout & Configuration** 标签页中，找到左侧的类别列表
2. 展开 **System Core**（系统核心）
3. 点击 **SYS**
4. 在右侧的配置面板中，找到 **Debug** 选项
5. 点击下拉菜单，选择 **Serial Wire**

> **💡 为什么这么做？** STM32 的调试接口默认是 JTAG（5 根线），但 JTAG 占用了很多引脚。我们选择 Serial Wire（SWD，只用 2 根线：SWDIO 和 SWCLK），这样可以释放更多引脚给其他功能使用。**如果不设置这一步，PA15/PB3/PB4 等引脚会被调试功能占用，导致这些引脚无法正常使用。**

> **⚠️ 警告：** 如果不选择 Serial Wire，后面你可能会发现 PB3（蜂鸣器）、PB4（编码器）等引脚不受控制，因为它们被 JTAG 占用了！

### 2.4 配置 RCC（时钟源）

1. 在左侧的 **System Core** 中，点击 **RCC**
2. 在右侧的配置面板中，找到 **High Speed Clock (HSE)** 选项
3. 点击下拉菜单，选择 **Crystal/Ceramic Resonator**

> **💡 为什么这么做？** HSE（高速外部时钟）就是我们板子上的 8MHz 晶振，它提供精确的时钟信号。我们选择晶体/陶瓷谐振器，告诉 STM32 外部有一个 8MHz 的晶振。

### 2.5 配置时钟树

这是最关键的一步，我们要把 STM32 的"心脏"（时钟）加速到 72MHz。

1. 在 CubeMX 的顶部，切换到 **Clock Configuration** 标签页
2. 你会看到一个复杂的时钟树图表，别慌，我们只需要关注几个关键点
3. 找到 **HSE** 输入，确认它显示的是 **8**（代表 8MHz 晶振）
4. 找到 **PLL Source**（PLL 时钟源），选择 **HSE**
5. 找到 **PLL Mul**（PLL 倍频系数），在输入框中输入 **x9**（或者从下拉菜单中选择 9）
6. 找到 **SYSCLK**（系统时钟），确保它显示为 **72MHz**（或者点击它，输入 72，回车）
7. 观察时钟树，确认所有总线时钟（AHB、APB1、APB2）都为绿色，且数值正确

> **💡 为什么是 72MHz？** 外部晶振是 8MHz，PLL 倍频 9 倍：8MHz × 9 = 72MHz。这是 STM32F103C8T6 的最高工作频率，就像汽车发动机的"最高转速"。跑得越快，处理能力越强，小车才能更灵敏地做出反应。

> **⚠️ 注意：**
> - APB1 总线时钟应该是 36MHz（72MHz 的一半）
> - APB2 总线时钟应该是 72MHz
> - 如果时钟树中出现红色，说明配置有问题，请检查 PLL 设置

### 2.6 项目管理

1. 切换到 **Project Manager** 标签页
2. 在 **Project Name** 输入框中，输入项目名称：**balancer_car**
3. 在 **Project Location** 中，选择你希望保存项目的目录
4. 在 **Toolchain / IDE** 下拉菜单中，选择 **MDK-ARM v5**

> **💡 为什么选择 MDK-ARM v5？** 这就是我们之前安装的 Keil uVision5 的"官方名称"。选择它，CubeMX 生成的项目文件就能直接被 Keil 打开。

### 2.7 代码生成设置

1. 在 **Project Manager** 标签页中，点击左侧的 **Code Generator**
2. 勾选 **"Generate peripheral initialization as a pair of .c/.h files per peripheral"**

> **💡 为什么勾选这个选项？** 如果不勾选，所有外设的初始化代码都会放在一个巨大的 main.c 文件中，找起来很麻烦。勾选后，每个外设会有独立的 .c 和 .h 文件，代码结构更清晰，比如 `i2c.c`、`usart.c` 等。不过在本项目中，我们直接在 main.c 中手写所有初始化代码，这个选项的目的是让代码生成更灵活。

### 2.8 生成代码

1. 点击右上角的 **GENERATE CODE** 按钮
2. 如果弹出提示框，询问是否覆盖已有文件，选择 **Yes**
3. 等待 CubeMX 自动生成代码（这个过程可能需要几十秒）
4. 生成完成后，会弹出一个提示框，点击 **Open Project** 可以直接打开 Keil 项目

> **✅ 恭喜！** 到此为止，你已经成功创建了一个 STM32 工程！虽然目前这个工程还只是一个"空壳"，但我们已经打好了一个坚实的基础。

---

## 第三章 GPIO 配置（CubeMX 操作）

现在我们要配置每个引脚的具体功能。在 CubeMX 的 **Pinout View**（引脚视图）中，你可以看到芯片的引脚图，每个引脚都可以点击，选择它要承担的角色。

### 3.1 引脚配置表

请在 **Pinout View** 中，依次点击下表列出的每个引脚，选择对应的功能：

| 引脚 | 配置为 | 说明 |
|:---:|:---|:---|
| PA0 | TIM2_CH1 | 左编码器 A 相输入 |
| PA1 | TIM2_CH2 | 左编码器 B 相输入 |
| PB4 | TIM3_CH1 | 右编码器 A 相输入 |
| PB5 | TIM3_CH2 | 右编码器 B 相输入 |
| PA2 | TIM2_CH3 | 左电机 PWM 输出 |
| PA3 | TIM2_CH4 | 右电机 PWM 输出 |
| PB0 | GPIO_Output | 左电机方向 1 |
| PB1 | GPIO_Output | 左电机方向 2 |
| PB12 | GPIO_Output | 右电机方向 1 |
| PB13 | GPIO_Output | 右电机方向 2 |
| PB6 | I2C1_SCL | MPU6050 时钟线 |
| PB7 | I2C1_SDA | MPU6050 数据线 |
| PA9 | USART1_TX | 蓝牙发送 |
| PA10 | USART1_RX | 蓝牙接收 |
| PB14 | GPIO_Output | RGB LED 红色 |
| PB15 | GPIO_Output | RGB LED 绿色 |
| PB8 | GPIO_Output | RGB LED 蓝色 |
| PB3 | GPIO_Output | 蜂鸣器 |
| PA4 | ADC1_IN4 | 电池电压检测 |

> **💡 操作提示：** 在 Pinout View 中，将鼠标悬停在某个引脚上，会显示这个引脚当前的功能。点击它，会弹出一个菜单，列出所有可用的功能。找到你要的功能，点击即可。

### 3.2 设置 GPIO_Output 引脚的初始电平

对于配置为 GPIO_Output 的引脚，我们需要设置它们的默认状态：

1. 在左侧 **Pinout & Configuration** 中，点击 **System Core → GPIO**
2. 在右侧的 GPIO 列表中，找到 PB0、PB1、PB12、PB13、PB14、PB15、PB8、PB3
3. 对于每个引脚，检查 **GPIO output level** 是否设置为 **Low**（低电平，即 0V）

> **💡 为什么默认设成低电平？** 这些引脚连接的设备（电机驱动、LED、蜂鸣器）在低电平时处于关闭状态，防止小车一上电就乱动。

### 3.3 未使用引脚的处理

把没有被使用的引脚设置为 **Analog**（模拟）模式，可以降低功耗，减少干扰。

1. 在 Pinout View 中，找到所有没有被使用的引脚
2. 点击它们，选择 **Analog**（或者 **GPIO_Analog**）

> **💡 提示：** 未使用的引脚如果不设置，可能会处于"悬空"状态，电平不确定，容易受外界干扰，甚至导致芯片耗电增加。

### 3.4 特别警告

> **⚠️ 警告——STM32F103C8T6 引脚限制！**
>
> **STM32F103C8T6 是 LQFP48 封装，只有 48 个引脚，没有 PC0、PC1、PC2、PC3、PC4 这些引脚！**
>
> 很多网上教程用的是 STM32F103C8T6 的"大号版本"（如 100 引脚的型号），它们有 PC 引脚。**如果你跟着那些教程把 LED 接到 PC0~PC2，你会发现 LED 根本不亮，因为芯片根本没有这些引脚！**
>
> 本项目中，RGB LED 的三个引脚改到了 PB14（红）、PB15（绿）、PB8（蓝），蜂鸣器改到了 PB3。**请务必确认你的接线使用的是正确的引脚！**

---

## 第四章 TIM 定时器配置（CubeMX 操作 + 代码修改）

定时器是 STM32 中非常重要的外设，它就像"电子秒表"，可以精确计时、测量信号、产生脉冲。我们的小车要用到 3 个定时器。

### 4.1 TIM2 配置（左编码器 + 电机 PWM 混合模式）

**TIM2 是本项目中最特殊的定时器，因为它同时承担两种任务：**
- CH1/CH2（PA0/PA1）：左编码器输入（读取电机转速）
- CH3/CH4（PA2/PA3）：PWM 输出（控制电机速度）

这种"一半输入一半输出"的模式叫做**混合模式**。

#### 4.1.1 在 CubeMX 中配置 TIM2

1. 在左侧的 **Timers** 类别中，点击 **TIM2**
2. 在 **Mode** 标签页中，找到 **Channel1** 和 **Channel2**，将它们都设置为 **Encoder Mode**（编码器模式）
3. 找到 **Channel3** 和 **Channel4**，将它们都设置为 **PWM Generation CHx**（PWM 生成）
4. 切换到 **Configuration** 标签页，进行参数设置：
   - **Prescaler（预分频器）**：输入 **0**（编码器部分不需要分频）
   - **Counter Mode（计数模式）**：选择 **Up**（向上计数）
   - **Counter Period（自动重载值）**：输入 **65535**（0xFFFF）
   - **Encoder Mode（编码器模式）**：选择 **TI1 and TI2**（双沿触发，4 倍频）
5. 切换到 **Parameter Settings** 标签页，设置 PWM 部分的参数：
   - **Prescaler（预分频器）**：输入 **71**（72-1，让 72MHz → 1MHz）
   - **Counter Mode（计数模式）**：选择 **Up**
   - **Counter Period（自动重载值）**：输入 **999**（1000-1，让 1MHz → 1kHz）
   - **Auto-reload preload（自动重载预装载）**：选择 **Enable**

> **⚠️ 注意——CubeMX 的局限性：**
>
> CubeMX 对 TIM2 的混合模式支持有限，它可能无法同时正确处理编码器模式和 PWM 模式。**生成的代码可能需要手动修改。** 别担心，在第七章中，会提供完整的代码，你只需要复制粘贴即可。

#### 4.1.2 编码器工作原理（通俗解释）

想象一下，你手里有一把尺子，你要测量一个轮子转了多少圈。

- **编码器** 就像一个"电子尺子"，它可以精确测量电机的转动角度和方向
- N20 电机内部的编码器每转一圈会产生 **390 个脉冲**
- TIM2 使用 **TI1 and TI2 模式**（也叫 4 倍频模式），可以把 390 个脉冲变成 **390 × 4 = 1560 个计数**
- 通过读取定时器的计数值变化，就能知道电机转了多少、转得快慢、以及是正转还是反转

**公式：**
```
速度（mm/s）= 脉冲数差值 × 轮胎周长 ÷ （编码器线数 × 减速比） × 控制频率
```

#### 4.1.3 PWM 频率计算

PWM 就是"脉冲宽度调制"，通过快速开关电源，控制电机的平均电压。

- STM32 的系统时钟（APB1 总线）是 **36MHz**
- TIM2 挂载在 APB1 上，由于 APB1 预分频器=2，实际 TIM2 时钟 = **72MHz**（因为定时器有倍频机制）
- 预分频器设为 **72-1=71**，所以 TIM2 计数频率 = 72MHz ÷ 72 = **1MHz**
- 自动重载值设为 **1000-1=999**，所以 PWM 频率 = 1MHz ÷ 1000 = **1kHz**

> **💡 为什么用 1kHz？** 1kHz 意味着一秒钟产生 1000 个 PWM 脉冲，电机对这种频率响应良好，既不会产生噪音，也不会让电机抖动。

### 4.2 TIM3 配置（右编码器）

1. 在左侧的 **Timers** 类别中，点击 **TIM3**
2. 在 **Mode** 标签页中，将 **Channel1** 和 **Channel2** 都设置为 **Encoder Mode**
3. 参数设置：
   - **Prescaler**：**0**
   - **Counter Period**：**65535**（0xFFFF）
   - **Encoder Mode**：**TI1 and TI2**

> **⚠️ 注意——TIM3 引脚重映射！**
>
> STM32 的 TIM3 默认引脚是 PA6（CH1）和 PA7（CH2），但这两个引脚被其他功能占用了。我们需要将 TIM3 的通道重映射到 PB4（CH1）和 PB5（CH2）。
>
> 在代码中，我们需要手动添加：
> ```c
> __HAL_RCC_AFIO_CLK_ENABLE();
> __HAL_AFIO_REMAP_TIM3_PARTIAL();  // 部分重映射
> ```
> 这部分在 CubeMX 中无法直接配置，需要我们在代码中手动添加。

### 4.3 TIM1 配置（1kHz 控制定时器）

TIM1 是我们的"控制心跳"——它每 1ms 产生一次中断，告诉 CPU"该执行控制算法了！"

**TIM1 在 CubeMX 中不需要配置，我们直接在代码中手动初始化。** 原因是 TIM1 是高级定时器，配置稍微复杂，手动写代码更清晰。

> **💡 为什么需要 1kHz 控制？** 自平衡小车需要在很短的时间内不断检测倾斜角度并做出调整。1kHz 意味着每 1 毫秒就调整一次，这个速度足够快，能让小车保持平衡。

**TIM1 的参数计算：**
- TIM1 挂载在 APB2 上，时钟 = 72MHz
- 预分频器 = 72-1，计数频率 = 72MHz ÷ 72 = 1MHz
- 自动重载值 = 1000-1，中断频率 = 1MHz ÷ 1000 = 1kHz

---

## 第五章 I2C 和 USART 配置（CubeMX 操作）

### 5.1 I2C1 配置（连接 MPU6050）

I2C 是一种"两根线"的通信协议，可以连接多个设备。我们用它来读取 MPU6050 姿态传感器数据。

1. 在左侧的 **Connectivity**（连接性）中，点击 **I2C1**
2. 在 **Mode** 标签页中，将 **I2C** 设置为 **I2C**（使能 I2C 外设）
3. 切换到 **Parameter Settings** 标签页，设置参数：
   - **I2C Speed Mode（速度模式）**：选择 **Fast Mode**（快速模式）
   - **I2C Clock Speed（时钟频率）**：输入 **400000**（400kHz）

> **💡 为什么用 400kHz？**
>
> I2C 有两种速度模式：
> - **Standard Mode（标准模式）**：100kHz，慢速但稳定
> - **Fast Mode（快速模式）**：400kHz，速度更快
>
> MPU6050 支持 400kHz 的快速模式，我们用更快的速度读取数据，可以获取更及时的传感器信息。

> **💡 I2C 工作原理：**
> - SCL（时钟线）：由主设备（STM32）控制，决定数据传输的节奏
> - SDA（数据线）：传输实际的数据
> - 每个 I2C 设备都有一个唯一的地址，MPU6050 的地址是 **0x68**
> - 通信时，STM32 先发送设备地址，然后发送要读取的寄存器地址，最后接收数据

### 5.2 USART1 配置（连接蓝牙模块）

USART 是一种"串行通信"协议，通俗地说，就是"一根线发、一根线收"。

1. 在左侧的 **Connectivity** 中，点击 **USART1**
2. 在 **Mode** 标签页中，将 **Mode** 设置为 **Asynchronous**（异步模式）
3. 切换到 **Parameter Settings** 标签页，设置参数：
   - **Baud Rate（波特率）**：输入 **115200**（传输速度）
   - **Word Length（数据位）**：选择 **8 Bits**（8 位数据）
   - **Parity（校验位）**：选择 **None**（无校验）
   - **Stop Bits（停止位）**：选择 **1**（1 位停止位）

> **💡 每个参数是什么？**
>
> - **波特率 115200**：一秒钟传输 115200 个比特（二进制位），相当于每秒约 11520 个字符。这是蓝牙模块常用的速度。
> - **8 位数据**：每次传输 8 位（1 字节）数据，这是最常见的设置。
> - **无校验**：不检查数据是否传错，简单可靠。
> - **1 位停止位**：每传输完一字节，发一个停止信号。

#### 5.2.1 使能 USART1 中断

1. 在 USART1 的配置中，切换到 **NVIC Settings** 标签页
2. 勾选 **USART1 global interrupt**（USART1 全局中断）

> **💡 为什么需要中断？**
>
> 如果不使用中断，STM32 需要不停地"轮询"（反复检查）有没有收到数据，这会浪费大量 CPU 时间。使用中断后，当有数据到达时，USART 会自动通知 CPU 来处理，CPU 平时可以专心做其他事情。

---

## 第六章 ADC 和 NVIC 配置（CubeMX 操作）

### 6.1 ADC1 配置（电池电压检测）

ADC 是"模数转换器"，可以把模拟电压（比如电池的 7.4V）转换成数字信号（0~4095 之间的数值），让 STM32 能够"读懂"电压。

1. 在左侧的 **Analog**（模拟）中，点击 **ADC1**
2. 在 **Configuration** 标签页中，点击 **Analog channel conversion** 下面的 **"Add"** 按钮
3. 在弹出的窗口中，选择 **Channel 4**（对应 PA4 引脚）
4. 设置 **Sampling Time（采样时间）**：选择 **55.5 Cycles**（55.5 个时钟周期）

> **💡 采样时间是什么意思？**
> ADC 需要花一点时间来"测量"电压，采样时间就是用来测量的时间。55.5 个时钟周期是比较适中的值，测量结果比较准确，速度也够快。

> **💡 电压换算公式：**
> ```
> 实际电压 = ADC值 × 3.3V ÷ 4096 × 分压比
> ```
> - ADC 是 12 位的，所以数值范围是 0~4095
> - 参考电压是 3.3V（STM32 的工作电压）
> - 分压比取决于你外接的分压电阻（比如两个 10kΩ 电阻串联，分压比就是 2）

### 6.2 NVIC 配置（中断优先级）

NVIC 是"嵌套向量中断控制器"，负责管理所有中断的优先级。可以把它想象成一个"紧急事务处理中心"——当多个中断同时发生时，它决定先处理哪个。

1. 在左侧的 **System Core** 中，点击 **NVIC**
2. 在 **NVIC** 标签页中，设置 **Priority Group（优先级分组）** 为 **4 bits for pre-emption priority**（4 位抢占优先级，即 0~15 级）

> **💡 为什么这么设置？** 4 位优先级意味着有 16 个优先级等级（0 最高，15 最低），足够我们使用。

3. 在 **NVIC** 的 **NVIC Interrupts Table** 中，找到并勾选以下中断：
   - **TIM1 update interrupt**（TIM1 更新中断）——控制循环
   - **USART1 global interrupt**（USART1 全局中断）——蓝牙通信
   - **USART2 global interrupt**（USART2 全局中断）——语音模块（可选）

4. 为每个中断设置优先级（数值越小优先级越高）：
   - TIM1：**1**（最高优先级，因为控制算法必须准时执行）
   - USART1：**2**（次高优先级）
   - USART2：**2**（与 USART1 同级）

> **⚠️ 注意：SysTick 优先级**
>
> SysTick 是一个"系统滴答定时器"，HAL 库用它来做延时（如 `HAL_Delay()`）。它的优先级应该设为**最低**，以免影响其他中断。
>
> 在代码中，我们会添加：
> ```c
> HAL_NVIC_SetPriority(SysTick_IRQn, 15, 0);  // 优先级最低
> ```

> **💡 为什么 TIM1 优先级最高？** 自平衡控制是"实时"任务，每 1ms 必须执行一次，如果被其他中断耽误了，小车可能会失去平衡摔倒。所以它的优先级最高。

---

## 第七章 应用层代码编写

**这是最详细的一章！** 从现在开始，我们不再使用 CubeMX 的图形化界面，而是要手动编写代码了。

### 7.1 文件结构概览

我们需要手动创建以下文件：

| 文件 | 功能 |
|:---|:---|
| `motor.c / motor.h` | 电机驱动（控制速度和方向） |
| `encoder.c / encoder.h` | 编码器读取（测量速度） |
| `mpu6050.c / mpu6050.h` | MPU6050 姿态传感器驱动 |
| `pid.c / pid.h` | PID 控制器（平衡算法核心） |
| `uart_protocol.c / uart_protocol.h` | 串口通信协议 |
| `power_manager.c / power_manager.h` | 电源管理（电池检测、摔倒保护） |
| `indicator.c / indicator.h` | 指示灯和蜂鸣器 |

这些文件存放在 `firmware_keil/Core/Src/`（源文件）和 `firmware_keil/Core/Inc/`（头文件）目录下。

### 7.2 main.h —— 主头文件（引脚定义和全局变量）

**文件位置：** `firmware_keil/Core/Inc/main.h`

这个文件是所有代码的"总枢纽"，定义了引脚映射、系统参数和全局变量声明。

**引脚定义：**
```c
// ======================== 引脚定义 ========================

// 左电机 PWM - PA2 (TIM2_CH3)
#define LEFT_MOTOR_PWM_PORT       GPIOA
#define LEFT_MOTOR_PWM_PIN        GPIO_PIN_2
#define LEFT_MOTOR_PWM_TIM        TIM2
#define LEFT_MOTOR_PWM_CHANNEL    TIM_CHANNEL_3

// 左电机方向 - PB0, PB1
#define LEFT_MOTOR_DIR1_PORT      GPIOB
#define LEFT_MOTOR_DIR1_PIN       GPIO_PIN_0
#define LEFT_MOTOR_DIR2_PORT      GPIOB
#define LEFT_MOTOR_DIR2_PIN       GPIO_PIN_1

// 右电机 PWM - PA3 (TIM2_CH4)
#define RIGHT_MOTOR_PWM_PORT      GPIOA
#define RIGHT_MOTOR_PWM_PIN       GPIO_PIN_3
#define RIGHT_MOTOR_PWM_TIM       TIM2
#define RIGHT_MOTOR_PWM_CHANNEL   TIM_CHANNEL_4

// 右电机方向 - PB12, PB13
#define RIGHT_MOTOR_DIR1_PORT     GPIOB
#define RIGHT_MOTOR_DIR1_PIN      GPIO_PIN_12
#define RIGHT_MOTOR_DIR2_PORT     GPIOB
#define RIGHT_MOTOR_DIR2_PIN      GPIO_PIN_13

// 左编码器 - PA0 (TIM2_CH1), PA1 (TIM2_CH2)
#define LEFT_ENCODER_TIM          TIM2
#define LEFT_ENCODER_CH1_PIN      GPIO_PIN_0
#define LEFT_ENCODER_CH2_PIN      GPIO_PIN_1

// 右编码器 - PB4 (TIM3_CH1), PB5 (TIM3_CH2)
#define RIGHT_ENCODER_TIM         TIM3
#define RIGHT_ENCODER_CH1_PIN     GPIO_PIN_4
#define RIGHT_ENCODER_CH2_PIN     GPIO_PIN_5

// MPU6050 - I2C1: PB6(SCL), PB7(SDA)
#define MPU6050_I2C               hi2c1
#define MPU6050_ADDR              0x68

// RGB LED - PB14(R), PB15(G), PB8(B)
#define LED_R_PORT                GPIOB
#define LED_R_PIN                 GPIO_PIN_14
#define LED_G_PORT                GPIOB
#define LED_G_PIN                 GPIO_PIN_15
#define LED_B_PORT                GPIOB
#define LED_B_PIN                 GPIO_PIN_8

// 蜂鸣器 - PB3
#define BUZZER_PORT               GPIOB
#define BUZZER_PIN                GPIO_PIN_3

// UART1 - 蓝牙/调试: PA9(TX), PA10(RX)
#define UART_DEBUG                huart1
```

**系统状态枚举：**
```c
typedef enum {
    SYSTEM_INIT      = 0,   // 初始化
    SYSTEM_STARTUP   = 1,   // 启动中
    SYSTEM_BALANCING = 2,   // 平衡中
    SYSTEM_LOW_BAT   = 3,   // 低电量
    SYSTEM_FALLEN    = 4,   // 摔倒保护
    SYSTEM_SLEEP     = 5,   // 休眠
    SYSTEM_ERROR     = 6    // 错误
} SystemState_t;
```

**系统参数：**
```c
// 控制频率 1kHz
#define CONTROL_FREQ_HZ           1000
#define CONTROL_PERIOD_MS         1

// PWM 参数
#define PWM_PERIOD                1000
#define PWM_MAX_OUTPUT            1000
#define PWM_MIN_OUTPUT            -1000

// 编码器参数
#define ENCODER_PPR               390       // 编码器线数
#define WHEEL_DIAMETER_MM         65        // 轮径 mm
#define WHEEL_CIRCUMFERENCE_MM    (WHEEL_DIAMETER_MM * 3.14159f)

// 摔倒保护阈值
#define FALL_TILT_THRESHOLD       45.0f     // 倾角超过45度认为摔倒
```

**全局变量声明：**
```c
extern SystemState_t g_system_state;
extern float g_pitch_angle;         // 当前倾角
extern float g_left_speed;          // 左轮速度
extern float g_right_speed;         // 右轮速度
extern float g_target_speed;        // 目标速度
extern float g_target_turn;         // 目标转向
extern float g_battery_voltage;     // 电池电压
extern uint32_t g_sys_tick_ms;      // 系统运行毫秒
```

> **💡 什么是 `extern`？** `extern` 是 C 语言中的一个关键字，意思是"这个变量在别的地方定义了"。变量在 main.c 中定义，如果在其他文件中也要使用，就需要用 `extern` 声明一下。

### 7.3 motor.c / motor.h —— 电机驱动

**文件位置：** `firmware_keil/Core/Src/motor.c` 和 `firmware_keil/Core/Inc/motor.h`

**电机驱动的作用：** 控制小车两个轮子的转动速度和方向。

#### 电机结构体

```c
typedef struct {
    TIM_HandleTypeDef *pwm_tim;     // PWM定时器
    uint32_t pwm_channel;           // PWM通道
    TIM_HandleTypeDef *encoder_tim; // 编码器定时器

    GPIO_TypeDef *dir1_port;        // 方向1端口
    uint16_t dir1_pin;              // 方向1引脚
    GPIO_TypeDef *dir2_port;        // 方向2端口
    uint16_t dir2_pin;              // 方向2引脚

    int16_t current_pwm;            // 当前PWM值
    int16_t last_encoder_cnt;       // 上次编码器计数值
    float speed;                    // 当前速度
} Motor_TypeDef;
```

> **💡 结构体是什么？** 结构体就像是一个"收纳盒"，把相关的信息放在一起。比如电机的"收纳盒"里就放了：这个电机用哪个定时器、哪个通道、哪几个引脚来控制方向、当前速度是多少等等。

#### 关键函数说明

**`void Motor_Init(void)`** —— 初始化电机
- **作用：** 设置电机结构体的各个参数，告诉代码"左电机用哪个引脚、右电机用哪个引脚"
- **调用时机：** 程序启动时调用一次

**`void Motor_SetSpeed(Motor_TypeDef *motor, int16_t speed)`** —— 设置电机速度
- **参数：** `motor` 是电机结构体指针（指定左电机还是右电机），`speed` 是速度值（-1000~1000）
- **作用：** 控制电机正转、反转或刹车
- **方向控制逻辑：**
  - `speed > 0`：正转（前进），方向引脚 1 输出高电平，方向引脚 2 输出低电平
  - `speed < 0`：反转（后退），方向引脚 1 输出低电平，方向引脚 2 输出高电平
  - `speed == 0`：刹车，两个方向引脚都输出高电平

**`void Motor_Brake(Motor_TypeDef *motor)`** —— 刹车
- **作用：** 让电机紧急停止（短接电机两端，产生阻力）

**`void Motor_Stop(Motor_TypeDef *motor)`** —— 停止（自由滑行）
- **作用：** 让电机自由停止（不施加任何阻力，靠摩擦力自然停下）

**`void Motor_StopAll(void)`** —— 停止所有电机
- **作用：** 同时停止左右两个电机

#### 电机控制逻辑详解

```
TB6612 电机驱动器的控制逻辑：
   AIN1 | AIN2  | 电机状态
   -----|-------|----------
    0   |   0   | 刹车（停止）
    1   |   0   | 正转（前进）
    0   |   1   | 反转（后退）
    1   |   1   | 刹车（停止）
```

> **💡 为什么需要两个方向引脚？** 一个引脚控制正向，一个引脚控制反向，通过它们的组合，可以实现四种状态：停止、前进、后退、刹车。这就像汽车的"前进挡"和"倒挡"。

### 7.4 encoder.c / encoder.h —— 编码器读取

**文件位置：** `firmware_keil/Core/Src/encoder.c` 和 `firmware_keil/Core/Inc/encoder.h`

**编码器的作用：** 测量电机实际转动的速度和距离。

#### 编码器结构体

```c
typedef struct {
    TIM_HandleTypeDef *timer;   // 编码器定时器
    int16_t last_count;         // 上次读取的计数值
    float speed;                // 换算后的速度（mm/s）
    float total_distance;       // 累计距离（mm）
} Encoder_TypeDef;
```

#### 关键函数说明

**`void Encoder_Init(void)`** —— 初始化编码器
- **作用：** 设置左编码器使用 TIM2，右编码器使用 TIM3
- **调用时机：** 程序启动时调用一次

**`float Encoder_ReadSpeed(Encoder_TypeDef *enc)`** —— 读取速度
- **参数：** `enc` 是编码器结构体指针
- **返回值：** 速度值，单位是 mm/s（毫米每秒）
- **作用：** 读取编码器当前计数值，减去上次的计数值，得到"差值"，再通过公式换算成速度
- **调用时机：** 每 1ms 调用一次（在定时器中断中）

**速度计算公式：**
```c
float speed = (float)delta * WHEEL_CIRCUMFERENCE_MM 
              / (ENCODER_PULSES_PER_REV * MOTOR_GEAR_RATIO) * 1000.0f;
```

**拆解公式：**
- `delta`：1ms 内的脉冲数差值
- `WHEEL_CIRCUMFERENCE_MM`：轮胎周长 = 65mm × π ≈ 204.2mm
- `ENCODER_PULSES_PER_REV`：编码器每转脉冲数 = 390
- `MOTOR_GEAR_RATIO`：电机减速比 = 30:1
- `* 1000`：因为 1ms 测一次，要换算成每秒的速度

**简化计算：** 每 1ms 差值 × 204.2 ÷ (390 × 30) × 1000 = 差值 × 17.45 mm/s

> **💡 减速比是什么意思？** N20 电机内部有一个齿轮箱，电机本身转 30 圈，输出轴才转 1 圈。这样虽然速度慢了，但力气变大了（扭矩增加了），小车才能站得稳。

### 7.5 mpu6050.c / mpu6050.h —— 姿态传感器驱动

**文件位置：** `firmware_keil/Core/Src/mpu6050.c` 和 `firmware_keil/Core/Inc/mpu6050.h`

**MPU6050 的作用：** 它是小车的"平衡感"，可以感知小车倾斜了多少度、倾斜的速度有多快。

#### 数据结构

```c
// 原始数据（从传感器直接读取的数值）
typedef struct {
    int16_t accel_x;    // 加速度 X 轴
    int16_t accel_y;    // 加速度 Y 轴
    int16_t accel_z;    // 加速度 Z 轴
    int16_t temp;       // 温度
    int16_t gyro_x;     // 陀螺仪 X 轴角速度
    int16_t gyro_y;     // 陀螺仪 Y 轴角速度
    int16_t gyro_z;     // 陀螺仪 Z 轴角速度
} MPU6050_DataRaw_t;

// 换算后的物理量
typedef struct {
    float accel_x;      // 加速度 (单位: g)
    float accel_y;
    float accel_z;
    float temp;         // 温度 (单位: °C)
    float gyro_x;       // 角速度 (单位: °/s)
    float gyro_y;
    float gyro_z;
} MPU6050_DataScaled_t;
```

#### 关键函数说明

**`uint8_t MPU6050_Init(I2C_HandleTypeDef *hi2c)`** —— 初始化 MPU6050
- **参数：** `hi2c` 是 I2C 句柄指针（我们传 `&hi2c1`）
- **返回值：** 0 表示成功，1 表示失败
- **作用：**
  1. 检查设备 ID（应为 0x68）
  2. 退出睡眠模式
  3. 设置采样率为 1kHz
  4. 设置数字低通滤波器为 44Hz（过滤高频噪声）
  5. 设置陀螺仪量程为 ±250°/s
  6. 设置加速度计量程为 ±2g

**`void MPU6050_ReadAll(MPU6050_DataRaw_t *raw)`** —— 一次性读取所有数据
- **参数：** `raw` 是输出参数，读取的数据会填到这里
- **作用：** 从 MPU6050 的寄存器中一次读取 14 个字节，包含加速度、温度、陀螺仪数据

**`void MPU6050_ScaleData(...)`** —— 换算数据
- **作用：** 把原始数字（比如 16384）换算成物理量（比如 1g 重力加速度）
- **换算公式：**
  - 加速度：原始值 ÷ 16384（因为 ±2g 量程，灵敏度 16384 LSB/g）
  - 陀螺仪：原始值 ÷ 131（因为 ±250°/s 量程，灵敏度 131 LSB/°/s）
  - 温度：原始值 ÷ 340 + 36.53

**`float MPU6050_CalcAccPitch(float ax, float ay, float az)`** —— 计算倾斜角度
- **作用：** 利用加速度计数据计算当前倾斜角度
- **公式：** `atan2(-ax, sqrt(ay² + az²)) × 180/π`
- **返回值：** 角度值（度），小车向前倾斜为正

**`float MPU6050_ComplementaryFilter(float gyro_rate, float acc_angle, float dt)`** —— 角度融合
- **参数：** `gyro_rate` 是陀螺仪角速度，`acc_angle` 是加速度计角度，`dt` 是时间间隔（0.001s）
- **返回值：** 融合后的角度
- **作用：** 把陀螺仪和加速度计的数据"融合"在一起，得到一个更准确的角度

> **💡 为什么需要互补滤波？**
>
> - **陀螺仪** 测量角速度，短期很准，但长期会"漂移"（误差累积）
> - **加速度计** 测量角度，长期稳定，但短期有振动噪声
>
> 互补滤波的思路是：**短期信任陀螺仪，长期信任加速度计**。
>
> ```
> 最终角度 = 0.98 × (陀螺仪积分角度) + 0.02 × (加速度计角度)
> ```
>
> 0.98 和 0.02 是"信任系数"，加起来等于 1。0.98 表示 98% 信任陀螺仪，2% 信任加速度计。

### 7.6 pid.c / pid.h —— PID 控制器

**文件位置：** `firmware_keil/Core/Src/pid.c` 和 `firmware_keil/Core/Inc/pid.h`

**PID 控制器是整辆小车的"灵魂"！** 它决定了小车能否站得稳。

#### 什么是 PID？（通俗理解）

想象你用手掌托着一根竖直的铅笔，让它保持不倒：

- **P（比例）**：铅笔往左倒，你就往右推，倒得越厉害，推得越用力。这是"反应"。
- **I（积分）**：如果铅笔总是往一个方向偏，你就持续加大相反方向的力，直到它回到中间。这是"纠偏"。
- **D（微分）**：如果铅笔倒的速度很快，你就提前用力推，提前阻止它倒下。这是"预判"。

#### PID 结构体

```c
typedef struct {
    float kp;                   // 比例系数
    float ki;                   // 积分系数
    float kd;                   // 微分系数

    float integral;             // 积分累计值
    float last_error;           // 上一次误差
    float derivative;           // 微分项（可外部赋值）

    float integral_limit;       // 积分限幅
    float output_limit;         // 输出限幅

    float output;               // 当前输出值
} PID_TypeDef;
```

#### 三环 PID 结构

本项目采用**串级 PID** 控制，包含三个 PID 环：

```
速度环（外环）：目标速度 → 倾角偏置
                      ↓
直立环（内环）：目标倾角 → PWM 控制量
                      ↓
转向环（叠加）：   差速修正
                      ↓
                 电机输出
```

**PID 默认参数：**

| 环 | Kp | Ki | Kd | 输出限幅 |
|:---|:---:|:---:|:---:|:---:|
| 直立环（Balance） | 150.0 | 0.8 | 3.5 | 800 |
| 速度环（Speed） | 40.0 | 0.2 | 0.0 | 200 |
| 转向环（Turn） | 65.0 | 0.0 | 0.0 | 300 |

> **⚠️ 注意：** 这些是初始参数，实际调试时可能需要根据你的小车进行调整。具体调试方法见第八章。

#### 关键函数说明

**`void PID_Init(PID_TypeDef *pid, float kp, float ki, float kd, float integral_limit, float output_limit)`**
- **作用：** 设置 PID 的各个参数

**`float PID_Calc(PID_TypeDef *pid, float error)`**
- **参数：** `error` 是当前误差（目标值 - 当前值）
- **返回值：** 控制输出值
- **作用：** 执行一次 PID 计算，输出控制量
- **公式：** `输出 = Kp × 误差 + Ki × 积分 + Kd × 微分`

**`void PID_CascadeControl(float target_speed, float current_pitch, float gyro_y, float left_speed, float right_speed)`**
- **作用：** 串级 PID 控制主函数，每 1ms 调用一次
- **执行流程：**
  1. **速度环：** 计算目标速度和实际速度的误差，输出"倾角偏置"
  2. **直立环：** 计算目标倾角和实际倾角的误差，输出"PWM 控制量"
  3. **转向环：** 计算左右轮速度差，输出"转向修正量"
  4. **合成输出：** 左电机 = 直立控制 - 转向控制，右电机 = 直立控制 + 转向控制

### 7.7 uart_protocol.c / uart_protocol.h —— 串口通信协议

**文件位置：** `firmware_keil/Core/Src/uart_protocol.c` 和 `firmware_keil/Core/Inc/uart_protocol.h`

#### 串口指令

**单字符指令（用串口调试助手发送）：**

| 指令 | 功能 |
|:---:|:---|
| **S** | 启动平衡模式（小车开始站立） |
| **T** | 停止/休眠（小车停止工作） |
| **P** | 打印当前数据（查看传感器数值） |
| **C** | 校准 MPU6050 零偏 |

**远程控制指令（通过蓝牙 App 发送）：**

| 指令格式 | 功能 |
|:---|:---|
| `S:0.5` | 设置速度，正数前进，负数后退 |
| `T:-0.3` | 设置转向，正数右转，负数左转 |
| `P` | 请求数据上报 |

**数据上报格式：**
```
A:1.23|S:0.05|V:7.4|B:1\r\n
```
- `A`: 当前倾角（度）
- `S`: 平均速度（m/s）
- `V`: 电池电压（V）
- `B`: 系统状态

#### 关键函数说明

**`void UART_SendString(const char *str)`** —— 发送字符串
- **作用：** 通过串口发送一段文本

**`void UART_ReportSensorData(void)`** —— 上报传感器数据
- **作用：** 把当前角度、速度、电压等信息打包发送给手机 App

**`void UART_RxCallback(uint8_t data)`** —— 接收中断回调
- **作用：** 当串口收到数据时，这个函数会被调用，判断是单字符指令还是远程控制指令

### 7.8 power_manager.c / power_manager.h —— 电源管理

**文件位置：** `firmware_keil/Core/Src/power_manager.c` 和 `firmware_keil/Core/Inc/power_manager.h`

#### 关键函数说明

**`float Power_ReadBatteryVoltage(void)`** —— 读取电池电压
- **返回值：** 电池电压值（V）
- **读取步骤：**
  1. 启动 ADC 转换
  2. 等待转换完成
  3. 读取 ADC 值（0~4095）
  4. 换算为电压：`电压 = ADC值 × 3.3 / 4096 × 分压比`

**`uint8_t Power_CheckBattery(void)`** —— 检查电池状态
- **返回值：** 0=正常，1=低电量，2=临界（需要立即停车）

**`uint8_t Power_CheckFall(float pitch)`** —— 摔倒检测
- **参数：** `pitch` 是当前倾角
- **返回值：** 0=正常，1=摔倒
- **检测逻辑：** 如果倾角超过 45 度且持续 2 秒以上，判定为摔倒

**`void Power_Process(void)`** —— 电源管理主处理
- **调用时机：** 在主循环中每 100ms 调用一次
- **作用：** 检查电池电量和摔倒状态，必要时控制小车进入安全状态

### 7.9 indicator.c / indicator.h —— 指示灯和蜂鸣器

**文件位置：** `firmware_keil/Core/Src/indicator.c` 和 `firmware_keil/Core/Inc/indicator.h`

#### 状态-颜色映射

| 系统状态 | LED 颜色 | 说明 |
|:---|:---:|:---|
| 初始化 | 🔵 蓝色常亮 | 正在初始化 |
| 启动中 | 🔵 蓝色常亮 | 等待用户发送 'S' 指令 |
| 平衡中 | 🟢 绿色常亮 | 正常工作 |
| 低电量 | 🟡 黄色闪烁 | 提醒充电 |
| 摔倒 | 🔴 红色常亮 | 检测到摔倒 |
| 休眠 | 熄灭 | 休眠模式 |
| 错误 | 🔴 红色闪烁 | 系统错误 |

#### 关键函数说明

**`void Indicator_SetColor(uint16_t color)`** —— 设置 RGB 颜色
- **参数：** 颜色组合，例如 `RGB_RED`、`RGB_GREEN`、`RGB_BLUE`、`RGB_YELLOW` 等

**`void Indicator_UpdateByState(SystemState_t state)`** —— 根据状态更新指示灯
- **作用：** 根据系统状态自动设置对应的颜色

**`void Indicator_Process(void)`** —— 指示灯主处理
- **调用时机：** 在主循环中不断调用
- **作用：** 处理闪烁逻辑（亮灭切换）

### 7.10 main.c —— 主程序

**文件位置：** `firmware_keil/Core/Src/main.c`

这是整个程序的"总指挥"，所有模块的初始化、主循环控制都在这里。

#### 程序启动流程

1. **HAL_Init()** —— 初始化 HAL 库
2. **SystemClock_Config()** —— 配置系统时钟为 72MHz
3. **MX_GPIO_Init()** —— 初始化 GPIO
4. **MX_I2C1_Init()** —— 初始化 I2C1
5. **MX_TIM2_Init()** —— 初始化 TIM2（左编码器 + PWM）
6. **MX_TIM3_Init()** —— 初始化 TIM3（右编码器）
7. **MX_USART1_UART_Init()** —— 初始化 USART1（蓝牙）
8. **MX_USART2_UART_Init()** —— 初始化 USART2（语音模块）
9. **MX_ADC1_Init()** —— 初始化 ADC1（电池检测）
10. **TIM1_Config()** —— 手动配置 TIM1（1kHz 控制定时器）
11. **模块初始化**：Indicator_Init()、Motor_Init()、Encoder_Init()、UART_Protocol_Init()、Power_Init()
12. **MPU6050_Init()** —— 初始化 MPU6050，如果失败则进入错误状态
13. **启动 USART1 中断接收**
14. **启动 TIM1 定时器**（开始 1ms 中断）

#### 主循环（while(1)）

主循环中执行以下任务，不断重复：

```c
while (1)
{
    // 1. 更新系统运行时间
    g_sys_tick_ms = HAL_GetTick();

    // 2. 电源管理 - 检查电池和摔倒（每100ms）
    Power_Process();

    // 3. 状态机 - 根据状态控制LED和电机
    System_StateMachine();

    // 4. 指示灯处理 - 闪烁逻辑
    Indicator_Process();

    // 5. 每100ms心跳检测
    // 6. 每500ms上报数据（蓝牙连接时）
}
```

#### 系统状态机

```c
static void System_StateMachine(void)
{
    switch (g_system_state)
    {
        case SYSTEM_INIT:      // 初始化中，不做任何操作
        case SYSTEM_STARTUP:   // 启动中，等待 'S' 指令
        case SYSTEM_BALANCING: // 平衡中，控制算法在中断中执行
        case SYSTEM_LOW_BAT:   // 低电量，停止电机
        case SYSTEM_FALLEN:    // 摔倒保护，停止电机
        case SYSTEM_SLEEP:     // 休眠模式，停止电机
        case SYSTEM_ERROR:     // 错误状态，停止电机
    }
}
```

#### 1kHz 中断服务函数

这是小车平衡的核心，每 1ms 执行一次：

```c
void TIM1_UP_IRQHandler(void)
{
    // 只有在平衡状态下才执行控制算法
    if (g_system_state == SYSTEM_BALANCING)
    {
        // 第1步：读取MPU6050所有数据
        MPU6050_ReadAll(&mpu_raw);

        // 第2步：换算为物理量
        MPU6050_ScaleData(&mpu_raw, &mpu_scaled);

        // 第3步：从加速度计计算倾斜角度
        float acc_pitch = MPU6050_CalcAccPitch(...);

        // 第4步：互补滤波融合
        g_pitch_angle = MPU6050_ComplementaryFilter(...);

        // 第5步：读取编码器速度
        g_left_speed  = Encoder_ReadSpeed(&g_encoder_left);
        g_right_speed = Encoder_ReadSpeed(&g_encoder_right);

        // 第6步：串级PID控制
        PID_CascadeControl(g_target_speed, g_pitch_angle, ...);
    }
}
```

> **💡 为什么控制算法放在中断里？** 因为控制算法必须每 1ms 精确执行一次，不能被其他事情打断。放在定时器中断中，可以确保时间的精确性。

#### 完整的 TIM2 初始化代码（混合模式）

由于 CubeMX 对 TIM2 混合模式的支持有限，这里提供完整的代码，你需要手动替换 CubeMX 生成的 `MX_TIM2_Init()` 函数：

```c
static void MX_TIM2_Init(void)
{
    TIM_Encoder_InitTypeDef sEncoderConfig = {0};
    TIM_OC_InitTypeDef sConfigOC = {0};
    GPIO_InitTypeDef GPIO_InitStruct = {0};

    // ====== 编码器模式配置 (CH1/CH2 on PA0/PA1) ======
    htim2.Instance = TIM2;
    htim2.Init.Prescaler = 0;
    htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim2.Init.Period = 0xFFFF;
    htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    htim2.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;

    sEncoderConfig.EncoderMode = TIM_ENCODERMODE_TI12;
    sEncoderConfig.IC1Polarity = TIM_ICPOLARITY_RISING;
    sEncoderConfig.IC1Selection = TIM_ICSELECTION_DIRECTTI;
    sEncoderConfig.IC1Prescaler = TIM_ICPSC_DIV1;
    sEncoderConfig.IC1Filter = 0;
    sEncoderConfig.IC2Polarity = TIM_ICPOLARITY_RISING;
    sEncoderConfig.IC2Selection = TIM_ICSELECTION_DIRECTTI;
    sEncoderConfig.IC2Prescaler = TIM_ICPSC_DIV1;
    sEncoderConfig.IC2Filter = 0;

    if (HAL_TIM_Encoder_Init(&htim2, &sEncoderConfig) != HAL_OK)
        Error_Handler();

    HAL_TIM_Encoder_Start(&htim2, TIM_CHANNEL_ALL);

    // ====== PWM 输出配置 (CH3/CH4 on PA2/PA3) ======
    // 配置 PA2, PA3 为复用推挽输出
    __HAL_RCC_GPIOA_CLK_ENABLE();
    GPIO_InitStruct.Pin = GPIO_PIN_2 | GPIO_PIN_3;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

    // 配置 PWM 通道参数
    sConfigOC.OCMode = TIM_OCMODE_PWM1;
    sConfigOC.Pulse = 0;
    sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
    sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;

    if (HAL_TIM_PWM_ConfigChannel(&htim2, &sConfigOC, TIM_CHANNEL_3) != HAL_OK)
        Error_Handler();
    if (HAL_TIM_PWM_ConfigChannel(&htim2, &sConfigOC, TIM_CHANNEL_4) != HAL_OK)
        Error_Handler();

    // 启动PWM输出
    HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_3);
    HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_4);
}
```

#### 完整的 TIM3 初始化代码（含重映射）

```c
static void MX_TIM3_Init(void)
{
    TIM_Encoder_InitTypeDef sEncoderConfig = {0};

    // 使能 AFIO 时钟并配置 TIM3 部分重映射 (PB4=CH1, PB5=CH2)
    __HAL_RCC_AFIO_CLK_ENABLE();
    __HAL_AFIO_REMAP_TIM3_PARTIAL();

    htim3.Instance = TIM3;
    htim3.Init.Prescaler = 0;
    htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim3.Init.Period = 0xFFFF;
    htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    htim3.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;

    sEncoderConfig.EncoderMode = TIM_ENCODERMODE_TI12;
    sEncoderConfig.IC1Polarity = TIM_ICPOLARITY_RISING;
    sEncoderConfig.IC1Selection = TIM_ICSELECTION_DIRECTTI;
    sEncoderConfig.IC1Prescaler = TIM_ICPSC_DIV1;
    sEncoderConfig.IC1Filter = 0;
    sEncoderConfig.IC2Polarity = TIM_ICPOLARITY_RISING;
    sEncoderConfig.IC2Selection = TIM_ICSELECTION_DIRECTTI;
    sEncoderConfig.IC2Prescaler = TIM_ICPSC_DIV1;
    sEncoderConfig.IC2Filter = 0;

    if (HAL_TIM_Encoder_Init(&htim3, &sEncoderConfig) != HAL_OK)
        Error_Handler();

    HAL_TIM_Encoder_Start(&htim3, TIM_CHANNEL_ALL);
}
```

#### 完整的 TIM1 配置代码（1kHz 控制定时器）

```c
static void TIM1_Config(void)
{
    TIM_ClockConfigTypeDef sClockSourceConfig = {0};
    TIM_MasterConfigTypeDef sMasterConfig = {0};

    htim1.Instance = TIM1;
    htim1.Init.Prescaler = 72 - 1;      // 72MHz / 72 = 1MHz
    htim1.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim1.Init.Period = 1000 - 1;        // 1MHz / 1000 = 1kHz
    htim1.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    htim1.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;

    if (HAL_TIM_Base_Init(&htim1) != HAL_OK)
        Error_Handler();

    sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
    HAL_TIM_ConfigClockSource(&htim1, &sClockSourceConfig);

    sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
    sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
    HAL_TIMEx_MasterConfigSynchronization(&htim1, &sMasterConfig);
}
```

---

## 第八章 编译烧录与调试

代码写好了，现在要把它"烧录"到 STM32 芯片中，让小车活起来！

### 8.1 在 Keil5 中打开项目

1. 打开 Keil uVision5
2. 点击菜单栏的 **Project → Open Project**
3. 找到 CubeMX 生成的项目文件夹，打开 `balancer_car.uvprojx` 文件
4. 项目加载完成后，左侧的 **Project** 窗口中会显示所有文件

### 8.2 添加用户代码文件

如果 CubeMX 生成项目时没有包含我们手动创建的文件，需要手动添加：

1. 在左侧 **Project** 窗口中，右键点击 **Source Group**（如 `Application/User`）
2. 选择 **Add Existing Files to Group...**
3. 找到 `motor.c`、`encoder.c`、`mpu6050.c`、`pid.c`、`uart_protocol.c`、`power_manager.c`、`indicator.c` 文件，选中并添加
4. 同样方法，在 **Header Files** 组中添加对应的 .h 文件

### 8.3 编译项目

1. 点击工具栏上的 **Build** 按钮（或者按键盘上的 **F7** 键）
2. 观察下方的 **Build Output** 窗口，看编译过程
3. 如果编译成功，你会看到：
   ```
   Build started: Project: balancer_car
   *** Using Compiler 'V5.06 update 7', folder: ...
   ...
   linking...
   Program Size: Code=XXXX RO-data=XXXX RW-data=XXXX ZI-data=XXXX
   Build Time Elapsed: XX:XX:XX
   ```
   **最重要的是看到 "0 Error(s), 0 Warning(s)"**（0 个错误，0 个警告）

> **⚠️ 警告：** 如果编译有错误，仔细阅读错误信息，它通常会告诉你出错的文件和行号。常见的错误有：
> - 忘记添加文件到项目中
> - 头文件路径没有配置
> - 函数名拼写错误

### 8.4 设置 Debug 选项

1. 点击工具栏上的 **Options for Target** 按钮（或者按 **Alt+F7**）
2. 在弹出的窗口中，点击 **Debug** 标签页
3. 在右上角的 **Use** 选项中，选择 **ST-Link Debugger**
4. 点击右侧的 **Settings** 按钮
5. 在弹出的窗口中，确认 **Debug** 标签页中的 **Port** 选择为 **SW**（串行线调试）
6. 切换到 **Flash Download** 标签页
7. 勾选 **Reset and Run**（下载后自动运行）
8. 在 **Programming Algorithm** 中，确保有以下算法（如果没有，点击 **Add** 添加）：
   - **STM32F10x Med-density Flash**（128KB Flash）

> **💡 Reset and Run 是什么？** 勾选这个选项后，程序烧录完成后会自动复位并运行，省去了你手动按复位键的步骤。

### 8.5 烧录程序

1. 将 ST-Link 下载器连接到电脑
2. 将 ST-Link 的 SWD 接口连接到 STM32 最小系统板：
   - ST-Link SWDIO → STM32 SWDIO（PA13）
   - ST-Link SWCLK → STM32 SWCLK（PA14）
   - ST-Link GND → STM32 GND
   - ST-Link 3.3V → STM32 3.3V
3. 点击工具栏上的 **Download** 按钮（或者按 **F8**）
4. 观察下方的 **Build Output** 窗口，会显示烧录过程
5. 如果烧录成功，会看到：
   ```
   Erase Done.
   Programming Done.
   Verify OK.
   Application running...
   ```

> **✅ 恭喜！** 程序已经成功烧录到 STM32 中了！

### 8.6 串口调试

1. 将 CH340 USB 转串口模块连接到电脑
2. 连接 CH340 到 STM32：
   - CH340 TXD → STM32 PA10（USART1_RX）
   - CH340 RXD → STM32 PA9（USART1_TX）
   - CH340 GND → STM32 GND
3. 打开串口调试助手软件（如 SSCOM、Putty 等）
4. 设置串口参数：
   - 波特率：**115200**
   - 数据位：**8**
   - 校验位：**None**
   - 停止位：**1**
   - 打开串口
5. 给 STM32 上电，你应该会看到：
   ```
   System init OK!
   Send 'S' to start balancing.
   ```
6. 在串口助手中发送 **S**（大写），小车应该开始尝试平衡
7. 发送 **P** 可以查看当前数据：
   ```
   A:1.23|S:0.05|V:7.4|B:2
   ```

### 8.7 PID 参数调试方法

**PID 调参是自平衡小车最关键的步骤，也是最需要耐心的步骤。**

#### 调试步骤

**第一步：调直立环（P 和 D）**

1. 将小车拿在手里，悬空（不要接触地面）
2. 只设置直立环的 P 参数（Kp），从较小的值开始（如 50）
3. 发送 'S' 启动平衡
4. 用手轻轻倾斜小车，感受电机的反应：
   - 如果电机没有反应 → P 太小，增加
   - 如果电机剧烈抖动 → P 太大，减小
5. 找到合适的 P 值后，加入 D 参数（Kd）：
   - D 参数可以抑制抖动
   - 逐渐增加 D，直到小车响应迅速但不抖动

**第二步：调试直立环的 I**

1. 如果小车总是往一个方向倾斜，需要加入 I 参数
2. 从较小的值开始（如 0.1），逐渐增加
3. I 太大会引起低频振荡（小车来回摆动）

**第三步：调试速度环**

1. 直立环调好后，小车应该能短暂站立
2. 加入速度环的 P 参数，让小车能稳定站立
3. 速度环的 I 参数用于消除稳态误差

**调试口诀：**
> 先调直立后调速，P 大震荡 D 消震，
> I 小纠偏 I 大摆，耐心调试不灰心。

> **💡 调参技巧：**
> - 每次只改变一个参数，记录变化效果
> - 参数的微小变化（如 0.1 的差异）就可能产生明显效果
> - 建议使用串口助手，实时观察角度数据变化
> - 如果小车完全失控，检查编码器接线是否正确

---

## 第九章 蓝牙远程控制

### 9.1 HC-05 接线

HC-05 蓝牙模块的接线非常简单：

| HC-05 引脚 | 连接到 |
|:---:|:---|
| VCC | STM32 3.3V |
| GND | STM32 GND |
| TXD | STM32 PA10 (USART1_RX) |
| RXD | STM32 PA9 (USART1_TX) |

> **⚠️ 注意：** HC-05 的 RXD 接 STM32 的 TX（PA9），HC-05 的 TXD 接 STM32 的 RX（PA10）。这是"交叉连接"，就像两个人面对面说话，一个人的"嘴巴"对着另一个人的"耳朵"。

> **💡 提示：** 有些 HC-05 模块的 VCC 需要接 5V 才能正常工作，但 STM32 的串口是 3.3V 电平的。如果模块工作不稳定，可以在 VCC 接 5V（通过 USB 或电池），但 TX/RX 之间可能需要电平转换。

### 9.2 手机 APP 控制

1. 在手机应用商店搜索"蓝牙串口"或"Bluetooth Serial"，下载任意一款蓝牙串口 APP
2. 打开 APP，搜索蓝牙设备
3. 找到名为 **HC-05** 或 **HC-06** 的设备，点击连接
4. 默认密码：**1234** 或 **0000**
5. 连接成功后，APP 上会显示"已连接"
6. 在 APP 的发送框中输入指令：
   - 输入 `S` 发送，启动平衡模式
   - 输入 `S:0.5` 发送，小车前进
   - 输入 `S:-0.3` 发送，小车后退
   - 输入 `T:0.2` 发送，小车右转
   - 输入 `T:-0.2` 发送，小车左转
   - 输入 `P` 发送，查看当前数据

### 9.3 蓝牙指令格式

| 指令 | 格式 | 示例 | 说明 |
|:---|:---|:---|:---|
| 启动平衡 | `S` | `S` | 单字符，无冒号 |
| 设置速度 | `S:数值` | `S:0.5` | 正数前进，负数后退，范围 -1.0~1.0 |
| 设置转向 | `T:数值` | `T:-0.3` | 正数右转，负数左转，范围 -1.0~1.0 |
| 请求数据 | `P` | `P` | 单字符，无冒号 |

> **💡 注意：** 蓝牙指令中的 S 和串口指令中的 S 功能不同。
> - 串口指令 `S`（单字符）= 启动平衡模式
> - 蓝牙指令 `S:0.5`（带冒号）= 设置速度

---

## 第十章 后续升级

恭喜你！你已经成功制作了一辆自平衡小车！如果你想让它更厉害，可以从以下几个方面进行升级。

### 10.1 传感器升级

| 升级项 | 说明 | 效果 |
|:---|:---|:---|
| 更换更高精度的编码器 | 替换 N20 电机的编码器为更高线数（如 500 线/1000 线） | 速度测量更精确，控制更稳定 |
| 增加超声波传感器 | 在车头增加 HC-SR04 超声波模块 | 实现避障功能 |
| 增加红外传感器 | 在车底安装红外传感器 | 实现循迹功能（沿黑线行驶） |
| 更换 MPU6050 为 ICM-20948 | 更新的 9 轴传感器芯片 | 角度测量更准确，支持磁力计 |

### 10.2 算法优化方向

| 优化项 | 说明 |
|:---|:---|
| 卡尔曼滤波 | 替代互补滤波，角度解算更精确（但计算量更大） |
| 自适应 PID | 根据小车状态自动调整 PID 参数 |
| 模糊控制 | 使用模糊逻辑替代 PID，对复杂路况适应性更好 |
| 机器学习 | 使用强化学习训练小车自主平衡 |

### 10.3 无线控制升级

| 升级项 | 说明 |
|:---|:---|
| WiFi 控制（ESP8266/ESP32） | 通过 WiFi 连接手机或电脑，控制距离更远 |
| 4G 控制 | 使用 4G 模块，实现远程控制（不受距离限制） |
| 无线手柄控制 | 使用 NRF24L01 无线模块，配合手柄控制 |
| 摄像头图传 | 增加摄像头模块，实现第一人称视角控制 |

---

## 附录

### 附录A：引脚图（ASCII 艺术风格）

```
STM32F103C8T6 (LQFP48) 引脚图

                         ┌─────────────────────┐
                   VBAT ─┤1                 48◄─┼─ VSS
                   PC13 ─┤2                 47◄─┼─ VDD
                   PC14 ─┤3                 46◄─┼─ PA0  ← 左编码器A相 (TIM2_CH1)
                   PC15 ─┤4                 45◄─┼─ PA1  ← 左编码器B相 (TIM2_CH2)
                   RST  ─┤5                 44◄─┼─ PA2  → 左电机PWM (TIM2_CH3)
                   VSSA ─┤6                 43◄─┼─ PA3  → 右电机PWM (TIM2_CH4)
                   VDDA ─┤7                 42◄─┼─ PA4  → 电池检测 (ADC1_IN4)
              PA5(SPI1_SCK) ─┤8            41◄─┼─ PA5  (未使用)
              PA6(SPI1_MISO) ─┤9           40◄─┼─ PA6  (未使用)
              PA7(SPI1_MOSI) ─┤10          39◄─┼─ PA7  (未使用)
              PB0  → 左电机方向1 ─┤11      38◄─┼─ PB5  ← 右编码器B相 (TIM3_CH2)
              PB1  → 左电机方向2 ─┤12      37◄─┼─ PB4  ← 右编码器A相 (TIM3_CH1)
             PB2(BOOT1) ─┤13              36◄─┼─ PB3  → 蜂鸣器
            PB10 → 语音TX(USART2_TX) ─┤14 35◄─┼─ PA15 (未使用，SWDIO占用)
            PB11 → 语音RX(USART2_RX) ─┤15 34◄─┼─ PA12 (未使用)
            PB12 → 右电机方向1 ─┤16      33◄─┼─ PA11 (未使用)
            PB13 → 右电机方向2 ─┤17      32◄─┼─ PA10 ← 蓝牙RX (USART1_RX)
            PB14 → RGB LED 红 ─┤18       31◄─┼─ PA9  → 蓝牙TX (USART1_TX)
            PB15 → RGB LED 绿 ─┤19       30◄─┼─ PA8  (未使用)
             PB8  → RGB LED 蓝 ─┤20      29◄─┼─ PB15
             PB9  (未使用) ─┤21           28◄─┼─ PB14
                   VDD ─┤22              27◄─┼─ VSS
                   VSS ─┤23              26◄─┼─ VDD
              PB6  → MPU6050 SCL ─┤24    25◄─┼─ PB7  → MPU6050 SDA
                         └─────────────────────┘
```

> **💡 如何看这个图？** 芯片是"俯视图"，从芯片正上方往下看。引脚 1 在左上角，按逆时针方向编号。左上角有一个小圆点或缺口，标记了引脚 1 的位置。

### 附录B：常见问题排查

| 问题 | 可能原因 | 解决方法 |
|:---|:---|:---|
| 烧录时提示 "No ST-Link detected" | ST-Link 没连接好或驱动没装 | 检查 USB 连接，重新安装驱动 |
| 烧录时提示 "Flash Download failed" | Flash 下载算法没选对 | 在 Debug 设置中添加 STM32F10x Med-density Flash |
| 编译时提示 "Undefined symbol" | 文件没添加到项目或头文件路径不对 | 检查文件是否添加到项目中，检查头文件路径 |
| 上电后 MPU6050 初始化失败 | 接线错误或 MPU6050 损坏 | 检查 I2C 接线（PB6/PB7），检查 MPU6050 供电 |
| 电机不转 | PWM 引脚接错或电机驱动没供电 | 确认 PA2/PA3 是否正确连接，检查 TB6612 供电 |
| 小车剧烈抖动 | PID 参数不合适 | 减小 P 参数，增加 D 参数 |
| 小车总是往一个方向倒 | 编码器接线反了或 MPU6050 安装方向不对 | 交换编码器 A/B 相，检查 MPU6050 方向 |
| 蓝牙连接不上 | 波特率不匹配或引脚接错 | 确认蓝牙波特率是 115200，检查 TX/RX 是否交叉连接 |
| 电池电压检测不准 | 分压电阻阻值不对 | 检查分压电路，修改 `VOLTAGE_DIVIDER_RATIO` 的值 |
| LED 不亮 | 引脚接错或 LED 损坏 | 检查 PB8/PB14/PB15 接线，确认 LED 是共阴极 |

### 附录C：参考资料

| 资料名称 | 说明 |
|:---|:---|
| STM32F103C8T6 数据手册 | ST 官方芯片手册，包含所有技术参数 |
| STM32F1xx HAL 库手册 | ST 官方 HAL 库函数参考 |
| MPU6050 数据手册 | InvenSense 官方传感器手册 |
| TB6612FNG 数据手册 | Toshiba 官方电机驱动芯片手册 |
| HC-05 蓝牙模块 AT 指令集 | 蓝牙模块配置命令参考 |
| 正点原子/野火 STM32 教程 | 中文 STM32 入门教程，讲解详细 |

---

> **最后的话**
>
> 做自平衡小车是一个很有挑战但也很有成就感的过程。你可能会遇到各种问题，但请不要灰心——每一个问题都是一个学习的机会。
>
> 记住：**调试是一个系统性的过程，一次只改变一个变量，观察效果，再做下一次调整。**
>
> 祝你成功！🎉

---

*本指南根据 `firmware_keil/Core/Inc/` 和 `firmware_keil/Core/Src/` 中的实际代码编写，确保所有代码示例与项目代码一致。*