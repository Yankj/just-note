# 记一下 Web App

> 像发微信一样记录灵感，AI 自动帮你整理成知识库。

## 快速开始

### 前端开发

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 访问 http://localhost:3000
```

### 后端开发

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动 API 服务器
python app/main.py

# 访问 http://localhost:8000
```

## 项目结构

```
just-note-web/
├── frontend/              # React 前端
│   ├── src/
│   │   ├── components/   # 可复用组件
│   │   ├── pages/        # 页面组件
│   │   ├── stores/       # 状态管理 (Zustand)
│   │   ├── types/        # TypeScript 类型
│   │   └── utils/        # 工具函数
│   └── package.json
│
├── backend/              # FastAPI 后端
│   └── app/
│       ├── api/         # API 路由
│       ├── models/      # 数据模型
│       └── main.py      # 入口
│
└── docs/                # 文档
    └── PRODUCT-DESIGN.md
```

## 技术栈

**前端**:
- React 18 + TypeScript
- Vite (构建工具)
- Tailwind CSS (样式)
- Zustand (状态管理)
- React Router (路由)
- date-fns (日期处理)

**后端**:
- FastAPI (Python)
- Uvicorn (ASGI 服务器)
- Pydantic (数据验证)

## 功能特性

### MVP (v1.0)

- ✅ 快速记录（全局输入框）
- ✅ 笔记列表（时间线展示）
- ✅ 笔记详情（查看/编辑/删除）
- ✅ 类型筛选（9 种内容类型）
- ✅ 搜索功能
- ✅ 日记视图（按天聚合）
- ✅ 统计面板
- ⏳ AI 自动分类（待集成）
- ⏳ 导出功能（待实现）

## API 文档

启动后端后访问：http://localhost:8000/docs

### 主要端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/notes` | GET | 获取笔记列表 |
| `/api/notes` | POST | 创建笔记 |
| `/api/notes/:id` | GET | 获取笔记详情 |
| `/api/notes/:id` | PUT | 更新笔记 |
| `/api/notes/:id` | DELETE | 删除笔记 |
| `/api/notes/diary/:date` | GET | 获取日记视图 |
| `/api/notes/stats` | GET | 获取统计数据 |

## 部署

### 前端 (Vercel)

1. 推送代码到 GitHub
2. 在 Vercel 导入项目
3. 设置构建命令：`cd frontend && npm install && npm run build`
4. 设置输出目录：`frontend/dist`

### 后端 (云服务器)

```bash
# 安装依赖
pip install -r requirements.txt

# 使用 systemd 管理
sudo systemctl start just-note-api
sudo systemctl enable just-note-api
```

## 开发计划

- [ ] AI 自动分类集成
- [ ] 语义搜索
- [ ] 知识关联
- [ ] 导出功能 (Obsidian/Notion)
- [ ] PWA 支持
- [ ] 深色模式
- [ ] 多端同步

## 许可证

MIT

---

**记一下** · 让记录像呼吸一样自然
