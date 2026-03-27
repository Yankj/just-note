# GitHub Token 安全管理方案

## 🔐 推荐方案：SSH Key

**最安全、最方便的方式**

```bash
# 1. 生成 SSH Key
ssh-keygen -t ed25519 -C "your_email@example.com"

# 2. 查看公钥
cat ~/.ssh/id_ed25519.pub

# 3. 添加到 GitHub
# https://github.com/settings/ssh/new

# 4. 切换远程仓库
git remote set-url origin git@github.com:Yankj/just-note.git

# 5. 推送（无需密码）
git push
```

**优点**:
- ✅ 最安全
- ✅ 无需管理 Token
- ✅ 一次配置永久使用

---

## 📋 备选方案：Git Credential Helper

```bash
# 配置 Git 记住凭证
git config --global credential.helper store

# 推送一次（会保存凭证）
git push

# 以后推送无需再次输入
git push
```

**凭证位置**: `~/.git-credentials` (权限 600)

---

## 📝 使用 Token 推送

### 方式一：环境变量

```bash
# 设置 Token（仅当前会话）
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx

# 推送
git push "https://${GITHUB_TOKEN}@github.com/Yankj/just-note.git" main
```

### 方式二：使用脚本

```bash
# 1. 保存 Token（首次）
echo 'YOUR_TOKEN' > ~/.github_token
chmod 600 ~/.github_token

# 2. 加载 Token
source .github-token.sh

# 3. 推送
git-push
```

---

## ⚠️ 安全警告

### ❌ 不要这样做

- 不要在代码中硬编码 Token
- 不要在提交中包含 Token
- 不要在日志中暴露 Token
- 不要分享 Token 给他人

### ✅ 应该这样做

- 使用 SSH Key（推荐）
- 使用环境变量
- 使用 Git Credential Helper
- 定期更换 Token

---

## 🔍 检查 Token 是否泄露

```bash
# 检查 Git 历史
git log -p | grep "ghp_"

# 检查文件
grep -r "ghp_" . --exclude="*.git/*"

# 检查远程配置
git remote -v
```

---

## 🚨 Token 泄露处理

1. **立即删除 Token**
   - https://github.com/settings/tokens

2. **生成新 Token**
   - https://github.com/settings/tokens/new

3. **更新配置**
   ```bash
   # 如果使用 Credential Helper
   rm ~/.git-credentials
   
   # 如果使用环境变量
   # 更新 ~/.github_token
   ```

---

**推荐使用 SSH Key！** 🔒
