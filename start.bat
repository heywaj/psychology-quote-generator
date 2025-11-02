@echo off
chcp 65001 >nul
title 🎨 自动化心理语录图片生成器

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                  🎨 自动化心理语录图片生成器                    ║
echo ║                   一键启动 - Windows版本                     ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: 检查虚拟环境
if not exist ".venv\Scripts\python.exe" (
    echo ❌ 未找到虚拟环境，正在创建...
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ 创建虚拟环境失败，请确保已安装Python 3.9+
        pause
        exit /b 1
    )
    echo ✅ 虚拟环境创建成功
)

:: 运行入口程序
echo 🚀 正在启动程序...
echo.
".venv\Scripts\python.exe" run.py

echo.
echo 👋 程序已退出
pause