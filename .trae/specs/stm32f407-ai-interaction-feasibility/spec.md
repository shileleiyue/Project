# STM32F407ZGT6 探索者 联网AI互动 可行性评估 Spec

## Why
用户拥有一块正点原子探索者 STM32F407ZGT6 开发板（带 4.3 寸 LCD 触摸屏），希望评估该硬件平台能否胜任"联网AI互动"任务（即通过网络连接云端 AI 服务，在本地进行交互式对话、问答等场景）。

## What Changes
- 本规格为**硬件可行性评估**，不涉及代码实现。
- 对 STM32F407ZGT6 + 探索者底板各外设模块进行能力边界分析。
- 评估"联网AI互动"场景下的关键子任务及其可行性。
- 给出可行的最小系统架构方案和不可行的替代方案。
- 输出结论：是否能做、能做什么、不能做什么、需要额外哪些硬件。

## Impact
- Affected specs: 无（全新评估）
- Affected code: 无（本规格仅输出评估结论，不产生代码）

---

## 硬件平台基线

### MCU: STM32F407ZGT6
| 参数 | 值 | 对AI互动的影响 |
|------|-----|---------------|
| 内核 | ARM Cortex-M4F @ 168MHz | 无 NPU/向量加速，**不能本地跑 AI 模型** |
| Flash | 1MB | 固件存储充足 |
| SRAM | 192KB (128KB + 64KB CCM) | **极紧缺**，HTTP 响应 buffer、JSON 解析、LCD 显存都争抢这 192KB |
| FPU | 单精度硬件浮点 | 对轻量信号处理有帮助，对 AI 推理无实质帮助 |

### 探索者底板外设
| 外设 | 芯片/规格 | 对AI互动的作用 |
|------|-----------|---------------|
| 外部 SRAM | IS62WV51216 1MB | 缓解 SRAM 压力，可存放网络 buffer 和 JSON |
| 外部 Flash | W25Q128 16MB | 可存字库、历史记录、离线缓存 |
| 以太网 PHY | LAN8720A (RMII) | **有线网络**，可跑 LWIP |
| LCD | 4.3 寸 TFT (480×800) | **显示 AI 回复文本** |
| 触摸屏 | 电容触摸 (FT5206/I2C) | 用户输入交互 |
| 音频 Codec | WM8978 (I2S) | 可录音/播放，支持语音交互 |
| SD 卡槽 | SDIO | 可存大量历史对话 |
| USB OTG | FS | 可接 WiFi 网卡（需驱动）或键盘 |

---

## ADDED Requirements

### Requirement: 联网能力评估
系统 SHALL 评估 STM32F407ZGT6 探索者实现网络通信的可行方案及瓶颈。

#### Scenario: 以太网有线连接
- **WHEN** 使用板载 LAN8720A + LWIP 协议栈
- **THEN** 可实现 TCP/UDP 通信，HTTP 请求可行。**HTTPS/TLS 极难**（mbedTLS 需要 ~64KB RAM 仅 TLS 握手，与 HTTP buffer 和 JSON 解析内存争抢严重）。

#### Scenario: WiFi 无线连接
- **WHEN** 通过 SPI/USART 外接 ESP8266 或 ESP32 模块
- **THEN** ESP8266/ESP32 自带 TCP/IP 协议栈，AT 指令方式即可发起 HTTP 请求，**比以太网方案更简单**。ESP32 还可分担 TLS 握手。

### Requirement: AI 服务交互评估
系统 SHALL 评估调用云端 AI API（如 OpenAI/文心一言/通义千问等）的可行性。

#### Scenario: HTTP API 调用
- **WHEN** 通过 HTTP 向云端 AI 服务发送请求
- **THEN** 可行。但需注意：多数 AI API 强制 HTTPS，需中间代理或 ESP32 做 TLS 卸载。

#### Scenario: JSON 响应解析
- **WHEN** 接收到 AI API 的 JSON 响应（通常 1-10KB）
- **THEN** 使用 cJSON 或 JSMN 等轻量解析库可行。但需确保 SRAM 有足够 buffer（建议利用外部 1MB SRAM）。

#### Scenario: 流式响应（SSE/Streaming）
- **WHEN** AI 服务返回流式 chunk 数据
- **THEN** **极难**。STM32F4 处理 HTTP 分块传输+实时解析+LCD 刷新，RAM 和 CPU 都紧张，建议只使用非流式完整响应。

### Requirement: 人机交互评估
系统 SHALL 评估板载 4.3 寸 LCD 触摸屏和音频 Codec 是否满足交互需求。

#### Scenario: 文本显示
- **WHEN** 在 4.3 寸 LCD 上显示 AI 回复文本
- **THEN** 可行。480×800 分辨率足够显示中文对话，需字库支持（存储于外部 Flash 或 SD 卡）。

#### Scenario: 触摸输入
- **WHEN** 用户通过触摸屏输入文字
- **THEN** 可行但体验差。4.3 寸屏上实现全键盘输入体验不如手机。建议：预设快捷问题按钮 / 语音输入 / 外接 USB 键盘。

#### Scenario: 语音输入
- **WHEN** 通过 WM8978 录制音频并发送到云端语音识别 API
- **THEN** 可行。WM8978 支持 8-48kHz 采样，PCM 音频流可通过 HTTP 上传到 ASR 服务。但需要处理音频 buffer（建议用外部 SRAM）。

#### Scenario: 语音合成播放
- **WHEN** 从云端 TTS 获取音频并播放
- **THEN** 可行。下载 MP3/WAV 通过 WM8978 播放，或直接使用 PCM 流。需注意音频解码的 CPU 开销。

### Requirement: 整体架构评估
系统 SHALL 给出可行的最小系统架构方案。

#### Scenario: 可行方案 A - ESP32 WiFi + 云端 AI + LCD 文本交互
- **WHEN** 采用 ESP32 作为 WiFi 和 TLS 代理模块
- **THEN** 架构为：LCD 触摸屏 ↔ STM32F407 ↔ ESP32(AT指令) ↔ WiFi ↔ 云端 AI API。可完成文本对话式 AI 互动。**这是最推荐的可行方案。**

#### Scenario: 可行方案 B - 以太网 + HTTP 代理 + LCD 文本交互
- **WHEN** 使用板载 LAN8720A 以太网 + 自建 HTTP→HTTPS 代理服务
- **THEN** 架构为：LCD 触摸屏 ↔ STM32F407 ↔ 以太网 ↔ 代理服务器(HTTP→HTTPS) ↔ 云端 AI API。需要额外部署一台代理服务器（如树莓派/PC）。

#### Scenario: 不可行方案 - 本地运行 AI 模型
- **WHEN** 尝试在 STM32F407 上本地运行 LLM 或神经网络模型
- **THEN** 完全不可行。168MHz Cortex-M4 无 NPU，192KB SRAM，无法运行任何有意义的对话 AI 模型。

---

## 结论

| 维度 | 结论 | 说明 |
|------|------|------|
| 本地AI推理 | **不可行** | 无 NPU，算力/内存完全不够 |
| 联网文本对话 | **可行** | 需 ESP32 做 WiFi+TLS 或用以太网+代理 |
| 语音输入 | **可行** | 需 WM8978 录音+云端 ASR，有开发量 |
| 语音输出 | **可行** | 需 WM8978 播放+云端 TTS，有开发量 |
| 流式对话 | **困难** | RAM 和 CPU 紧张，不建议 |
| 多轮对话记忆 | **受限** | 外部 Flash/SD 可存历史，但 RAM 限制上下文长度 |

**最终结论：STM32F407ZGT6 探索者可以胜任"云端AI瘦客户端"角色，实现文本/语音的联网AI互动，但需要外接 WiFi 模块（推荐 ESP32），且响应速度和交互体验远不如手机/PC。适合作为学习项目或概念验证，不适合作为产品。**