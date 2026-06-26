# Checklist

- [x] spec.md 中 STM32F407ZGT6 核心参数（内核、主频、Flash、SRAM、FPU）准确无误
- [x] spec.md 中探索者底板外设清单完整（外部 SRAM、Flash、以太网、LCD、触摸、音频、SD、USB）
- [x] 联网能力评估覆盖了以太网和 WiFi 两种方案，且标注了各自的瓶颈
- [x] HTTPS/TLS 资源瓶颈有具体数据说明（mbedTLS ~64KB RAM）
- [x] AI 服务交互评估覆盖了 HTTP API 调用、JSON 解析、流式响应三种场景
- [x] 人机交互评估覆盖了文本显示、触摸输入、语音输入、语音输出四种场景
- [x] 给出了至少一个可行方案和至少一个不可行方案
- [x] 最终结论包含各维度汇总表，结论明确
- [x] tasks.md 中的任务覆盖了所有评估维度
- [x] 任务依赖关系标注正确