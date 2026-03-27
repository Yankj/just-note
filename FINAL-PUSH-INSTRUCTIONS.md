# 🚀 GitHub 推送说明 - 最终版

**准备就绪**: 两个分支已本地创建完成

---

## 分支说明

### 1. `feature/full-workspace` 分支
**内容**: 完整的 OpenClaw workspace（包含所有 Skills、Memory、Agents 等）
**用途**: 备份和参考

### 2. `main` 分支
**内容**: 只包含「记一下」Web App
**用途**: 主要开发分支，干净的代码

---

## 推送步骤

### 方式一：使用推送脚本（推荐）

```bash
cd ~/openclaw/workspace

# 执行推送脚本
./PUSH-TO-GITHUB.sh
```

**需要认证**:
- 用户名：`Yankj`
- 密码：使用**新的** Personal Access Token

脚本会：
1. ✅ 推送 `feature/full-workspace` 分支（完整代码）
2. ✅ 推送 `main` 分支（干净的 Web App）

---

### 方式二：手动推送

```bash
cd ~/openclaw/workspace

# 1. 推送完整代码到 feature 分支
git checkout feature/full-workspace
git push -u origin feature/full-workspace

# 2. 推送干净代码到 main 分支
git checkout main
git push -u origin main
```

---

## 推送后验证

访问：https://github.com/Yankj/just-note

### 查看 main 分支

应该只看到：
- ✅ `apps/just-note-web/` - Web App 代码
- ✅ `docs/` - 文档
- ✅ `README.md` - 项目说明
- ✅ `PUSH-TO-GITHUB.sh` - 推送脚本

**不应该看到**:
- ❌ `.openclaw/`
- ❌ `skills/`
- ❌ `memory/`
- ❌ `agents/`
- ❌ `*.skill`

### 查看 feature/full-workspace 分支

应该看到完整的 workspace：
- ✅ 所有文件（包括 Skills、Memory 等）

---

## 切换分支查看

在 GitHub 仓库页面：
1. 点击分支选择器（默认显示 `main`）
2. 选择 `feature/full-workspace` 查看完整代码
3. 选择 `main` 查看干净的 Web App

---

## 安全提醒

⚠️ **请使用新的 Personal Access Token**

旧的 Token (`ghp_wd5i0gg...`) 已经暴露，建议：
1. 访问：https://github.com/settings/tokens
2. 删除旧 Token
3. 生成新 Token（勾选 `repo` 权限）
4. 使用新 Token 推送

---

## 推送完成后

### 克隆仓库（其他人）

```bash
# 克隆 main 分支（默认）
git clone https://github.com/Yankj/just-note.git

# 或克隆完整 workspace
git clone -b feature/full-workspace https://github.com/Yankj/just-note.git
```

### 后续开发

```bash
# 在 main 分支开发
git checkout main
# ... 写代码 ...
git add -A
git commit -m "feat: 新功能"
git push
```

---

**准备好后执行推送脚本即可！** 🚀

```bash
./PUSH-TO-GITHUB.sh
```
