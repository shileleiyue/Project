/**
  ******************************************************************************
  * @file    game.c
  * @brief   打地鼠游戏 (Whack-a-Mole)
  * @note    4x3 网格，12个洞，30秒倒计时，触摸屏点击
  ******************************************************************************
  */

#include "game.h"
#include <string.h>

/* 全局游戏数据 */
static GameData_t g_game;

/* 洞口布局: 计算每个洞口的中心坐标 */
/* 屏幕 480x800，留出顶部状态栏 80px 和底部区域 */
static const uint16_t GRID_TOP     = 140;   /* 网格顶部 Y */
static const uint16_t GRID_LEFT    = 45;    /* 网格左侧 X */
static const uint16_t GRID_GAP_X   = 130;   /* 列间距 */
static const uint16_t GRID_GAP_Y   = 150;   /* 行间距 */

/* ======================== 初始化游戏 ======================== */

void Game_Init(void) {
    uint8_t i;
    memset(&g_game, 0, sizeof(GameData_t));

    /* 计算每个洞口位置 */
    for (i = 0; i < GAME_ROWS * GAME_COLS; i++) {
        uint8_t row = i / GAME_COLS;
        uint8_t col = i % GAME_COLS;
        g_game.holes[i].cx = GRID_LEFT + col * GRID_GAP_X;
        g_game.holes[i].cy = GRID_TOP  + row * GRID_GAP_Y;
        g_game.holes[i].mole_visible = 0;
        g_game.holes[i].mole_timer = 0;
        g_game.holes[i].hit = 0;
        g_game.holes[i].hit_timer = 0;
    }

    g_game.state = GAME_STATE_IDLE;
    g_game.score = 0;
    g_game.combo = 0;
    g_game.max_combo = 0;
    g_game.miss_count = 0;
    g_game.last_mole_spawn = 0;
    g_game.last_frame = 0;
}

/* ======================== 开始游戏 ======================== */

void Game_Start(void) {
    Game_Init();
    g_game.state = GAME_STATE_PLAYING;
    g_game.start_time = HAL_GetTick();
    g_game.last_mole_spawn = g_game.start_time;
    g_game.last_frame = g_game.start_time;

    /* 生成第一个地鼠 */
    uint8_t idx = rand() % (GAME_ROWS * GAME_COLS);
    g_game.holes[idx].mole_visible = 1;
    g_game.holes[idx].mole_timer = HAL_GetTick();
}

/* ======================== 游戏更新 ======================== */

void Game_Update(void) {
    uint32_t now = HAL_GetTick();
    uint8_t i;

    if (g_game.state != GAME_STATE_PLAYING) return;

    /* 更新计时 */
    g_game.elapsed = (now - g_game.start_time) / 1000;

    /* 检查游戏结束 */
    if (g_game.elapsed >= GAME_DURATION) {
        g_game.state = GAME_STATE_OVER;
        return;
    }

    /* 更新每个洞口 */
    for (i = 0; i < GAME_ROWS * GAME_COLS; i++) {
        Hole_t *hole = &g_game.holes[i];

        /* 打中闪烁效果 */
        if (hole->hit) {
            if (now - hole->hit_timer > 150) {
                hole->hit = 0;
                hole->mole_visible = 0;
            }
            continue;
        }

        /* 地鼠自动隐藏 */
        if (hole->mole_visible) {
            if (now - hole->mole_timer > MOLE_SHOW_TIME) {
                hole->mole_visible = 0;
                g_game.miss_count++;
                g_game.combo = 0;  /* 漏掉重置连击 */
            }
        }
    }

    /* 随机生成新地鼠 */
    if (now - g_game.last_mole_spawn > MOLE_HIDE_TIME) {
        /* 找当前可见地鼠数量 */
        uint8_t visible_count = 0;
        for (i = 0; i < GAME_ROWS * GAME_COLS; i++) {
            if (g_game.holes[i].mole_visible) visible_count++;
        }

        /* 最多同时显示 3 只地鼠 */
        if (visible_count < 3) {
            /* 尝试随机找一个空洞口 */
            uint8_t attempts = 0;
            while (attempts < 20) {
                uint8_t idx = rand() % (GAME_ROWS * GAME_COLS);
                if (!g_game.holes[idx].mole_visible && !g_game.holes[idx].hit) {
                    g_game.holes[idx].mole_visible = 1;
                    g_game.holes[idx].mole_timer = now;
                    break;
                }
                attempts++;
            }
        }
        g_game.last_mole_spawn = now;
    }

    g_game.last_frame = now;
}

/* ======================== 触摸处理 ======================== */

void Game_HandleTouch(uint16_t x, uint16_t y) {
    uint8_t i;

    if (g_game.state == GAME_STATE_IDLE) {
        /* 点击开始按钮区域 */
        if (x >= 140 && x <= 340 && y >= 350 && y <= 420) {
            Game_Start();
        }
        return;
    }

    if (g_game.state == GAME_STATE_OVER) {
        /* 点击重新开始区域 */
        if (x >= 140 && x <= 340 && y >= 550 && y <= 620) {
            Game_Start();
        }
        return;
    }

    /* 游戏中: 检测点击了哪个洞口 */
    if (g_game.state != GAME_STATE_PLAYING) return;

    for (i = 0; i < GAME_ROWS * GAME_COLS; i++) {
        Hole_t *hole = &g_game.holes[i];
        int16_t dx = (int16_t)x - (int16_t)hole->cx;
        int16_t dy = (int16_t)y - (int16_t)hole->cy;

        if (dx * dx + dy * dy <= HOLE_RADIUS * HOLE_RADIUS) {
            if (hole->mole_visible && !hole->hit) {
                /* 打中地鼠! */
                hole->hit = 1;
                hole->hit_timer = HAL_GetTick();
                g_game.combo++;
                if (g_game.combo > g_game.max_combo) {
                    g_game.max_combo = g_game.combo;
                }
                /* 连击加分 */
                g_game.score += 10 + (g_game.combo > 1 ? g_game.combo * 5 : 0);
                return;
            }
        }
    }
}

/* ======================== 游戏渲染 ======================== */

/* 绘制单个洞口 */
static void DrawHole(Hole_t *hole) {
    uint16_t cx = hole->cx;
    uint16_t cy = hole->cy;

    if (hole->hit) {
        /* 打中效果: 黄色闪光 */
        LCD_FillCircle(cx, cy, HOLE_RADIUS, COLOR_YELLOW);
        LCD_DrawCircle(cx, cy, HOLE_RADIUS, COLOR_BLACK);
    } else if (hole->mole_visible) {
        /* 地鼠可见: 棕色圆形 + 眼睛 */
        LCD_FillCircle(cx, cy, MOLE_RADIUS, COLOR_BROWN);

        /* 白色眼睛 */
        LCD_FillCircle(cx - 10, cy - 10, 8, COLOR_WHITE);
        LCD_FillCircle(cx + 10, cy - 10, 8, COLOR_WHITE);

        /* 黑色瞳孔 */
        LCD_FillCircle(cx - 8, cy - 10, 4, COLOR_BLACK);
        LCD_FillCircle(cx + 8, cy - 10, 4, COLOR_BLACK);

        /* 嘴巴 */
        LCD_DrawLine(cx - 8, cy + 8, cx + 8, cy + 8, COLOR_BLACK);
        LCD_DrawLine(cx - 8, cy + 8, cx - 8, cy + 12, COLOR_BLACK);
        LCD_DrawLine(cx + 8, cy + 8, cx + 8, cy + 12, COLOR_BLACK);
        LCD_DrawLine(cx - 8, cy + 12, cx + 8, cy + 12, COLOR_BLACK);

        /* 洞口边框 */
        LCD_DrawCircle(cx, cy, HOLE_RADIUS, COLOR_BLACK);
    } else {
        /* 空洞口: 深色圆 */
        LCD_FillCircle(cx, cy, HOLE_RADIUS, COLOR_GRAY);
        LCD_DrawCircle(cx, cy, HOLE_RADIUS, COLOR_BLACK);
    }
}

/* 绘制顶部状态栏 */
static void DrawHUD(void) {
    char buf[20];
    uint32_t remaining;

    /* 状态栏背景 */
    LCD_FillRect(0, 0, LCD_WIDTH - 1, 79, COLOR_BLACK);

    /* 标题 */
    LCD_ShowString(10, 5, "Whack-a-Mole!", COLOR_YELLOW, COLOR_BLACK, 2);

    if (g_game.state == GAME_STATE_IDLE) {
        LCD_ShowString(10, 45, "Tap screen to play!", COLOR_WHITE, COLOR_BLACK, 1);
        return;
    }

    /* 分数 */
    LCD_ShowString(10, 28, "Score:", COLOR_WHITE, COLOR_BLACK, 1);
    LCD_ShowNum(75, 28, g_game.score, 4, COLOR_GREEN, COLOR_BLACK, 1);

    /* 倒计时 */
    if (g_game.state == GAME_STATE_PLAYING) {
        remaining = GAME_DURATION - g_game.elapsed;
    } else {
        remaining = 0;
    }
    sprintf(buf, "Time: %lu", remaining);
    LCD_ShowString(160, 28, buf, COLOR_CYAN, COLOR_BLACK, 1);

    /* 连击 */
    if (g_game.combo >= 2) {
        sprintf(buf, "Combo x%lu!", g_game.combo);
        LCD_ShowString(300, 28, buf, COLOR_ORANGE, COLOR_BLACK, 1);
    }

    /* 进度条 */
    uint16_t bar_width = (uint16_t)((LCD_WIDTH - 20) * remaining / GAME_DURATION);
    LCD_FillRect(10, 55, LCD_WIDTH - 10, 70, COLOR_GRAY);
    if (bar_width > 0) {
        uint16_t bar_color = (remaining < 10) ? COLOR_RED : COLOR_GREEN;
        LCD_FillRect(10, 55, 10 + bar_width, 70, bar_color);
    }
}

/* 绘制空闲界面 */
static void DrawIdleScreen(void) {
    LCD_Clear(COLOR_DARKGREEN);

    /* 标题 */
    LCD_ShowString(80, 80, "WHACK-A-MOLE", COLOR_YELLOW, COLOR_DARKGREEN, 3);

    /* 说明文字 */
    LCD_ShowString(60, 180, "Tap the moles when they", COLOR_WHITE, COLOR_DARKGREEN, 1);
    LCD_ShowString(60, 200, "pop up to score points!", COLOR_WHITE, COLOR_DARKGREEN, 1);
    LCD_ShowString(60, 230, "30 seconds time limit!", COLOR_WHITE, COLOR_DARKGREEN, 1);

    /* 开始按钮 */
    LCD_FillRect(140, 350, 340, 420, COLOR_GREEN);
    LCD_DrawRect(140, 350, 340, 420, COLOR_BLACK);
    LCD_ShowString(155, 370, "START GAME", COLOR_WHITE, COLOR_GREEN, 2);

    /* 提示 */
    LCD_ShowString(90, 500, "Touch the green button", COLOR_LIGHTGRAY, COLOR_DARKGREEN, 1);
    LCD_ShowString(100, 520, "or press KEY0 to start", COLOR_LIGHTGRAY, COLOR_DARKGREEN, 1);
}

/* 绘制游戏结束界面 */
static void DrawGameOverScreen(void) {
    char buf[30];

    LCD_Clear(COLOR_BLACK);

    /* 结束标题 */
    LCD_ShowString(110, 80, "GAME OVER", COLOR_RED, COLOR_BLACK, 3);

    /* 最终分数 */
    sprintf(buf, "Final Score: %lu", g_game.score);
    LCD_ShowString(80, 180, buf, COLOR_YELLOW, COLOR_BLACK, 2);

    /* 最大连击 */
    sprintf(buf, "Max Combo: %lu", g_game.max_combo);
    LCD_ShowString(80, 230, buf, COLOR_ORANGE, COLOR_BLACK, 2);

    /* 漏掉的地鼠 */
    sprintf(buf, "Missed: %lu", g_game.miss_count);
    LCD_ShowString(80, 280, buf, COLOR_CYAN, COLOR_BLACK, 2);

    /* 评级 */
    if (g_game.score >= 200) {
        LCD_ShowString(80, 340, "Rating: S - Excellent!", COLOR_GREEN, COLOR_BLACK, 2);
    } else if (g_game.score >= 120) {
        LCD_ShowString(80, 340, "Rating: A - Great!", COLOR_GREEN, COLOR_BLACK, 2);
    } else if (g_game.score >= 60) {
        LCD_ShowString(80, 340, "Rating: B - Good!", COLOR_CYAN, COLOR_BLACK, 2);
    } else {
        LCD_ShowString(80, 340, "Rating: C - Try Again!", COLOR_YELLOW, COLOR_BLACK, 2);
    }

    /* 重新开始按钮 */
    LCD_FillRect(140, 550, 340, 620, COLOR_GREEN);
    LCD_DrawRect(140, 550, 340, 620, COLOR_WHITE);
    LCD_ShowString(140, 568, "PLAY AGAIN", COLOR_WHITE, COLOR_GREEN, 2);

    LCD_ShowString(100, 670, "Touch button or press KEY0", COLOR_LIGHTGRAY, COLOR_BLACK, 1);
}

/* 绘制游戏场景 */
static void DrawGameScene(void) {
    uint8_t i;

    /* 背景 */
    LCD_FillRect(0, 80, LCD_WIDTH - 1, LCD_HEIGHT - 1, COLOR_DARKGREEN);

    /* 装饰: 草地纹理 */
    for (i = 0; i < LCD_WIDTH; i += 8) {
        LCD_DrawPixel(i, 80 + (i % 6), COLOR_GREEN);
    }

    /* 绘制所有洞口 */
    for (i = 0; i < GAME_ROWS * GAME_COLS; i++) {
        DrawHole(&g_game.holes[i]);
    }

    /* 底部信息 */
    if (g_game.combo >= 3) {
        char buf[20];
        sprintf(buf, "Combo x%lu!", g_game.combo);
        LCD_ShowString(160, LCD_HEIGHT - 30, buf, COLOR_ORANGE, COLOR_DARKGREEN, 2);
    }
}

/* ======================== 主渲染函数 ======================== */

void Game_Render(void) {
    if (g_game.state == GAME_STATE_IDLE) {
        DrawIdleScreen();
    } else if (g_game.state == GAME_STATE_OVER) {
        DrawGameOverScreen();
    } else {
        DrawGameScene();
    }

    /* 状态栏始终在最上层 */
    DrawHUD();
}