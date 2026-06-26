@echo off
chcp 65001 >nul
echo ========================================
echo   STM32F103C8T6 自平衡小车 - 固件编译
echo ========================================
echo.

REM 设置工具链路径（根据实际安装路径修改）
set TOOLCHAIN_PATH=D:\IST\STM32\STM32CubeIDE_2.2.0\STM32CubeIDE\plugins\com.st.stm32cube.ide.mcu.externaltools.gnu-tools-for-stm32.14.3.rel1.win32_1.0.100.202602081740\tools\bin
set PATH=%TOOLCHAIN_PATH%;%PATH%

REM 显示编译器信息
echo 编译器版本：
arm-none-eabi-gcc --version
echo.
if %errorlevel% neq 0 (
    echo [错误] 未找到 arm-none-eabi-gcc，请检查 TOOLCHAIN_PATH 设置。
    echo.
    echo 当前配置的路径：%TOOLCHAIN_PATH%
    echo.
    echo 请修改本脚本中的 TOOLCHAIN_PATH 为实际安装路径。
    pause
    exit /b 1
)

REM 编译
echo 开始编译...
make clean
make -j4 all

if %errorlevel% equ 0 (
    echo.
    echo ===== 编译成功 =====
    echo 输出文件：
    dir build\*.elf 2>nul
    dir build\*.hex 2>nul
    dir build\*.bin 2>nul
) else (
    echo.
    echo ===== 编译失败，请检查错误信息 =====
    pause
)