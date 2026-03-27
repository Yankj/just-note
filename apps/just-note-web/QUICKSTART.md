# 记一下 Web App - 快速启动指南

**5 分钟启动开发环境！**

---

## 方式一：使用启动脚本（推荐）

```bash
cd ~/openclaw/workspace/apps/just-note-web

# 一键启动（前端 + 后端）
./start-dev.sh
```

---

## 方式二：手动启动

### 1. 启动后端

```bash
cd ~/openclaw/workspace/apps/just-note-web/backend

# 创建虚拟环境（首次）
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖（首次）
pip install -r requirements.txt

# 启动 API 服务器
python app/main.py
```

后端将在 http://localhost:8000 运行
API 文档：http://localhost:8000/docs

### 2. 启动前端（新终端）

```bash
cd ~/openclaw/workspace/apps/just-note-web/frontend

# 安装依赖（首次）
npm install

# 启动开发服务器
npm run dev
```

前端将在 http://localhost:3000 运行

---

## 测试功能

### 1. 访问应用

打开浏览器访问：http://localhost:3000

### 2. 记录第一条笔记

1. 在首页输入框输入内容
2. 选择类型（灵感/想法/知识等）
3. 点击"记录"按钮
4. 笔记将显示在列表中

### 3. 查看功能

- **首页** - 快速记录和最近笔记
- **全部记录** - 浏览和筛选所有笔记
- **日记视图** - 按天聚合查看
- **统计** - 查看使用数据

---

## 常见问题

### Q: npm install 失败？

```bash
# 清除缓存重试
npm cache clean --force
npm install

# 或使用淘宝镜像
npm config set registry https://registry.npmmirror.com
npm install
```

### Q: Python 依赖安装失败？

```bash
# 升级 pip
pip install --upgrade pip

# 或使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q: 端口被占用？

```bash
# 查看占用端口的进程
lsof -i :3000  # 前端
lsof -i :8000  # 后端

# 杀死进程
kill -9 <PID>
```

---

## 下一步

1. **体验核心功能** - 记录、查看、编辑笔记
2. **查看设计文档** - `PRODUCT-DESIGN.md`
3. **开始开发** - 添加新功能或优化体验

---

## 项目结构

```
just-note-web/
├── frontend/           # React 前端 (http://localhost:3000)
│   ├── src/
│   │   ├── pages/     # 页面组件
│   │   ├── components/# 可复用组件
│   │   └── stores/    # 状态管理
│   └── package.json
│
├── backend/           # FastAPI 后端 (http://localhost:8000)
│   └── app/
│       └── main.py    # API 入口
│
└── docs/             # 文档
    └── PRODUCT-DESIGN.md
```

---

## 技术栈

- **前端**: React 18 + TypeScript + Tailwind CSS
- **后端**: FastAPI (Python)
- **状态管理**: Zustand
- **路由**: React Router v6
- **日期处理**: date-fns

---

**遇到问题？** 查看 `README.md` 或提交 Issue。

> **记一下** · 让记录像呼吸一样自然
