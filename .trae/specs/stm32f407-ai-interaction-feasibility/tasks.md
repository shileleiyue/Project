# Tasks

本任务清单为硬件可行性评估的验证步骤，不涉及代码实现。

- [x] Task 1: 核对 STM32F407ZGT6 核心参数
  - [x] 确认 MCU 型号、内核、主频、Flash、SRAM 规格
  - [x] 确认探索者底板外设清单（外部 SRAM、Flash、以太网 PHY、LCD、触摸、音频 Codec、SD 卡槽）

- [x] Task 2: 评估联网能力
  - [x] 评估板载 LAN8720A 以太网方案可行性及 LWIP 协议栈适配
  - [x] 评估外接 ESP32/ESP8266 WiFi 模块方案可行性
  - [x] 评估 HTTPS/TLS 在 STM32F4 上的资源开销与瓶颈

- [x] Task 3: 评估 AI 服务交互能力
  - [x] 评估 HTTP 请求调用云端 AI API 的可行性
  - [x] 评估 JSON 响应解析的内存需求
  - [x] 评估流式响应（SSE）的可行性

- [x] Task 4: 评估人机交互能力
  - [x] 评估 4.3 寸 LCD 显示中文文本的可行性
  - [x] 评估触摸屏文字输入的体验
  - [x] 评估 WM8978 语音输入（录音→云端 ASR）的可行性
  - [x] 评估 WM8978 语音输出（云端 TTS→播放）的可行性

- [x] Task 5: 输出整体评估结论
  - [x] 给出可行方案 A（ESP32 WiFi + 云端 AI）
  - [x] 给出可行方案 B（以太网 + HTTP 代理）
  - [x] 明确标注不可行方案（本地 AI 推理）
  - [x] 汇总各维度结论表

# Task Dependencies
- Task 2, 3, 4 可并行执行
- Task 5 依赖 Task 1-4 全部完成