#!/usr/bin/env python3
"""
自动下载并安装ngrok
"""

import os
import requests
import zipfile
import subprocess


def download_ngrok():
    """下载ngrok"""
    print("📦 正在下载ngrok...")
    
    # ngrok Windows下载链接
    url = ("https://bin.equinox.io/c/bNyj1mQVY4c/"
           "ngrok-v3-stable-windows-amd64.zip")
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # 保存到当前目录
        zip_path = "ngrok.zip"
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print("✅ ngrok下载完成!")
        return zip_path
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return None


def extract_ngrok(zip_path):
    """解压ngrok"""
    print("📂 正在解压ngrok...")
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(".")
        
        # 删除zip文件
        os.remove(zip_path)
        
        print("✅ ngrok解压完成!")
        return True
    except Exception as e:
        print(f"❌ 解压失败: {e}")
        return False


def test_ngrok():
    """测试ngrok是否可用"""
    try:
        result = subprocess.run(['./ngrok.exe', 'version'],
                                capture_output=True, text=True, cwd='.')
        if result.returncode == 0:
            print("✅ ngrok安装成功!")
            print(f"版本: {result.stdout.strip()}")
            return True
        else:
            print("❌ ngrok测试失败")
            return False
    except Exception as e:
        print(f"❌ ngrok测试失败: {e}")
        return False


def setup_ngrok():
    """设置ngrok"""
    print("\n🔑 ngrok设置:")
    print("1. 访问 https://dashboard.ngrok.com/signup 注册账号")
    print("2. 登录后访问 https://dashboard.ngrok.com/get-started/your-authtoken")
    print("3. 复制你的authtoken")
    print("4. 运行命令: ./ngrok.exe authtoken YOUR_TOKEN")
    print("\n💡 示例:")
    print("./ngrok.exe authtoken 2abc123def456ghi789jkl")


def main():
    print("🚀 ngrok自动安装程序")
    print("=" * 50)
    
    # 检查是否已经存在
    if os.path.exists("ngrok.exe"):
        print("✅ ngrok已存在!")
        if test_ngrok():
            setup_ngrok()
            return
    
    # 下载ngrok
    zip_path = download_ngrok()
    if not zip_path:
        return
    
    # 解压ngrok
    if not extract_ngrok(zip_path):
        return
    
    # 测试ngrok
    if test_ngrok():
        setup_ngrok()
        print("\n🎉 安装完成! 现在可以运行:")
        print("python deploy_public.py")


if __name__ == "__main__":
    main() 