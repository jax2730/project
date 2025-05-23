#!/usr/bin/env python3
"""
MediaPipe AI识别系统 - Vercel一键部署
免费获得全球访问的HTTPS网站
"""

import os
import subprocess
import sys
import webbrowser
import time

def check_node():
    """检查Node.js是否安装"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def check_vercel():
    """检查Vercel CLI是否安装"""
    try:
        result = subprocess.run(['vercel', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_vercel():
    """安装Vercel CLI"""
    print("📦 正在安装Vercel CLI...")
    try:
        subprocess.run(['npm', 'install', '-g', 'vercel'], check=True)
        return True
    except subprocess.CalledProcessError:
        print("❌ 安装Vercel CLI失败")
        return False

def build_project():
    """构建项目"""
    print("🔨 正在构建前端项目...")
    try:
        os.chdir("frontend")
        subprocess.run(['npm', 'install'], check=True)
        subprocess.run(['npm', 'run', 'build'], check=True)
        os.chdir("..")
        return True
    except subprocess.CalledProcessError:
        print("❌ 构建项目失败")
        return False

def deploy_to_vercel():
    """部署到Vercel"""
    print("🚀 正在部署到Vercel...")
    try:
        os.chdir("frontend/dist")
        result = subprocess.run(['vercel', '--prod', '--yes'], 
                              capture_output=True, text=True)
        os.chdir("../..")
        
        if result.returncode == 0:
            # 从输出中提取URL
            output = result.stdout
            lines = output.split('\n')
            for line in lines:
                if 'https://' in line and 'vercel.app' in line:
                    return line.strip()
        return None
    except subprocess.CalledProcessError:
        print("❌ 部署失败")
        return None

def main():
    print("🌍 MediaPipe AI识别系统 - Vercel公网部署")
    print("=" * 60)
    print("🎯 目标: 获得免费的全球HTTPS网站")
    print("⏱️  预计时间: 3-5分钟")
    print("=" * 60)
    
    # 检查Node.js
    if not check_node():
        print("❌ 请先安装Node.js: https://nodejs.org/")
        return
    
    # 检查并安装Vercel CLI
    if not check_vercel():
        if not install_vercel():
            return
    
    # 构建项目
    if not build_project():
        return
    
    # 部署到Vercel
    print("🌐 开始部署到Vercel...")
    print("💡 首次使用需要登录Vercel账号")
    
    url = deploy_to_vercel()
    
    if url:
        print("✅ 部署成功!")
        print("=" * 60)
        print(f"🌍 公网地址: {url}")
        print("🔒 自动HTTPS加密")
        print("⚡ 全球CDN加速")
        print("🆓 完全免费")
        print("=" * 60)
        print("🎉 你的网站现在可以被全世界访问!")
        print("📤 分享这个地址给任何人")
        print("=" * 60)
        
        # 自动打开浏览器
        webbrowser.open(url)
        
        # 保存URL到文件
        with open("public_url.txt", "w") as f:
            f.write(f"MediaPipe AI识别系统公网地址:\n{url}\n")
        
        print("💾 公网地址已保存到 public_url.txt")
        
    else:
        print("❌ 部署失败，请检查网络连接或Vercel配置")

if __name__ == "__main__":
    main() 