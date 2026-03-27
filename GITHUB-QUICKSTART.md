# 🚀 GitHub 自动提交 - 快速开始

**3 步完成配置，让 AI 自动写代码并提交！**

---

## 步骤 1: 创建 GitHub 仓库

1. 访问 https://github.com/new
2. 创建新仓库（名称如：`openclaw-workspace`）
3. **不要**勾选"Initialize this repository with a README"
4. 复制仓库地址，例如：`https://github.com/yourname/openclaw-workspace.git`

---

## 步骤 2: 添加远程仓库并推送

```bash
# 进入工作区
cd ~/openclaw/workspace

# 添加远程仓库（替换为你的地址）
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# 首次推送
git branch -M main
git push -u origin main
```

**需要认证？** 选择以下任一方式：

### 方式 A: GitHub CLI（推荐）

```bash
# 安装
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh -y

# 登录
gh auth login
# 选择 GitHub.com → HTTPS → Login with a web browser
```

### 方式 B: Personal Access Token

1. 访问 https://github.com/settings/tokens
2. 生成新 Token（经典），勾选 `repo` 权限
3. 复制 Token
4. 使用 Token 推送：
```bash
git push -u origin main
# 输入用户名和 Token（作为密码）
```

---

## 步骤 3: 开始使用！

### 让 AI 写代码并提交

**告诉 AI**:
- "帮我写一个计算器组件，写完后提交到 GitHub"
- "提交所有变更并推送"
- "创建一个新分支 feature-calculator 并提交"

### 手动提交

```bash
# 使用自动提交脚本
./scripts/auto-commit.sh "feat: 添加新功能"

# 或者手动 Git 命令
git add -A
git commit -m "feat: 你的提交信息"
git push origin main
```

---

## ✅ 完成！

现在你可以：
- ✅ 让 AI 写代码并自动提交
- ✅ 在 GitHub 上查看提交历史
- ✅ 与团队协作开发

---

## 📚 更多文档

- [完整配置指南](./GITHUB-SETUP-GUIDE.md) - 详细配置步骤和故障排查
- [Skill 文档](./skills/github-auto-commit/SKILL.md) - GitHub 自动提交 Skill 说明

---

**遇到问题？** 查看 [GITHUB-SETUP-GUIDE.md](./GITHUB-SETUP-GUIDE.md) 的故障排查部分。
