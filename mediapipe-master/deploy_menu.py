#!/usr/bin/env python3
"""
MediaPipe AI识别系统 - 部署选择菜单
选择最适合你的公网部署方案
"""

import os
import sys
import subprocess

def print_banner():
    print("🌍 MediaPipe AI识别系统 - 公网部署向导")
    print("=" * 60)
    print("让全世界都能访问你的AI识别系统！")
    print("=" * 60)

def print_options():
    print("\n📋 请选择部署方案:")
    print("1. 🚀 Vercel部署 (推荐)")
    print("   • 完全免费")
    print("   • 自动HTTPS")
    print("   • 全球CDN")
    print("   • 永久域名")
    print("   • 3分钟完成")
    print()
    print("2. 🔗 ngrok隧道")
    print("   • 快速测试")
    print("   • 临时地址")
    print("   • 需要保持运行")
    print("   • 1分钟完成")
    print()
    print("3. 📚 查看所有方案")
    print("   • 详细对比")
    print("   • 云服务器")
    print("   • GitHub Pages")
    print("   • 自定义域名")
    print()
    print("0. ❌ 退出")
    print("=" * 60)

def deploy_vercel():
    print("\n🚀 启动Vercel部署...")
    try:
        subprocess.run([sys.executable, "deploy_vercel.py"])
    except FileNotFoundError:
        print("❌ deploy_vercel.py 文件不存在")

def deploy_ngrok():
    print("\n🔗 启动ngrok隧道...")
    try:
        subprocess.run([sys.executable, "deploy_public.py"])
    except FileNotFoundError:
        print("❌ deploy_public.py 文件不存在")

def show_all_options():
    print("\n📚 所有部署方案详情:")
    print("=" * 60)
    
    print("🌟 方案对比:")
    print("┌─────────────┬─────────┬─────────┬─────────┬─────────┐")
    print("│    方案     │  成本   │  难度   │  速度   │ 推荐度  │")
    print("├─────────────┼─────────┼─────────┼─────────┼─────────┤")
    print("│ Vercel      │  免费   │   ⭐    │ ⭐⭐⭐⭐⭐ │ ⭐⭐⭐⭐⭐ │")
    print("│ ngrok       │  免费   │   ⭐    │ ⭐⭐⭐⭐  │ ⭐⭐⭐⭐  │")
    print("│ Netlify     │  免费   │  ⭐⭐   │ ⭐⭐⭐⭐⭐ │ ⭐⭐⭐⭐  │")
    print("│ GitHub Pages│  免费   │  ⭐⭐   │ ⭐⭐⭐   │ ⭐⭐⭐   │")
    print("│ 云服务器    │  付费   │ ⭐⭐⭐⭐ │ ⭐⭐⭐⭐⭐ │ ⭐⭐⭐   │")
    print("└─────────────┴─────────┴─────────┴─────────┴─────────┘")
    
    print("\n📖 详细说明:")
    print("• Vercel: 最推荐，免费HTTPS域名，全球CDN，自动部署")
    print("• ngrok: 快速测试，临时地址，需要保持电脑运行")
    print("• Netlify: 类似Vercel，功能丰富，适合静态网站")
    print("• GitHub Pages: 需要GitHub仓库，适合开源项目")
    print("• 云服务器: 最灵活，需要技术基础，适合商业项目")
    
    print("\n🔗 相关链接:")
    print("• Vercel: https://vercel.com")
    print("• ngrok: https://ngrok.com")
    print("• Netlify: https://netlify.com")
    print("• GitHub Pages: https://pages.github.com")
    
    print("\n📋 查看详细教程:")
    print("• 阅读 PUBLIC_DEPLOYMENT.md 文件")
    print("• 包含完整的部署步骤和故障排除")

def main():
    while True:
        print_banner()
        print_options()
        
        try:
            choice = input("请输入选项 (0-3): ").strip()
            
            if choice == "1":
                deploy_vercel()
                break
            elif choice == "2":
                deploy_ngrok()
                break
            elif choice == "3":
                show_all_options()
                input("\n按回车键返回主菜单...")
                os.system('cls' if os.name == 'nt' else 'clear')
            elif choice == "0":
                print("\n👋 感谢使用MediaPipe AI识别系统!")
                break
            else:
                print("❌ 无效选项，请重新选择")
                input("按回车键继续...")
                os.system('cls' if os.name == 'nt' else 'clear')
                
        except KeyboardInterrupt:
            print("\n\n👋 感谢使用MediaPipe AI识别系统!")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            input("按回车键继续...")

if __name__ == "__main__":
    main() 