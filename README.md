# HEIGO 足球经理联赛管理系统

⚽ **专业足球联赛管理平台 | 积分榜 | 比赛录入 | 赛程管理 | 交易系统中**

基于 FM26 联赛管理系统本地版设计的 Web 版本，支持完整的联赛管理功能！

## ✨ 核心功能

### 📊 联赛管理
- **积分榜** - 自动计算积分、排名（支持超级/甲级/乙级三级联赛）
- **赛程管理** - 联赛赛程、杯赛赛程
- **比赛录入** - 在线录入比赛结果，自动更新积分榜
- **球队管理** - 球队信息、教练信息

### 💰 交易系统
- **交易申请** - 提交球员交易申请
- **交易记录** - 查看历史交易
- **交易审核** - 管理员审核交易

### 🏆 荣誉系统
- **冠军荣誉榜** - 记录教练冠军数量
- **评级系统** - S/A/B/C 评级 + 星级

### 📢 公告系统
- **联赛公告** - 发布官方公告
- **置顶公告** - 重要公告置顶显示

## 🚀 一键部署

### 方式一：运行部署脚本

```bash
cd heigo-league-pro
chmod +x deploy.sh
./deploy.sh
```

选择部署方式：
1. **Railway** - 免费额度，自动部署
2. **Render** - 免费套餐
3. **Docker** - 自建服务器
4. **直接运行** - 传统部署

### 方式二：Railway 手动部署

1. 访问 https://railway.app/
2. 登录 GitHub
3. New Project → Deploy from GitHub repo
4. 选择 `heigo-league-pro` 仓库
5. 自动部署完成

### 方式三：Docker 部署

```bash
docker build -t heigo-league-pro .
docker run -d -p 5000:5000 \
  -e SECRET_KEY="your-secret-key" \
  -v $(pwd)/data:/app/instance \
  heigo-league-pro
```

访问：http://localhost:5000

### 方式四：直接运行

```bash
pip install -r requirements.txt
python run.py
```

访问：http://localhost:5000

## 📊 页面说明

| 页面 | 功能 | 说明 |
|------|------|------|
| 📊 积分榜 | 查看联赛排名 | 支持三级联赛切换 |
| 🏟️ 球队 | 球队列表 | 搜索、筛选功能 |
| ⚽ 比赛录入 | 录入比赛结果 | 自动更新积分榜 |
| 📅 赛程 | 查看赛程 | 按轮次筛选 |
| 💰 交易 | 交易申请 | 提交/查看交易 |
| 🏆 荣誉 | 冠军榜 | 教练荣誉排名 |
| ⚙️ 管理 | 系统设置 | 数据导入导出 |

## 📁 项目结构

```
heigo-league-pro/
├── app/
│   ├── __init__.py          # Flask 应用初始化
│   ├── models.py            # 数据模型
│   ├── routes.py            # API 路由
│   └── templates/           # HTML 模板
├── static/
│   ├── css/                 # 样式文件
│   └── js/                  # JavaScript 文件
├── index.html               # 主页面（单页应用）
├── deploy.sh                # 一键部署脚本
├── Dockerfile               # Docker 配置
├── docker-compose.yml       # Docker Compose
├── Procfile                 # Railway/Render 配置
├── railway.json             # Railway 配置
├── requirements.txt         # Python 依赖
├── run.py                   # 启动入口
└── README.md                # 本文件
```

## 🛠️ 技术栈

- **前端：** 原生 HTML/CSS/JavaScript（单页应用）
- **后端：** Flask + SQLAlchemy
- **数据库：** SQLite（开发）/ PostgreSQL（生产）
- **部署：** Railway / Render / Docker

## 🔧 API 接口

### 积分榜
```
GET /api/standings?level=超级
```

### 球队列表
```
GET /api/teams?level=甲级&search=关键词
```

### 比赛录入
```
POST /api/matches
{
  "round": 1,
  "home_team_id": 1,
  "away_team_id": 2,
  "home_score": 2,
  "away_score": 1,
  "match_date": "2024-01-01"
}
```

### 赛程
```
GET /api/schedule?round=1
```

### 交易申请
```
POST /api/transfers
{
  "player_name": "球员名",
  "position": "前锋",
  "from_team_id": 1,
  "to_team_id": 2,
  "transfer_type": "买卖",
  "amount": 10000000
}
```

## 📝 使用说明

### 1. 创建球队
在管理后台添加球队和教练信息。

### 2. 录入赛程
创建联赛赛程（可批量生成）。

### 3. 录入比赛
比赛结束后，在"比赛录入"页面填写比分。

### 4. 查看积分榜
积分榜自动根据比赛结果更新。

### 5. 提交交易
在"交易"页面提交球员交易申请。

## 🔐 默认管理员

- **用户名：** `admin`
- **密码：** `admin123`

⚠️ **首次登录后请立即修改密码！**

## 📊 积分规则

- 胜：3 分
- 平：1 分
- 负：0 分

排名优先级：
1. 积分
2. 净胜球
3. 进球数
4. 相互战绩

## 🎨 主题配色

- 主色调：深色科技风（#0f0f23）
- 强调色：青色（#00d4aa）
- 成功：绿色（#00ff88）
- 警告：橙色（#ffaa00）
- 危险：红色（#ff4466）

## 📝 更新日志

### v1.0 - 2026-04-10
- ✨ 初始版本发布
- ✨ 积分榜系统
- ✨ 比赛录入系统
- ✨ 赛程管理系统
- ✨ 交易系统
- ✨ 荣誉系统
- ✨ 一键部署脚本

---

## 🙏 致谢

灵感来源于 FM26 联赛管理系统本地版

**祝你使用愉快！** ⚽🎉
