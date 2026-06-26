/**
  ******************************************************************************
  * @file    system_stm32f1xx.c
  * @brief   STM32F1xx 系统时钟配置文件
  * @details 提供 SystemInit、SystemCoreClockUpdate 以及 SystemCoreClock 变量
  ******************************************************************************
  */

#include "stm32f1xx.h"

/* ======================== 全局变量 ======================== */

/**
  * @brief 系统核心时钟频率 (Hz)
  * @note  初始值设为 8MHz (HSI)，SystemInit 后更新为实际值
  */
uint32_t SystemCoreClock = 8000000;

/* ======================== 时钟预分频表 ======================== */

/**
  * @brief AHB 预分频器值查找表
  * @note  对应 RCC_CFGR 寄存器 HPRE[3:0] 位域
  */
const uint8_t AHBPrescTable[16] = {
    0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 6, 7, 8, 9
};

/**
  * @brief APB 预分频器值查找表
  * @note  对应 RCC_CFGR 寄存器 PPRE1[2:0] / PPRE2[2:0] 位域
  */
const uint8_t APBPrescTable[8] = {
    0, 0, 0, 0, 1, 2, 3, 4
};

/* ======================== 系统初始化函数 ======================== */

/**
  * @brief  系统初始化函数
  * @note   启动后由 Reset_Handler 调用
  *         设置中断向量表偏移，启动 HSE 振荡器
  *         用户应在 SystemClock_Config() 中完成 PLL 配置
  */
void SystemInit(void)
{
    /* 设置中断向量表偏移地址为 Flash 起始地址 */
    SCB->VTOR = FLASH_BASE | 0x00;

    /* 启动 HSE 振荡器（如果尚未启用） */
    RCC->CR |= ((uint32_t)RCC_CR_HSEON);

    /* 等待 HSE 就绪 */
    while (!(RCC->CR & RCC_CR_HSERDY))
    {
        /* 等待 HSE 稳定 */
    }

    /* 关闭所有外设时钟（可选，降低功耗） */
    RCC->APB1RSTR = 0x00000000;
    RCC->APB2RSTR = 0x00000000;

    /* 更新 SystemCoreClock */
    SystemCoreClockUpdate();
}

/**
  * @brief  更新 SystemCoreClock 变量
  * @note   根据 RCC_CFGR 寄存器的配置计算当前系统时钟频率
  */
void SystemCoreClockUpdate(void)
{
    uint32_t tmp = 0, pllmul = 0, pllsource = 0;
    uint32_t predivfactor = 0;

    /* 获取 SYSCLK 源 */
    tmp = RCC->CFGR & RCC_CFGR_SWS;

    switch (tmp)
    {
        case 0x00:  /* HSI 作为系统时钟 */
            SystemCoreClock = HSI_VALUE;
            break;

        case 0x04:  /* HSE 作为系统时钟 */
            SystemCoreClock = HSE_VALUE;
            break;

        case 0x08:  /* PLL 作为系统时钟 */
            /* 获取 PLL 时钟源 */
            pllsource = (RCC->CFGR & RCC_CFGR_PLLSRC) ? 1 : 0;

            if (pllsource == 0)  /* HSI/2 作为 PLL 输入 */
            {
                SystemCoreClock = HSI_VALUE / 2;
            }
            else  /* HSE 作为 PLL 输入 */
            {
                /* 获取预分频因子 */
                predivfactor = (RCC->CFGR2 & RCC_CFGR2_PREDIV1) + 1;
                SystemCoreClock = HSE_VALUE / predivfactor;
            }

            /* 获取 PLL 倍频因子 */
            pllmul = RCC->CFGR & RCC_CFGR_PLLMULL;
            if (pllmul >= 0x08 && pllmul <= 0x0F)
            {
                pllmul = (pllmul - 0x07) * 2 + 2;
            }
            else if (pllmul == 0x10)
            {
                pllmul = 6;
            }
            else if (pllmul == 0x12)
            {
                pllmul = 7;
            }
            else if (pllmul == 0x14)
            {
                pllmul = 8;
            }
            else if (pllmul == 0x16)
            {
                pllmul = 9;
            }
            else if (pllmul >= 0x18)
            {
                pllmul = (pllmul - 0x17) * 2 + 10;
            }
            else
            {
                pllmul = 2;
            }

            SystemCoreClock *= pllmul;
            break;

        default:
            SystemCoreClock = HSI_VALUE;
            break;
    }

    /* 计算 HCLK 频率 (考虑 AHB 预分频) */
    tmp = AHBPrescTable[((RCC->CFGR & RCC_CFGR_HPRE) >> 7)];
    SystemCoreClock >>= tmp;
}