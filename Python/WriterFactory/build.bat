@echo off
chcp 65001 >nul
setlocal

echo ============================================
echo    作家工厂 WriterFactory  -  一键打包
echo ============================================
echo.

echo [1/3] 安装/检查依赖...
python -m pip install -r requirements-desktop.txt
if errorlevel 1 goto :error

echo.
echo [2/3] 收集静态文件 collectstatic...
python manage.py collectstatic --noinput
if errorlevel 1 goto :error

echo.
echo [3/3] PyInstaller 打包中（约需 1-3 分钟）...
python -m PyInstaller WriterFactory.spec --clean --noconfirm
if errorlevel 1 goto :error

echo.
echo ============================================
echo   打包完成！
echo   可执行文件: dist\WriterFactory\WriterFactory.exe
echo   用户数据目录: %%LOCALAPPDATA%%\WriterFactory
echo ============================================
pause
exit /b 0

:error
echo.
echo [错误] 打包失败，请检查上方日志。
pause
exit /b 1
