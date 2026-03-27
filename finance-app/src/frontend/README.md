# 财务自由管理系统 - 前端

基于 React + Vite + TypeScript + Ant Design 构建的财务自由管理前端应用。

## 技术栈

- **框架**: React 18 + TypeScript
- **构建工具**: Vite 5
- **UI 组件库**: Ant Design 5
- **路由**: React Router v7
- **HTTP 客户端**: Axios
- **样式**: TailwindCSS

## 功能模块

1. **财务自由规划** - 财务目标设定、进度追踪、里程碑管理
2. **投资日记** - 交易记录、情绪分析、复盘总结
3. **心理诊断** - 交易心理评估、贪婪/恐惧指数、改进建议
4. **资产视图** - 资产配置、净值追踪、收益分析
5. **被动收入** - 收入来源管理、增长追踪、财务自由进度
6. **AI 对话** - 智能财务助手、投资咨询、市场分析

## 快速开始

### 安装依赖

```bash
npm install
```

### 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

### 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:3000

### 构建生产版本

```bash
npm run build
```

### 预览生产构建

```bash
npm run preview
```

## 项目结构

```
src/
├── api/              # API 调用层
│   ├── axios.ts      # Axios 配置
│   └── index.ts      # API 接口定义
├── pages/            # 页面组件
│   ├── FinancialPlanning.tsx
│   ├── InvestmentDiary.tsx
│   ├── PsychologyAssessment.tsx
│   ├── AssetsOverview.tsx
│   ├── PassiveIncome.tsx
│   └── AIChat.tsx
├── App.tsx           # 主应用组件（路由配置）
├── main.tsx          # 入口文件
└── index.css         # 全局样式
```

## API 配置

默认 API 地址：`http://localhost:8000/api`

可在 `.env` 文件中修改 `VITE_API_BASE_URL`。

## 开发规范

- 使用 TypeScript 严格模式
- 组件采用函数式 + Hooks
- 使用 Ant Design 组件库
- 使用 TailwindCSS 进行样式定制
- 遵循 ESLint 规则
