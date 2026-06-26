/**
  ******************************************************************************
  * @file    main.c
  * @brief   打地鼠游戏主程序 - 探索者 STM32F407ZGT6 + 4.3寸触摸屏
  * @note    系统时钟: 168MHz (HSE 8MHz -> PLL)
  *          LCD: ILI9341 FSMC 16位并行接口
  *          Touch: FT5206 I2C2
  *          背光: TIM3_CH3 PWM
  ******************************************************************************
  */

#include "main.h"

/* ======================== 外设句柄定义 ======================== */

I2C_HandleTypeDef   hi2c2;
TIM_HandleTypeDef   htim3;
SRAM_HandleTypeDef  hsram1;

/* 系统滴答计数器 */
static uint32_t g_sys_tick = 0;

/* ======================== 系统时钟配置 ======================== */

void SystemClock_Config(void) {
    RCC_OscInitTypeDef RCC_OscInitStruct = {0};
    RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

    /* 使能电源时钟 */
    __HAL_RCC_PWR_CLK_ENABLE();
    __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

    /* 配置 HSE 8MHz -> PLL -> 168MHz */
    RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
    RCC_OscInitStruct.HSEState = RCC_HSE_ON;
    RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
    RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
    RCC_OscInitStruct.PLL.PLLM = 8;
    RCC_OscInitStruct.PLL.PLLN = 336;
    RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
    RCC_OscInitStruct.PLL.PLLQ = 7;
    HAL_RCC_OscConfig(&RCC_OscInitStruct);

    /* 配置时钟总线: HCLK=168MHz, APB1=42MHz, APB2=84MHz */
    RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK | RCC_CLOCKTYPE_SYSCLK
                                | RCC_CLOCKTYPE_PCLK1 | RCC_CLOCKTYPE_PCLK2;
    RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
    RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
    RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV4;
    RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV2;
    HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_5);
}

/* ======================== GPIO 初始化 ======================== */

void MX_GPIO_Init(void) {
    GPIO_InitTypeDef GPIO_InitStruct = {0};

    /* 使能 GPIO 时钟 */
    __HAL_RCC_GPIOA_CLK_ENABLE();
    __HAL_RCC_GPIOB_CLK_ENABLE();
    __HAL_RCC_GPIOC_CLK_ENABLE();
    __HAL_RCC_GPIOD_CLK_ENABLE();
    __HAL_RCC_GPIOE_CLK_ENABLE();
    __HAL_RCC_GPIOF_CLK_ENABLE();
    __HAL_RCC_GPIOG_CLK_ENABLE();

    /* 板载 LED: PF9, PF10 */
    HAL_GPIO_WritePin(GPIOF, GPIO_PIN_9 | GPIO_PIN_10, GPIO_PIN_SET);
    GPIO_InitStruct.Pin = GPIO_PIN_9 | GPIO_PIN_10;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOF, &GPIO_InitStruct);

    /* 按键: PE2, PE3, PE4 (上拉输入) */
    GPIO_InitStruct.Pin = GPIO_PIN_2 | GPIO_PIN_3 | GPIO_PIN_4;
    GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    HAL_GPIO_Init(GPIOE, &GPIO_InitStruct);

    /* WKUP: PA0 (下拉输入) */
    GPIO_InitStruct.Pin = GPIO_PIN_0;
    GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
    GPIO_InitStruct.Pull = GPIO_PULLDOWN;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
}

/* ======================== FSMC 初始化 (LCD 16位并口) ======================== */

void MX_FSMC_Init(void) {
    SRAM_HandleTypeDef *hsram = &hsram1;
    FSMC_NORSRAM_TimingTypeDef Timing = {0};

    /* 使能 FSMC 时钟 */
    __HAL_RCC_FSMC_CLK_ENABLE();

    hsram->Instance = FSMC_NORSRAM_DEVICE;
    hsram->Extended = FSMC_NORSRAM_EXTENDED_DEVICE;

    /* FSMC 初始化 */
    hsram->Init.NSBank = FSMC_NORSRAM_BANK4;
    hsram->Init.DataAddressMux = FSMC_DATA_ADDRESS_MUX_DISABLE;
    hsram->Init.MemoryType = FSMC_MEMORY_TYPE_SRAM;
    hsram->Init.MemoryDataWidth = FSMC_NORSRAM_MEM_BUS_WIDTH_16;
    hsram->Init.BurstAccessMode = FSMC_BURST_ACCESS_MODE_DISABLE;
    hsram->Init.WaitSignalPolarity = FSMC_WAIT_SIGNAL_POLARITY_LOW;
    hsram->Init.WrapMode = FSMC_WRAP_MODE_DISABLE;
    hsram->Init.WaitSignalActive = FSMC_WAIT_TIMING_BEFORE_WS;
    hsram->Init.WriteOperation = FSMC_WRITE_OPERATION_ENABLE;
    hsram->Init.WaitSignal = FSMC_WAIT_SIGNAL_DISABLE;
    hsram->Init.ExtendedMode = FSMC_EXTENDED_MODE_DISABLE;
    hsram->Init.AsynchronousWait = FSMC_ASYNCHRONOUS_WAIT_DISABLE;
    hsram->Init.WriteBurst = FSMC_WRITE_BURST_DISABLE;
    hsram->Init.ContinuousClock = FSMC_CONTINUOUS_CLOCK_SYNC_ONLY;

    /* 读时序: 地址建立 15 HCLK, 数据建立 42 HCLK */
    Timing.AddressSetupTime = 15;
    Timing.AddressHoldTime = 0;
    Timing.DataSetupTime = 42;
    Timing.BusTurnAroundDuration = 0;
    Timing.CLKDivision = 0;
    Timing.DataLatency = 0;
    Timing.AccessMode = FSMC_ACCESS_MODE_A;

    HAL_SRAM_Init(hsram, &Timing, &Timing);
}

/* ======================== I2C2 初始化 (FT5206 触摸) ======================== */

void MX_I2C2_Init(void) {
    hi2c2.Instance = I2C2;
    hi2c2.Init.ClockSpeed = 100000;
    hi2c2.Init.DutyCycle = I2C_DUTYCYCLE_2;
    hi2c2.Init.OwnAddress1 = 0;
    hi2c2.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
    hi2c2.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
    hi2c2.Init.OwnAddress2 = 0;
    hi2c2.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
    hi2c2.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;
    HAL_I2C_Init(&hi2c2);
}

/* ======================== TIM3 初始化 (LCD 背光 PWM) ======================== */

void MX_TIM3_Init(void) {
    TIM_OC_InitTypeDef sConfigOC = {0};

    htim3.Instance = TIM3;
    htim3.Init.Prescaler = 84 - 1;       /* 84MHz / 84 = 1MHz */
    htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim3.Init.Period = 1000 - 1;        /* 1MHz / 1000 = 1kHz PWM */
    htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    htim3.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;
    HAL_TIM_PWM_Init(&htim3);

    sConfigOC.OCMode = TIM_OCMODE_PWM1;
    sConfigOC.Pulse = 800;               /* 初始 80% 亮度 */
    sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
    sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
    HAL_TIM_PWM_ConfigChannel(&htim3, &sConfigOC, TIM_CHANNEL_3);
}

/* HAL_TIM_PWM_MspInit: 背光 PWM 引脚配置 */
void HAL_TIM_PWM_MspInit(TIM_HandleTypeDef *htim) {
    if (htim->Instance == TIM3) {
        GPIO_InitTypeDef GPIO_InitStruct = {0};

        __HAL_RCC_TIM3_CLK_ENABLE();
        __HAL_RCC_GPIOB_CLK_ENABLE();

        /* PB0 -> TIM3_CH3 */
        GPIO_InitStruct.Pin = GPIO_PIN_0;
        GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
        GPIO_InitStruct.Pull = GPIO_NOPULL;
        GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
        GPIO_InitStruct.Alternate = GPIO_AF2_TIM3;
        HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
    }
}

/* HAL_I2C_MspInit: I2C2 引脚配置 */
void HAL_I2C_MspInit(I2C_HandleTypeDef *hi2c) {
    if (hi2c->Instance == I2C2) {
        GPIO_InitTypeDef GPIO_InitStruct = {0};

        __HAL_RCC_I2C2_CLK_ENABLE();
        __HAL_RCC_GPIOB_CLK_ENABLE();

        /* PB10 -> I2C2_SCL, PB11 -> I2C2_SDA */
        GPIO_InitStruct.Pin = GPIO_PIN_10 | GPIO_PIN_11;
        GPIO_InitStruct.Mode = GPIO_MODE_AF_OD;
        GPIO_InitStruct.Pull = GPIO_PULLUP;
        GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
        GPIO_InitStruct.Alternate = GPIO_AF4_I2C2;
        HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
    }
}

/* ======================== 随机数种子初始化 ======================== */

static void RandomInit(void) {
    /* 使用 SysTick 和未初始化的 SRAM 作为随机种子 */
    uint32_t seed = HAL_GetTick();
    /* 混合一些 ADC 噪声 (如果有的话) */
    seed ^= (uint32_t)(&seed);
    srand(seed);
}

/* ======================== 主程序 ======================== */

int main(void) {
    /* HAL 初始化 */
    HAL_Init();

    /* 系统时钟配置 */
    SystemClock_Config();

    /* 外设初始化 */
    MX_GPIO_Init();
    MX_FSMC_Init();
    MX_I2C2_Init();
    MX_TIM3_Init();

    /* 启动背光 PWM */
    HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_3);

    /* 初始化随机数种子 */
    RandomInit();

    /* 初始化 LCD */
    LCD_Init();
    LCD_Clear(COLOR_BLACK);

    /* 初始化触摸屏 */
    Touch_Init();

    /* 初始化游戏 */
    Game_Init();

    /* 背光调亮 */
    LCD_SetBackLight(90);

    /* 状态 LED 闪烁表示初始化完成 */
    HAL_GPIO_WritePin(GPIOF, GPIO_PIN_9, GPIO_PIN_RESET);
    HAL_Delay(200);
    HAL_GPIO_WritePin(GPIOF, GPIO_PIN_9, GPIO_PIN_SET);

    /* 绘制初始界面 */
    Game_Render();

    /* ======================== 主循环 ======================== */
    while (1) {
        uint32_t frame_start = HAL_GetTick();
        uint8_t need_render = 0;

        /* 检查按键 KEY0 启动游戏 */
        if (HAL_GPIO_ReadPin(KEY0_PORT, KEY0_PIN) == GPIO_PIN_RESET) {
            HAL_Delay(20);  /* 消抖 */
            if (HAL_GPIO_ReadPin(KEY0_PORT, KEY0_PIN) == GPIO_PIN_RESET) {
                if (g_game.state == GAME_STATE_IDLE || g_game.state == GAME_STATE_OVER) {
                    Game_Start();
                    need_render = 1;
                }
                /* 等待按键释放 */
                while (HAL_GPIO_ReadPin(KEY0_PORT, KEY0_PIN) == GPIO_PIN_RESET);
            }
        }

        /* 触摸扫描 */
        if (Touch_Scan()) {
            TouchPoint_t tp = Touch_GetPoint();
            if (tp.pressed) {
                Game_HandleTouch(tp.x, tp.y);
                need_render = 1;
            }
        }

        /* 游戏逻辑更新 */
        {
            GameState_t prev_state = g_game.state;
            Game_Update();
            if (g_game.state != prev_state) {
                need_render = 1;  /* 状态变化时重绘 */
            }
        }

        /* 游戏中每 200ms 重绘一次 */
        if (g_game.state == GAME_STATE_PLAYING) {
            static uint32_t last_render = 0;
            if (HAL_GetTick() - last_render >= 200) {
                need_render = 1;
                last_render = HAL_GetTick();
            }
        }

        /* 渲染 */
        if (need_render) {
            Game_Render();
            /* 活动 LED 闪烁 */
            HAL_GPIO_TogglePin(GPIOF, GPIO_PIN_10);
        }

        /* 帧率控制: 约 30 FPS */
        uint32_t frame_time = HAL_GetTick() - frame_start;
        if (frame_time < 33) {
            HAL_Delay(33 - frame_time);
        }
    }
}

/* ======================== 错误处理 ======================== */

void Error_Handler(void) {
    __disable_irq();
    while (1) {
        /* 错误状态: LED 快速闪烁 */
        HAL_GPIO_TogglePin(GPIOF, GPIO_PIN_9);
        for (volatile uint32_t i = 0; i < 100000; i++);
    }
}