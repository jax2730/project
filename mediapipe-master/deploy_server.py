#!/usr/bin/env python3
"""
简单的HTTP服务器用于发布MediaPipe AI识别系统
支持静态文件服务和CORS
"""

import http.server
import socketserver
import os
import sys
import socket
from urllib.parse import urlparse

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """支持CORS的HTTP请求处理器"""
    
    def end_headers(self):
        # 添加CORS头
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()
    
    def do_OPTIONS(self):
        """处理OPTIONS请求"""
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{self.log_date_time_string()}] {format % args}")

def get_local_ip():
    """获取本地IP地址"""
    try:
        # 连接到一个远程地址来获取本地IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def main():
    # 配置
    PORT = 8080
    DIRECTORY = "frontend/dist"
    
    # 检查目录是否存在
    if not os.path.exists(DIRECTORY):
        print(f"❌ 错误: 目录 '{DIRECTORY}' 不存在")
        print("请先运行 'cd frontend && npm run build' 来构建项目")
        sys.exit(1)
    
    # 切换到目标目录
    os.chdir(DIRECTORY)
    
    # 获取IP地址
    local_ip = get_local_ip()
    
    # 创建服务器
    with socketserver.TCPServer(("", PORT), CORSHTTPRequestHandler) as httpd:
        print("🚀 MediaPipe AI识别系统 - Web服务器启动成功!")
        print("=" * 60)
        print(f"📁 服务目录: {os.path.abspath('.')}")
        print(f"🌐 本地访问: http://localhost:{PORT}")
        print(f"🌍 网络访问: http://{local_ip}:{PORT}")
        print("=" * 60)
        print("💡 提示:")
        print("  - 在同一网络的其他设备可通过网络IP访问")
        print("  - 按 Ctrl+C 停止服务器")
        print("=" * 60)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 服务器已停止")
            print("感谢使用 MediaPipe AI识别系统!")

if __name__ == "__main__":
    main() 