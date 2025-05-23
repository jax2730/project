#!/usr/bin/env python3
"""
MediaPipe AI识别系统 - 公网部署
使用ngrok将本地服务器暴露到公网
"""

import http.server
import socketserver
import os
import sys
import subprocess
import threading
import time
import json
import requests
import webbrowser

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def log_message(self, format, *args):
        print(f"[访问] {format % args}")

def check_ngrok():
    """检查ngrok是否安装"""
    try:
        result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_ngrok():
    """安装ngrok的说明"""
    print("📦 ngrok未安装，请按以下步骤安装:")
    print("=" * 60)
    print("1. 访问 https://ngrok.com/download")
    print("2. 下载适合你系统的版本")
    print("3. 解压到任意目录")
    print("4. 将ngrok.exe添加到系统PATH环境变量")
    print("5. 注册ngrok账号并获取authtoken")
    print("6. 运行: ngrok authtoken YOUR_TOKEN")
    print("=" * 60)
    print("或者使用以下快速安装方法:")
    print("Windows: choco install ngrok")
    print("macOS: brew install ngrok")
    print("Linux: snap install ngrok")
    return False

def get_ngrok_url():
    """获取ngrok公网URL"""
    try:
        response = requests.get('http://localhost:4040/api/tunnels')
        tunnels = response.json()['tunnels']
        for tunnel in tunnels:
            if tunnel['config']['addr'] == 'http://localhost:8080':
                return tunnel['public_url']
    except:
        pass
    return None

def start_ngrok():
    """启动ngrok隧道"""
    try:
        # 启动ngrok
        ngrok_process = subprocess.Popen(
            ['ngrok', 'http', '8080'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # 等待ngrok启动
        time.sleep(3)
        
        # 获取公网URL
        public_url = get_ngrok_url()
        if public_url:
            return ngrok_process, public_url
        else:
            ngrok_process.terminate()
            return None, None
    except Exception as e:
        print(f"❌ 启动ngrok失败: {e}")
        return None, None

def main():
    PORT = 8080
    DIST_DIR = "frontend/dist"
    
    print("🌍 MediaPipe AI识别系统 - 公网部署")
    print("=" * 60)
    
    # 检查ngrok
    if not check_ngrok():
        install_ngrok()
        return
    
    # 检查构建文件
    if not os.path.exists(DIST_DIR):
        print("📦 构建文件不存在，开始构建前端...")
        os.chdir("frontend")
        os.system("npm run build")
        os.chdir("..")
        print("✅ 前端构建完成!")
    
    # 切换到构建目录
    os.chdir(DIST_DIR)
    
    print("🚀 启动本地服务器...")
    
    # 启动HTTP服务器
    def start_server():
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            httpd.serve_forever()
    
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # 等待服务器启动
    time.sleep(2)
    
    print("🌐 启动ngrok隧道...")
    ngrok_process, public_url = start_ngrok()
    
    if public_url:
        print("✅ 公网部署成功!")
        print("=" * 60)
        print(f"🌍 公网访问地址: {public_url}")
        print(f"🏠 本地访问地址: http://localhost:{PORT}")
        print("=" * 60)
        print("🎯 功能特性:")
        print("   • 全球任何人都可以访问")
        print("   • 实时点云数据可视化")
        print("   • AI目标检测与识别")
        print("   • 算法参数配置管理")
        print("=" * 60)
        print("💡 使用提示:")
        print("   • 分享公网地址给其他人访问")
        print("   • ngrok免费版有连接数限制")
        print("   • 按 Ctrl+C 停止服务")
        print("=" * 60)
        
        # 自动打开浏览器
        webbrowser.open(public_url)
        
        try:
            # 保持运行
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 正在停止服务...")
            if ngrok_process:
                ngrok_process.terminate()
            print("感谢使用 MediaPipe AI识别系统!")
    else:
        print("❌ 无法获取ngrok公网地址")
        print("请检查ngrok配置或网络连接")

if __name__ == "__main__":
    main() 