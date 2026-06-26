/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : STM32F103C8T6 自平衡小车 - 主程序
  * @note           : 控制频率: 1kHz (TIM1中断)
  *                   串口波特率: 115200
  *                   传感器: MPU6050 (I2C1)
  *                   电机驱动: TB6612 (TIM2_CH3/CH4 PWM)
  *                   编码器: TIM2_CH1/CH2(左), TIM3(右)
  ******************************************************************************
  */
/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* USER CODE BEGIN Includes */
#include "mpu6050.h"
#include "pid.h"
#include "motor.h"
#include "encoder.h"
#include "uart_protocol.h"
#include "power_manager.h"
#include "indicator.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */

/* ======================== 外设句柄 ======================== */

I2C_HandleTypeDef    hi2c1;
TIM_HandleTypeDef    htim1;   // 1kHz控制定时器TIM1
TIM_HandleTypeDef    htim2;   // 左编码器TIM2
TIM_HandleTypeDef    htim3;   // 右编码器TIM3
TIM_HandleTypeDef    htim4;   // 保留，当前未使用
UART_HandleTypeDef   huart1;  // 调试/蓝牙 USART1
UART_HandleTypeDef   huart2;  // 语音模块 USART2
ADC_HandleTypeDef    hadc1;   // 电池电压检测

/* ======================== 全局变量定义 ======================== */

SystemState_t g_system_state = SYSTEM_INIT;
float g_pitch_angle = 0.0f;
float g_left_speed = 0.0f;
float g_right_speed = 0.0f;
float g_target_speed = 0.0f;
float g_target_turn = 0.0f;
float g_battery_voltage = 0.0f;
uint32_t g_sys_tick_ms = 0;

/* ======================== 私有变量 ======================== */

static MPU6050_DataRaw_t   mpu_raw;
static MPU6050_DataScaled_t mpu_scaled;
static uint32_t last_print_ms = 0;
static uint8_t uart1_rx_byte;

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_I2C1_Init(void);
static void MX_TIM2_Init(void);
static void MX_TIM3_Init(void);
static void MX_TIM4_Init(void);
static void MX_USART1_UART_Init(void);
static void MX_USART2_UART_Init(void);
static void MX_ADC1_Init(void);

/* USER CODE BEGIN PFP */
static void System_StateMachine(void);
static void TIM1_Config(void);
/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* ======================== TIM1 1kHz 中断服务函数 ======================== */

void TIM1_UP_IRQHandler(void)
{
    if (__HAL_TIM_GET_IT_SOURCE(&htim1, TIM_IT_UPDATE) != RESET)
    {
        __HAL_TIM_CLEAR_IT(&htim1, TIM_IT_UPDATE);

        // 只有在平衡状态下才执行控制算法
        if (g_system_state == SYSTEM_BALANCING)
        {
            // 第1步：读取MPU6050所有数据
            MPU6050_ReadAll(&mpu_raw);

            // 第2步：换算为物理量
            MPU6050_ScaleData(&mpu_raw, &mpu_scaled);

            // 第3步：从加速度计计算倾斜角度
            float acc_pitch = MPU6050_CalcAccPitch(
                mpu_scaled.accel_x,
                mpu_scaled.accel_y,
                mpu_scaled.accel_z);

            // 第4步：互补滤波融合
            g_pitch_angle = MPU6050_ComplementaryFilter(
                mpu_scaled.gyro_y, acc_pitch, 0.001f);

            // 第5步：读取编码器速度
            g_left_speed  = Encoder_ReadSpeed(&g_encoder_left);
            g_right_speed = Encoder_ReadSpeed(&g_encoder_right);

            // 第6步：串级PID控制
            PID_CascadeControl(g_target_speed, g_pitch_angle,
                               mpu_scaled.gyro_y,
                               g_left_speed, g_right_speed);
        }
    }
}

/* ======================== 系统状态机 ======================== */

static void System_StateMachine(void)
{
    static SystemState_t last_state = SYSTEM_INIT;

    if (g_system_state != last_state)
    {
        last_state = g_system_state;
        // 状态变化时更新指示灯
        Indicator_UpdateByState(g_system_state);
    }

    switch (g_system_state)
    {
        case SYSTEM_INIT:
            // 初始化中，不做任何操作
            break;

        case SYSTEM_STARTUP:
            // 启动中，等待用户发送 'S' 指令进入平衡模式
            break;

        case SYSTEM_BALANCING:
            // 平衡中，控制算法在中断中执行
            break;

        case SYSTEM_LOW_BAT:
            // 低电量，停止电机，提示用户
            Motor_StopAll();
            break;

        case SYSTEM_FALLEN:
            // 摔倒保护，停止电机
            Motor_StopAll();
            break;

        case SYSTEM_SLEEP:
            // 休眠模式，停止电机
            Motor_StopAll();
            break;

        case SYSTEM_ERROR:
            // 错误状态，停止电机
            Motor_StopAll();
            break;
    }
}

/* ======================== USART1 中断回调 ======================== */

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
    if (huart->Instance == USART1)
    {
        // 调用串口协议处理
        UART_RxCallback(uart1_rx_byte);
        // 继续接收
        HAL_UART_Receive_IT(&huart1, &uart1_rx_byte, 1);
    }
}

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_I2C1_Init();
  MX_TIM2_Init();
  MX_TIM3_Init();
  // MX_TIM4_Init();  // PWM 已移至 TIM2_CH3/CH4
  MX_USART1_UART_Init();
  MX_USART2_UART_Init();
  MX_ADC1_Init();

  /* USER CODE BEGIN 2 */

  // 配置1kHz控制定时器
  TIM1_Config();

  // 模块初始化
  Indicator_Init();
  Motor_Init();
  Encoder_Init();
  UART_Protocol_Init();
  Power_Init();

  // 初始化MPU6050
  if (MPU6050_Init(&hi2c1) != 0)
  {
      // MPU6050初始化失败，进入错误状态
      g_system_state = SYSTEM_ERROR;
      Indicator_SetColor(RGB_RED);
      UART_SendString("MPU6050 init failed!\r\n");
  }
  else
  {
      // 初始化成功，进入启动状态
      g_system_state = SYSTEM_STARTUP;
      Indicator_SetColor(RGB_BLUE);
      UART_SendString("System init OK!\r\n");
      UART_SendString("Send 'S' to start balancing.\r\n");
  }

  // 启动UART1中断接收
  HAL_UART_Receive_IT(&huart1, &uart1_rx_byte, 1);

  // 启动TIM1定时器 (1kHz)
  HAL_TIM_Base_Start_IT(&htim1);

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
      // 更新系统运行时间
      g_sys_tick_ms = HAL_GetTick();

      // 1. 电源管理 - 检查电池和摔倒
      Power_Process();

      // 2. 状态机 - 根据状态控制LED和电机
      System_StateMachine();

      // 3. 指示灯处理 - 闪烁逻辑
      Indicator_Process();

      // 4. 每100ms心跳检测
      if (g_sys_tick_ms - last_print_ms >= 100)
      {
          last_print_ms = g_sys_tick_ms;
          UART_HeartbeatCheck();
      }

      // 5. 每500ms上报数据（蓝牙连接时）
      if (g_system_state == SYSTEM_BALANCING)
      {
          static uint32_t last_report_ms = 0;
          if (g_sys_tick_ms - last_report_ms >= 500)
          {
              last_report_ms = g_sys_tick_ms;
              UART_ReportSensorData();
          }
      }
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
  RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.HSEPredivValue = RCC_HSE_PREDIV_DIV1;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL9;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK | RCC_CLOCKTYPE_SYSCLK
                                | RCC_CLOCKTYPE_PCLK1 | RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }

  PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_ADC;
  PeriphClkInit.AdcClockSelection = RCC_ADCPCLK2_DIV2;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */

/**
 * @brief TIM1 配置 (1kHz)
 */
static void TIM1_Config(void)
{
    TIM_ClockConfigTypeDef sClockSourceConfig = {0};
    TIM_MasterConfigTypeDef sMasterConfig = {0};

    htim1.Instance = TIM1;
    htim1.Init.Prescaler = 72 - 1;          // 72MHz / 72 = 1MHz
    htim1.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim1.Init.Period = 1000 - 1;            // 1MHz / 1000 = 1kHz
    htim1.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    htim1.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;

    if (HAL_TIM_Base_Init(&htim1) != HAL_OK)
    {
        Error_Handler();
    }

    sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
    HAL_TIM_ConfigClockSource(&htim1, &sClockSourceConfig);

    sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
    sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
    HAL_TIMEx_MasterConfigSynchronization(&htim1, &sMasterConfig);
}

/**
 * @brief ADC1 初始化 (电池电压检测)
 */
static void MX_ADC1_Init(void)
{
    ADC_ChannelConfTypeDef sConfig = {0};

    hadc1.Instance = ADC1;
    hadc1.Init.ScanConvMode = ADC_SCAN_DISABLE;
    hadc1.Init.ContinuousConvMode = DISABLE;
    hadc1.Init.DiscontinuousConvMode = DISABLE;
    hadc1.Init.ExternalTrigConv = ADC_SOFTWARE_START;
    hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;
    hadc1.Init.NbrOfConversion = 1;
    if (HAL_ADC_Init(&hadc1) != HAL_OK)
        Error_Handler();

    sConfig.Channel = ADC_CHANNEL_4;
    sConfig.Rank = ADC_REGULAR_RANK_1;
    sConfig.SamplingTime = ADC_SAMPLETIME_55CYCLES_5;
    if (HAL_ADC_ConfigChannel(&hadc1, &sConfig) != HAL_OK)
        Error_Handler();
}

/**
 * @brief GPIO 初始化
 */
static void MX_GPIO_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};

    __HAL_RCC_GPIOA_CLK_ENABLE();
    __HAL_RCC_GPIOB_CLK_ENABLE();
    // 注意：STM32F103C8T6(LQFP48) 没有 PC0~PC4 引脚，LED/蜂鸣器改用 PB 引脚
    // GPIOC 仅引出 PC13/PC14/PC15，本项目中未使用
    __HAL_RCC_GPIOD_CLK_ENABLE();

    // 电机方向引脚 - PB0, PB1, PB12, PB13
    GPIO_InitStruct.Pin = GPIO_PIN_0 | GPIO_PIN_1 | GPIO_PIN_12 | GPIO_PIN_13;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

    // RGB LED - PB14(R), PB15(G), PB8(B)
    GPIO_InitStruct.Pin = GPIO_PIN_14 | GPIO_PIN_15 | GPIO_PIN_8;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

    // 蜂鸣器 - PB3
    GPIO_InitStruct.Pin = GPIO_PIN_3;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

    // 电池电压检测 ADC - PA4 (ADC1_IN4) 配置为模拟输入
    GPIO_InitStruct.Pin = GPIO_PIN_4;
    GPIO_InitStruct.Mode = GPIO_MODE_ANALOG;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

    // 初始状态：所有LED关闭，蜂鸣器关闭
    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_14 | GPIO_PIN_15 | GPIO_PIN_8, GPIO_PIN_RESET);
    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_3, GPIO_PIN_RESET);
}

/**
 * @brief I2C1 初始化 (用于 MPU6050)
 */
static void MX_I2C1_Init(void)
{
    hi2c1.Instance = I2C1;
    hi2c1.Init.ClockSpeed = 400000;
    hi2c1.Init.DutyCycle = I2C_DUTYCYCLE_2;
    hi2c1.Init.OwnAddress1 = 0;
    hi2c1.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
    hi2c1.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
    hi2c1.Init.OwnAddress2 = 0;
    hi2c1.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
    hi2c1.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;
    if (HAL_I2C_Init(&hi2c1) != HAL_OK)
        Error_Handler();
}

/**
 * @brief TIM2 初始化 (左编码器 + 电机PWM)
 * 混合模式：CH1/CH2 编码器输入 (PA0/PA1), CH3/CH4 PWM 输出 (PA2/PA3)
 */
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
    // TIM2 支持混合模式：编码器 CH1/CH2 输入 + PWM CH3/CH4 输出

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

/**
 * @brief TIM3 初始化 (右编码器)
 * PB4 = TIM3_CH1 (部分重映射), PB5 = TIM3_CH2 (部分重映射)
 */
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

/**
 * @brief TIM4 初始化 (未使用，保留)
 * 注意：PWM 已移至 TIM2_CH3/CH4 (PA2/PA3)
 *      PA6/PA7 没有 TIM4_CH1/CH2 复用功能，实际为 TIM3_CH1/CH2
 */
static void MX_TIM4_Init(void)
{
    // 当前未使用 - PWM 由 TIM2_CH3/CH4 提供
    TIM_OC_InitTypeDef sConfigOC = {0};

    htim4.Instance = TIM4;
    htim4.Init.Prescaler = 72 - 1;
    htim4.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim4.Init.Period = 1000 - 1;
    htim4.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    htim4.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;

    if (HAL_TIM_PWM_Init(&htim4) != HAL_OK)
        Error_Handler();

    sConfigOC.OCMode = TIM_OCMODE_PWM1;
    sConfigOC.Pulse = 0;
    sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
    sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;

    if (HAL_TIM_PWM_ConfigChannel(&htim4, &sConfigOC, TIM_CHANNEL_1) != HAL_OK)
        Error_Handler();
    if (HAL_TIM_PWM_ConfigChannel(&htim4, &sConfigOC, TIM_CHANNEL_2) != HAL_OK)
        Error_Handler();

    HAL_TIM_PWM_Start(&htim4, TIM_CHANNEL_1);
    HAL_TIM_PWM_Start(&htim4, TIM_CHANNEL_2);
}

/**
 * @brief USART1 初始化 (调试/蓝牙)
 */
static void MX_USART1_UART_Init(void)
{
    huart1.Instance = USART1;
    huart1.Init.BaudRate = 115200;
    huart1.Init.WordLength = UART_WORDLENGTH_8B;
    huart1.Init.StopBits = UART_STOPBITS_1;
    huart1.Init.Parity = UART_PARITY_NONE;
    huart1.Init.Mode = UART_MODE_TX_RX;
    huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
    huart1.Init.OverSampling = UART_OVERSAMPLING_16;
    if (HAL_UART_Init(&huart1) != HAL_OK)
        Error_Handler();
}

/**
 * @brief USART2 初始化 (语音模块)
 */
static void MX_USART2_UART_Init(void)
{
    huart2.Instance = USART2;
    huart2.Init.BaudRate = 115200;
    huart2.Init.WordLength = UART_WORDLENGTH_8B;
    huart2.Init.StopBits = UART_STOPBITS_1;
    huart2.Init.Parity = UART_PARITY_NONE;
    huart2.Init.Mode = UART_MODE_TX_RX;
    huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
    huart2.Init.OverSampling = UART_OVERSAMPLING_16;
    if (HAL_UART_Init(&huart2) != HAL_OK)
        Error_Handler();
}

/* ======================== HAL MSP 初始化回调 ======================== */

void HAL_TIM_Base_MspInit(TIM_HandleTypeDef *htim)
{
    if (htim->Instance == TIM1)
    {
        __HAL_RCC_TIM1_CLK_ENABLE();
        HAL_NVIC_SetPriority(TIM1_UP_IRQn, 1, 0);
        HAL_NVIC_EnableIRQ(TIM1_UP_IRQn);
    }
}

void HAL_TIM_PWM_MspInit(TIM_HandleTypeDef *htim)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    if (htim->Instance == TIM2)
    {
        __HAL_RCC_TIM2_CLK_ENABLE();
        __HAL_RCC_GPIOA_CLK_ENABLE();
        // PA2, PA3 配置为复用推挽输出 (TIM2_CH3/CH4)
        GPIO_InitStruct.Pin = GPIO_PIN_2 | GPIO_PIN_3;
        GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
        GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
        HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    }
    else if (htim->Instance == TIM4)
    {
        // TIM4 当前未使用，保留 MSP 初始化代码
        __HAL_RCC_TIM4_CLK_ENABLE();
    }
}

void HAL_TIM_Encoder_MspInit(TIM_HandleTypeDef *htim)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    if (htim->Instance == TIM2)
    {
        __HAL_RCC_TIM2_CLK_ENABLE();
        __HAL_RCC_GPIOA_CLK_ENABLE();
        GPIO_InitStruct.Pin = GPIO_PIN_0 | GPIO_PIN_1;
        GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
        GPIO_InitStruct.Pull = GPIO_NOPULL;
        HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    }
    else if (htim->Instance == TIM3)
    {
        __HAL_RCC_TIM3_CLK_ENABLE();
        __HAL_RCC_AFIO_CLK_ENABLE();
        __HAL_AFIO_REMAP_TIM3_PARTIAL();
        __HAL_RCC_GPIOB_CLK_ENABLE();
        GPIO_InitStruct.Pin = GPIO_PIN_4 | GPIO_PIN_5;
        GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
        GPIO_InitStruct.Pull = GPIO_NOPULL;
        HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
    }
}

void HAL_UART_MspInit(UART_HandleTypeDef *huart)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    if (huart->Instance == USART1)
    {
        __HAL_RCC_USART1_CLK_ENABLE();
        __HAL_RCC_GPIOA_CLK_ENABLE();
        GPIO_InitStruct.Pin = GPIO_PIN_9;
        GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
        GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
        HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
        GPIO_InitStruct.Pin = GPIO_PIN_10;
        GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
        GPIO_InitStruct.Pull = GPIO_NOPULL;
        HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
        HAL_NVIC_SetPriority(USART1_IRQn, 2, 0);
        HAL_NVIC_EnableIRQ(USART1_IRQn);
    }
    else if (huart->Instance == USART2)
    {
        __HAL_RCC_USART2_CLK_ENABLE();
        __HAL_RCC_GPIOB_CLK_ENABLE();
        GPIO_InitStruct.Pin = GPIO_PIN_10;
        GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
        GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
        HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
        GPIO_InitStruct.Pin = GPIO_PIN_11;
        GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
        GPIO_InitStruct.Pull = GPIO_NOPULL;
        HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
        HAL_NVIC_SetPriority(USART2_IRQn, 2, 0);
        HAL_NVIC_EnableIRQ(USART2_IRQn);
    }
}

void HAL_ADC_MspInit(ADC_HandleTypeDef *hadc)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    if (hadc->Instance == ADC1)
    {
        __HAL_RCC_ADC1_CLK_ENABLE();
        __HAL_RCC_GPIOA_CLK_ENABLE();
        GPIO_InitStruct.Pin = GPIO_PIN_0;
        GPIO_InitStruct.Mode = GPIO_MODE_ANALOG;
        HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    }
}

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
    g_system_state = SYSTEM_ERROR;
    Indicator_SetColor(RGB_RED);
    __disable_irq();
    while (1) { }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
    char buf[64];
    sprintf(buf, "Assert failed: %s, line %lu\r\n", file, line);
    UART_SendString(buf);
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */