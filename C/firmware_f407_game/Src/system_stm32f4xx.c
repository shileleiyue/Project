#include "stm32f4xx_hal.h"

/* 系统时钟配置在 main.c 中完成，此处提供默认配置 */
uint32_t SystemCoreClock = 168000000;
const uint8_t AHBPrescTable[16] = {0,0,0,0,0,0,0,0,1,2,3,4,6,7,8,9};
const uint8_t APBPrescTable[8] = {0,0,0,0,1,2,3,4};

void SystemInit(void) {
    /* FPU 使能 */
    #if (__FPU_PRESENT == 1) && (__FPU_USED == 1)
    SCB->CPACR |= ((3UL << 10*2) | (3UL << 11*2));
    #endif

    /* 配置 Flash 等待周期 */
    FLASH->ACR = FLASH_ACR_LATENCY_5WS;

    /* 使能 HSI */
    RCC->CR |= RCC_CR_HSION;
    while ((RCC->CR & RCC_CR_HSIRDY) == 0);

    /* 复位时钟配置 */
    RCC->CFGR = 0;
    RCC->CR &= ~(RCC_CR_HSEON | RCC_CR_CSSON | RCC_CR_PLLON);
    RCC->PLLCFGR = 0x24003010;
    RCC->CR &= ~RCC_CR_HSEBYP;
    RCC->CIR = 0;

    /* 配置中断向量表偏移 */
    SCB->VTOR = FLASH_BASE;
}

void SystemCoreClockUpdate(void) {
    /* 由 RCC 配置自动维护 */
}