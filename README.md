# OpenClaw Workspace

**注意**: 这个仓库包含两个分支：

## 分支说明

### `main` 分支 - 「记一下」Web App

**只包含**:
- ✅ `apps/just-note-web/` - 「记一下」Web App 完整代码
- ✅ `docs/` - 相关文档
- ✅ GitHub 配置文件

**快速开始**:
```bash
cd apps/just-note-web
./start-dev.sh
```

访问：http://localhost:3000

### `feature/full-workspace` 分支 - 完整 Workspace

**包含**:
- 📦 完整的 OpenClaw workspace
- 📦 所有 Skills (50+)
- 📦 Memory/笔记
- 📦 Agent 配置
- 📦 其他项目

**仅供备份和参考**

---

## 「记一下」Web App

> 像发微信一样记录灵感，AI 自动帮你整理成知识库。

### 功能特性

- ✅ 快速记录（9 种内容类型）
- ✅ 时间线展示
- ✅ 日记视图（按天聚合）
- ✅ 统计面板
- ✅ 搜索和筛选
- ✅ AI 自动分类（待集成）

### 技术栈

- **前端**: React 18 + TypeScript + Tailwind CSS
- **后端**: FastAPI (Python)
- **状态管理**: Zustand

### 开发

```bash
cd apps/just-note-web
./start-dev.sh
```

### 文档

- [产品设计](./apps/just-note-web/PRODUCT-DESIGN.md)
- [快速开始](./apps/just-note-web/QUICKSTART.md)
- [README](./apps/just-note-web/README.md)

---

## GitHub 分支

- **main**: 干净的 Web App 代码
- **feature/full-workspace**: 完整 workspace 备份

---

**记一下** · 让记录像呼吸一样自然
