#ifndef __GAME_H
#define __GAME_H

#include "stm32f4xx_hal.h"
#include "lcd.h"
#include "touch.h"
#include <stdint.h>
#include <stdlib.h>

/* 游戏参数 */
#define GAME_ROWS        4       /* 4行 */
#define GAME_COLS        3       /* 3列 - 共12个洞 */
#define GAME_DURATION    30      /* 游戏时长(秒) */
#define MOLE_SHOW_TIME   1500    /* 地鼠显示时间(ms) */
#define MOLE_HIDE_TIME   800     /* 地鼠隐藏间隔(ms) */
#define MOLE_RADIUS      35      /* 地鼠半径 */
#define HOLE_RADIUS      40      /* 洞口半径 */

/* 游戏状态 */
typedef enum {
    GAME_STATE_IDLE = 0,     /* 空闲/等待开始 */
    GAME_STATE_PLAYING,      /* 游戏中 */
    GAME_STATE_OVER          /* 游戏结束 */
} GameState_t;

/* 洞口结构体 */
typedef struct {
    uint16_t cx;             /* 中心 X */
    uint16_t cy;             /* 中心 Y */
    uint8_t  mole_visible;   /* 地鼠是否可见 */
    uint32_t mole_timer;     /* 地鼠计时器 */
    uint8_t  hit;            /* 是否被打中(闪烁效果) */
    uint32_t hit_timer;      /* 打中闪烁计时器 */
} Hole_t;

/* 游戏数据 */
typedef struct {
    GameState_t state;
    uint32_t    score;
    uint32_t    start_time;
    uint32_t    elapsed;
    uint32_t    combo;
    uint32_t    max_combo;
    uint32_t    miss_count;
    Hole_t      holes[GAME_ROWS * GAME_COLS];
    uint32_t    last_mole_spawn;
    uint32_t    last_frame;
} GameData_t;

/* 函数声明 */
void Game_Init(void);
void Game_Update(void);
void Game_Render(void);
void Game_Start(void);
void Game_HandleTouch(uint16_t x, uint16_t y);

#endif /* __GAME_H */