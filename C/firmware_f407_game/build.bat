@echo off
REM =============================================================================
REM   STM32F407ZGT6 打地鼠游戏 - 构建脚本
REM   用法: 双击运行或在命令行中执行 build.bat
REM   前提: 已安装 arm-none-eabi-gcc 工具链并添加到 PATH
REM =============================================================================

echo.
echo ============================================
echo   Whack-a-Mole Game - Build Script
echo   STM32F407ZGT6 探索者 + 4.3寸触摸屏
echo ============================================
echo.

REM 检查工具链
where arm-none-eabi-gcc >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] arm-none-eabi-gcc not found in PATH!
    echo Please install ARM GCC toolchain:
    echo   https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain
    echo.
    pause
    exit /b 1
)

echo [INFO] ARM GCC toolchain found.
echo [INFO] Building...
echo.

REM 清理旧构建
if exist build rmdir /s /q build

REM 执行 Make
make -j4 all

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Build failed! Check errors above.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   Build SUCCESS!
echo.
echo   Output files in build\:
echo     whack_mole.elf  - ELF file (debug)
echo     whack_mole.hex  - Hex file (flash)
echo     whack_mole.bin  - Binary file (flash)
echo ============================================
echo.
echo To flash the firmware, use one of:
echo   1. STM32CubeProgrammer (GUI or CLI)
echo   2. ST-LINK Utility
echo   3. st-flash (open source)
echo ============================================
echo.
pause