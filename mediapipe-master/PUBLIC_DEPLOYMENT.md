# 🌍 MediaPipe AI 识别系统 - 公网部署指南

## 📋 概述

将你的 MediaPipe AI 识别系统部署到公网，让全世界的人都能访问！

## 🚀 方案 1: ngrok 隧道（推荐，最简单）

### 步骤 1: 安装 ngrok

```bash
# 方法1: 官网下载
# 访问 https://ngrok.com/download
# 下载适合你系统的版本并解压

# 方法2: 包管理器安装
# Windows (需要Chocolatey)
choco install ngrok

# macOS (需要Homebrew)
brew install ngrok

# Linux
snap install ngrok
```

### 步骤 2: 注册并配置

```bash
# 1. 注册ngrok账号: https://dashboard.ngrok.com/signup
# 2. 获取authtoken
# 3. 配置token
ngrok authtoken YOUR_AUTH_TOKEN
```

### 步骤 3: 一键部署

```bash
python deploy_public.py
```

### 🎉 完成！

- 脚本会自动启动本地服务器
- 自动创建 ngrok 隧道
- 获得类似 `https://abc123.ngrok.io` 的公网地址
- 全世界任何人都可以访问！

---

## 🌐 方案 2: 云服务器部署

### 2.1 使用 Vercel（免费）

```bash
# 1. 安装Vercel CLI
npm install -g vercel

# 2. 构建项目
cd frontend && npm run build

# 3. 部署
cd dist && vercel --prod
```

### 2.2 使用 Netlify（免费）

```bash
# 1. 安装Netlify CLI
npm install -g netlify-cli

# 2. 构建项目
cd frontend && npm run build

# 3. 部署
cd dist && netlify deploy --prod
```

### 2.3 使用 GitHub Pages（免费）

```bash
# 1. 推送代码到GitHub
git add .
git commit -m "Deploy MediaPipe AI System"
git push origin main

# 2. 在GitHub仓库设置中启用Pages
# 3. 选择dist目录作为源
```

---

## ☁️ 方案 3: 云服务器（VPS）

### 3.1 购买云服务器

推荐服务商：

- **阿里云 ECS** (中国用户)
- **腾讯云 CVM** (中国用户)
- **AWS EC2** (国际用户)
- **DigitalOcean** (国际用户)
- **Vultr** (性价比高)

### 3.2 服务器配置

```bash
# 最低配置
CPU: 1核
内存: 1GB
存储: 20GB SSD
带宽: 1Mbps

# 推荐配置
CPU: 2核
内存: 4GB
存储: 40GB SSD
带宽: 5Mbps
```

### 3.3 部署步骤

```bash
# 1. 连接服务器
ssh root@your-server-ip

# 2. 安装依赖
apt update
apt install python3 python3-pip nodejs npm nginx

# 3. 上传项目文件
scp -r mediapipe-master root@your-server-ip:/var/www/

# 4. 构建项目
cd /var/www/mediapipe-master/frontend
npm install
npm run build

# 5. 配置Nginx
nano /etc/nginx/sites-available/mediapipe
```

### 3.4 Nginx 配置文件

```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /var/www/mediapipe-master/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🔒 方案 4: 内网穿透工具对比

| 工具       | 免费额度  | 稳定性     | 速度       | 自定义域名 |
| ---------- | --------- | ---------- | ---------- | ---------- |
| **ngrok**  | 1 个隧道  | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐   | 付费       |
| **frp**    | 无限制    | ⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐ | 支持       |
| **natapp** | 2 小时/天 | ⭐⭐⭐     | ⭐⭐⭐     | 付费       |
| **花生壳** | 1GB/月    | ⭐⭐⭐     | ⭐⭐       | 付费       |

---

## 🛠️ 快速部署脚本

### 一键 ngrok 部署

```bash
# 停止占用端口的进程
taskkill /f /im python.exe

# 启动公网部署
python deploy_public.py
```

### 一键云部署（Vercel）

```bash
# 构建并部署到Vercel
cd frontend
npm run build
cd dist
vercel --prod
```

---

## 📊 部署方案对比

| 方案             | 成本 | 难度     | 速度       | 稳定性     | 推荐度     |
| ---------------- | ---- | -------- | ---------- | ---------- | ---------- |
| **ngrok**        | 免费 | ⭐       | ⭐⭐⭐⭐   | ⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐ |
| **Vercel**       | 免费 | ⭐⭐     | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐   |
| **云服务器**     | 付费 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐     |
| **GitHub Pages** | 免费 | ⭐⭐     | ⭐⭐⭐     | ⭐⭐⭐⭐   | ⭐⭐⭐     |

---

## 🎯 推荐部署流程

### 新手用户（5 分钟）

1. 下载安装 ngrok
2. 注册获取 token
3. 运行 `python deploy_public.py`
4. 分享生成的公网地址

### 进阶用户（30 分钟）

1. 注册 Vercel 账号
2. 连接 GitHub 仓库
3. 自动部署获得永久域名
4. 配置自定义域名

### 专业用户（2 小时）

1. 购买云服务器
2. 配置域名解析
3. 部署完整环境
4. 配置 HTTPS 证书

---

## 🔧 故障排除

### ngrok 常见问题

```bash
# 问题1: ngrok command not found
# 解决: 将ngrok.exe添加到PATH环境变量

# 问题2: tunnel session failed
# 解决: 检查authtoken是否正确配置

# 问题3: 连接超时
# 解决: 检查防火墙设置，开放8080端口
```

### 云部署常见问题

```bash
# 问题1: 构建失败
# 解决: 检查Node.js版本，推荐使用v16+

# 问题2: 静态资源404
# 解决: 检查publicPath配置

# 问题3: 路由404
# 解决: 配置fallback到index.html
```

---

## 📞 技术支持

### 获取帮助

- **ngrok 文档**: https://ngrok.com/docs
- **Vercel 文档**: https://vercel.com/docs
- **云服务器教程**: 各大云厂商官方文档

### 联系方式

- 遇到问题可以查看日志文件
- 检查网络连接和防火墙设置
- 确保所有依赖正确安装

---

## 🎉 部署成功！

恭喜！你的 MediaPipe AI 识别系统现在可以被全世界访问了！

**分享你的网站地址，让更多人体验强大的 AI 识别功能！**

🌍 **公网地址示例**:

- ngrok: `https://abc123.ngrok.io`
- Vercel: `https://your-project.vercel.app`
- 自定义域名: `https://your-domain.com`
