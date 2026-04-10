#!/bin/bash

echo "🚀 HEIGO 联赛管理系统 - 一键部署"
echo "================================"
echo ""
echo "请选择部署方式："
echo "1. Railway (推荐 - 免费额度)"
echo "2. Render (免费套餐)"
echo "3. Docker (自建服务器)"
echo "4. 直接运行 (本地测试)"
echo ""
read -p "请输入选项 (1-4): " choice

case $choice in
    1)
        echo ""
        echo "📦 部署到 Railway..."
        echo ""
        echo "步骤："
        echo "1. 访问 https://railway.app/"
        echo "2. 登录 GitHub"
        echo "3. New Project → Deploy from GitHub repo"
        echo "4. 选择你的 heigo-league-pro 仓库"
        echo ""
        echo "✅ 部署完成后访问：https://your-project.up.railway.app"
        echo "🔐 默认账号：admin / admin123"
        ;;
    
    2)
        echo ""
        echo "📦 部署到 Render..."
        echo ""
        echo "步骤："
        echo "1. 访问 https://render.com/"
        echo "2. 登录 → New + → Web Service"
        echo "3. 连接 GitHub 并选择仓库"
        echo "4. 自动识别配置"
        echo ""
        echo "✅ 部署完成后访问你的 render 域名"
        echo "🔐 默认账号：admin / admin123"
        ;;
    
    3)
        echo ""
        echo "📦 Docker 部署..."
        echo ""
        
        if ! command -v docker &> /dev/null; then
            echo "❌ 未检测到 Docker，请先安装 Docker"
            exit 1
        fi
        
        echo "🔨 构建 Docker 镜像..."
        docker build -t heigo-league-pro .
        
        echo "🏃 启动容器..."
        docker run -d \
            --name heigo-league-pro \
            -p 5000:5000 \
            -e SECRET_KEY="your-secret-key-$(openssl rand -hex 16)" \
            -v $(pwd)/data:/app/instance \
            heigo-league-pro
        
        echo ""
        echo "✅ 部署完成！"
        echo "🌐 访问地址：http://localhost:5000"
        echo "🔐 默认账号：admin / admin123"
        ;;
    
    4)
        echo ""
        echo "📦 直接运行..."
        echo ""
        
        if ! command -v python3 &> /dev/null; then
            echo "❌ 未检测到 Python3"
            exit 1
        fi
        
        echo "📦 安装依赖..."
        pip3 install -r requirements.txt
        
        echo ""
        echo "🏃 启动应用..."
        echo "按 Ctrl+C 停止"
        python3 run.py
        ;;
    
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac

echo ""
echo "================================"
echo "🎉 部署完成！祝你使用愉快！⚽"
