/**
 * @file    uart_protocol.c
 * @brief   串口通信协议实现
 * @note    支持单字符指令（调试助手）和远程控制指令（蓝牙App）
 *          波特率: 115200, 8N1
 *          数据上报格式: A:倾角|S:速度|V:电压|B:状态\r\n
 */

#include "uart_protocol.h"
#include <stdarg.h>
#include <stdlib.h>

static UART_Handle_t uart_handle;

/* ======================== 外部变量引用 ======================== */

extern float g_pitch_angle;
extern float g_left_speed;
extern float g_right_speed;
extern float g_battery_voltage;
extern SystemState_t g_system_state;

/* ======================== 函数实现 ======================== */

/**
 * @brief 初始化串口协议
 */
void UART_Protocol_Init(void)
{
    uart_handle.rx_index = 0;
    uart_handle.rx_complete = 0;
    uart_handle.tx_len = 0;
    memset(uart_handle.rx_buffer, 0, UART_RX_BUF_SIZE);
    memset(uart_handle.tx_buffer, 0, UART_TX_BUF_SIZE);
}

/**
 * @brief 处理单字符指令（从串口调试助手接收）
 * @param cmd 指令字符
 * 
 * 支持指令:
 *   'S' - 启动平衡模式
 *   'T' - 停止/休眠
 *   'P' - 打印当前数据
 *   'C' - 校准MPU6050零偏
 */
void UART_ProcessCharCmd(uint8_t cmd)
{
    switch (cmd)
    {
        case CMD_START:  // 'S'
            if (g_system_state == SYSTEM_STARTUP || g_system_state == SYSTEM_SLEEP)
            {
                g_system_state = SYSTEM_BALANCING;
                UART_SendString("Balancing started.\r\n");
            }
            else
            {
                UART_SendString("Already balancing.\r\n");
            }
            break;

        case CMD_STOP:  // 'T'
            g_system_state = SYSTEM_SLEEP;
            UART_SendString("System sleep.\r\n");
            break;

        case CMD_PRINT:  // 'P'
            UART_ReportSensorData();
            break;

        case CMD_CALIBRATE:  // 'C'
            UART_SendString("Calibrating...\r\n");
            // 校准逻辑：需要读取MPU6050零偏值
            // 这里只是示例，实际需要在mpu6050.c中实现
            UART_SendString("Calibration done.\r\n");
            break;

        default:
            // 未知指令，忽略
            break;
    }
}

/**
 * @brief 解析远程控制指令（从蓝牙App接收）
 * @param cmd_str 指令字符串
 * 
 * 支持的格式:
 *   "S:speed" - 设置速度, 如 "S:0.5" (正数前进, 负数后退)
 *   "T:turn"  - 设置转向, 如 "T:-0.3" (正数左转, 负数右转)
 *   "P"       - 请求数据上报
 */
void UART_ParseRemoteCmd(char *cmd_str)
{
    extern float g_target_speed;
    extern float g_target_turn;

    if (cmd_str[0] == 'S' && cmd_str[1] == ':')
    {
        // 解析速度指令，如 "S:0.5"
        float speed = atof(&cmd_str[2]);
        // 限幅在 -1.0 ~ 1.0
        if (speed > 1.0f) speed = 1.0f;
        if (speed < -1.0f) speed = -1.0f;
        g_target_speed = speed;
    }
    else if (cmd_str[0] == 'T' && cmd_str[1] == ':')
    {
        // 解析转向指令，如 "T:-0.3"
        float turn = atof(&cmd_str[2]);
        if (turn > 1.0f) turn = 1.0f;
        if (turn < -1.0f) turn = -1.0f;
        g_target_turn = turn;
    }
    else if (cmd_str[0] == 'P')
    {
        // 请求数据上报，立即发送当前状态
        UART_ReportSensorData();
    }
}

/**
 * @brief 上报传感器数据给手机App
 * @note 格式: A:倾角|S:速度|V:电压|B:状态\r\n
 *       示例: A:1.23|S:0.05|V:7.4|B:1\r\n
 */
void UART_ReportSensorData(void)
{
    char buf[64];
    sprintf(buf, "A:%.2f|S:%.2f|V:%.1f|B:%d\r\n",
            g_pitch_angle,                    // 当前倾角
            (g_left_speed + g_right_speed) / 2.0f,  // 平均速度
            g_battery_voltage,                // 电池电压
            (int)g_system_state);             // 系统状态
    UART_SendString(buf);
}

/**
 * @brief 发送字符串
 * @param str 要发送的字符串
 */
void UART_SendString(const char *str)
{
    HAL_UART_Transmit(&UART_DEBUG, (uint8_t *)str, strlen(str), 100);
}

/**
 * @brief 发送格式化字符串
 * @param fmt 格式化字符串
 * @param ... 可变参数
 */
void UART_SendFormat(const char *fmt, ...)
{
    va_list args;
    va_start(args, fmt);
    uart_handle.tx_len = vsnprintf((char *)uart_handle.tx_buffer,
                                   UART_TX_BUF_SIZE, fmt, args);
    va_end(args);

    if (uart_handle.tx_len > 0)
    {
        HAL_UART_Transmit(&UART_DEBUG, uart_handle.tx_buffer,
                          uart_handle.tx_len, 100);
    }
}

/**
 * @brief 发送数据帧（带校验）
 * @param data 数据缓冲区
 * @param len 数据长度
 * 
 * 帧格式: 0xAA 0x55 len data[0..len-1] checksum
 * checksum = 所有字节异或
 */
void UART_SendFrame(uint8_t *data, uint8_t len)
{
    uint8_t frame[UART_TX_BUF_SIZE];
    uint8_t i;
    uint8_t checksum = 0;

    if (len + 4 > UART_TX_BUF_SIZE)
        return;

    frame[0] = 0xAA;  // 帧头1
    frame[1] = 0x55;  // 帧头2
    frame[2] = len;   // 数据长度

    for (i = 0; i < len; i++)
    {
        frame[3 + i] = data[i];
        checksum ^= data[i];
    }

    frame[3 + len] = checksum;  // 校验和

    HAL_UART_Transmit(&UART_DEBUG, frame, len + 4, 100);
}

/**
 * @brief 串口接收中断回调
 * @param data 接收到的字节
 * 
 * 处理逻辑:
 *   1. 单字节指令 ('S', 'T', 'P', 'C') 直接处理
 *   2. 多字节指令（远程控制）缓存到缓冲区，遇到 '\n' 或 '\r' 时解析
 */
void UART_RxCallback(uint8_t data)
{
    // 单字符指令
    if (data == CMD_START || data == CMD_STOP ||
        data == CMD_PRINT || data == CMD_CALIBRATE)
    {
        UART_ProcessCharCmd(data);
        return;
    }

    // 远程控制指令缓冲
    if (data == '\n' || data == '\r')
    {
        if (uart_handle.rx_index > 0)
        {
            // 字符串结束，解析
            uart_handle.rx_buffer[uart_handle.rx_index] = '\0';
            UART_ParseRemoteCmd((char *)uart_handle.rx_buffer);
            uart_handle.rx_index = 0;
        }
    }
    else
    {
        // 缓存到缓冲区
        if (uart_handle.rx_index < UART_RX_BUF_SIZE - 1)
        {
            uart_handle.rx_buffer[uart_handle.rx_index++] = data;
        }
    }
}

/**
 * @brief 心跳检测
 * 每100ms在主循环中调用，用于检测串口连接状态
 */
void UART_HeartbeatCheck(void)
{
    static uint32_t last_heartbeat = 0;
    uint32_t now = HAL_GetTick();

    // 每100ms输出一个'.'表示系统正常运行
    if (now - last_heartbeat >= 100)
    {
        last_heartbeat = now;
        // 可以取消注释以下行来查看心跳
        // UART_SendString(".");
    }
}