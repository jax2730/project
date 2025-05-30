@echo off
chcp 65001 >nul
title MediaPipe AI识别系统 - 网站启动器

echo.
echo ========================================
echo    MediaPipe AI识别系统
echo    一键启动Web服务器
echo ========================================
echo.

cd /d "%~dp0"
python start_website.py

pause 