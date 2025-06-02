#!/usr/bin/env python3
"""
ngrok设置助手
"""

import webbrowser
import subprocess


def main():
    print("🔑 ngrok设置助手")
    print("=" * 50)
    
    print("步骤 1: 注册ngrok账号")
    print("即将打开ngrok注册页面...")
    input("按回车键继续...")
    webbrowser.open("https://dashboard.ngrok.com/signup")
    
    print("\n步骤 2: 获取authtoken")
    print("注册并登录后，即将打开authtoken页面...")
    input("按回车键继续...")
    webbrowser.open("https://dashboard.ngrok.com/get-started/your-authtoken")
    
    print("\n步骤 3: 设置authtoken")
    print("请从网页上复制你的authtoken，然后粘贴到下面:")
    authtoken = input("authtoken: ").strip()
    
    if authtoken:
        print("\n正在设置authtoken...")
        try:
            result = subprocess.run(['./ngrok.exe', 'authtoken', authtoken],
                                    capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ authtoken设置成功!")
                print("\n🎉 ngrok设置完成!")
                print("现在可以运行: python deploy_public.py")
            else:
                print(f"❌ 设置失败: {result.stderr}")
        except Exception as e:
            print(f"❌ 设置失败: {e}")
    else:
        print("❌ 未输入authtoken")


if __name__ == "__main__":
    main() 