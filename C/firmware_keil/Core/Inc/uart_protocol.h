#ifndef __UART_PROTOCOL_H
#define __UART_PROTOCOL_H

#include "main.h"

/* ======================== 串口参数 ======================== */

#define UART_BAUDRATE           115200
#define UART_RX_BUF_SIZE        64
#define UART_TX_BUF_SIZE        128

/* ======================== 指令定义 ======================== */

// 单字符指令（调试用）
#define CMD_START       'S'     // 启动平衡模式
#define CMD_STOP        'T'     // 停止/休眠
#define CMD_PRINT       'P'     // 打印当前数据
#define CMD_CALIBRATE   'C'     // 校准MPU6050零偏

// 远程控制指令（蓝牙App用）
// 格式: "S:speed" 设置速度, 如 "S:0.5"
// 格式: "T:turn"  设置转向, 如 "T:-0.3"
// 格式: "P"       请求数据上报

/* ======================== 数据结构 ======================== */

typedef struct {
    uint8_t rx_buffer[UART_RX_BUF_SIZE];    // 接收缓冲区
    uint8_t rx_index;                        // 接收索引
    uint8_t rx_complete;                     // 接收完成标志

    uint8_t tx_buffer[UART_TX_BUF_SIZE];     // 发送缓冲区
    uint16_t tx_len;                         // 发送长度
} UART_Handle_t;

/* ======================== 函数声明 ======================== */

// 初始化串口协议
void UART_Protocol_Init(void);

// 处理单字符指令（从串口调试助手接收）
void UART_ProcessCharCmd(uint8_t cmd);

// 解析远程控制指令（从蓝牙App接收）
void UART_ParseRemoteCmd(char *cmd_str);

// 上报传感器数据给手机App
void UART_ReportSensorData(void);

// 发送字符串
void UART_SendString(const char *str);

// 发送格式化字符串
void UART_SendFormat(const char *fmt, ...);

// 发送数据帧（带校验）
// 格式: 0xAA 0x55 len data[0..len-1] checksum
void UART_SendFrame(uint8_t *data, uint8_t len);

// 串口接收中断回调（在HAL_UART_RxCpltCallback中调用）
void UART_RxCallback(uint8_t data);

// 心跳检测（每100ms在主循环中调用）
void UART_HeartbeatCheck(void);

#endif /* __UART_PROTOCOL_H */