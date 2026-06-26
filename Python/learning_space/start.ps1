# 个性化网络学习空间 · 一键启动脚本
# 用法：在本目录下 PowerShell 执行  .\start.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  个性化网络学习空间 · 一键启动" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$venvPython = "$PSScriptRoot\venv\Scripts\python.exe"
if (!(Test-Path $venvPython)) {
    Write-Host "[1] 创建虚拟环境..." -ForegroundColor Yellow
    python -m venv venv
    & .\venv\Scripts\python.exe -m pip install --upgrade pip
    & .\venv\Scripts\python.exe -m pip install -r requirements.txt
}

Write-Host "[2] 数据库迁移..." -ForegroundColor Yellow
& .\venv\Scripts\python.exe manage.py migrate --run-syncdb

Write-Host "[3] 导入种子数据..." -ForegroundColor Yellow
& .\venv\Scripts\python.exe manage.py shell -c "exec(open('seed.py', encoding='utf-8').read())"

Write-Host "[4] 启动 Django 后端 http://127.0.0.1:8000" -ForegroundColor Green
Start-Process -FilePath $venvPython -ArgumentList "manage.py runserver 0.0.0.0:8000" -WorkingDirectory $PSScriptRoot

Write-Host "[5] 启动前端静态服务器 http://127.0.0.1:8080" -ForegroundColor Green
Start-Process -FilePath $venvPython -ArgumentList "-m http.server 8080" -WorkingDirectory "$PSScriptRoot\frontend"

Write-Host ""
Write-Host "✅ 启动完成！浏览器打开 http://127.0.0.1:8080" -ForegroundColor Green
Write-Host ""
Write-Host "测试账号："
Write-Host "  学生 student  / student123" -ForegroundColor Blue
Write-Host "  教师 teacher  / teacher123" -ForegroundColor Blue
Write-Host "  管理员 admin  / admin123" -ForegroundColor Blue
Write-Host ""
Write-Host "API 文档：http://127.0.0.1:8000/api/docs/" -ForegroundColor Gray
