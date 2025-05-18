@echo off
chcp 65001
echo 启动图像处理系统...

REM 启动后端 Flask 服务器
start cmd /k "chcp 65001 && python app.py"

REM 等待2秒，确保后端先启动
timeout /t 2

REM 启动前端 Vue 开发服务器
start cmd /k "chcp 65001 && cd frontend && npm run serve"

echo 系统已启动！
echo 前端地址: http://localhost:8080
echo 后端地址: http://localhost:5000

pause 