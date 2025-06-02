#!/usr/bin/env python3
"""
MediaPipe AI识别系统 - 网站启动器
一键启动Web服务器并自动打开浏览器
"""

import http.server
import socketserver
import os
import sys
import webbrowser
import socket
import threading
import time

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def log_message(self, format, *args):
        print(f"[访问] {format % args}")

def get_local_ip():
    """获取本地IP地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def check_port(port):
    """检查端口是否可用"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result != 0

def main():
    PORT = 8080
    DIST_DIR = "frontend/dist"
    
    print("🚀 启动 MediaPipe AI识别系统...")
    print("=" * 60)
    
    # 检查构建文件
    if not os.path.exists(DIST_DIR):
        print("📦 构建文件不存在，开始构建前端...")
        os.chdir("frontend")
        os.system("npm run build")
        os.chdir("..")
        print("✅ 前端构建完成!")
    
    # 检查端口
    if not check_port(PORT):
        print(f"❌ 端口 {PORT} 已被占用，请关闭其他服务或更改端口")
        return
    
    # 切换到构建目录
    os.chdir(DIST_DIR)
    
    # 获取IP地址
    local_ip = get_local_ip()
    
    print("🌐 服务器信息:")
    print(f"   📁 服务目录: {os.path.abspath('.')}")
    print(f"   🏠 本地访问: http://localhost:{PORT}")
    print(f"   🌍 网络访问: http://{local_ip}:{PORT}")
    print("=" * 60)
    print("🎯 功能特性:")
    print("   • 实时点云数据可视化")
    print("   • AI目标检测与识别")
    print("   • 算法参数配置管理")
    print("   • 存储与模型管理")
    print("=" * 60)
    print("💡 使用提示:")
    print("   • 浏览器将自动打开网站")
    print("   • 同网络设备可通过网络IP访问")
    print("   • 按 Ctrl+C 停止服务器")
    print("=" * 60)
    
    # 启动服务器
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            # 延迟打开浏览器
            def open_browser():
                time.sleep(2)
                webbrowser.open(f"http://localhost:{PORT}")
            
            threading.Thread(target=open_browser, daemon=True).start()
            
            print("✅ 服务器启动成功! 正在打开浏览器...")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n🛑 服务器已停止")
        print("感谢使用 MediaPipe AI识别系统!")
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")

if __name__ == "__main__":
    main() 