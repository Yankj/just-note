# Token 管理总结

## 📋 当前状态

✅ **本地 Git 配置**:
- Credential helper: store
- 远程仓库：https://github.com/Yankj/just-note.git (不含 Token)

✅ **已提交文件**:
- `.github-token.sh` - Token 加载脚本（不含实际 Token）
- `GIT-TOKEN-MANAGEMENT.md` - Token 管理文档

✅ **远程仓库**:
- main 分支：干净的 Web App 代码
- feature/full-workspace 分支：完整 workspace

---

## 🔐 Token 管理方案

### 方案一：SSH Key ⭐⭐⭐⭐⭐（强烈推荐）

**一劳永逸，最安全**

```bash
# 生成 SSH Key
ssh-keygen -t ed25519 -C "your_email@example.com"

# 查看公钥
cat ~/.ssh/id_ed25519.pub

# 复制内容添加到 GitHub:
# https://github.com/settings/ssh/new

# 切换为 SSH
git remote set-url origin git@github.com:Yankj/just-note.git

# 测试
ssh -T git@github.com

# 推送（无需密码）
git push
```

---

### 方案二：Git Credential Helper ⭐⭐⭐⭐

```bash
# 配置
git config --global credential.helper store

# 推送一次（保存凭证）
git push

# 以后无需密码
git push
```

**凭证位置**: `~/.git-credentials`

---

### 方案三：Token 文件 + 脚本 ⭐⭐⭐

```bash
# 1. 保存 Token（首次）
echo 'YOUR_TOKEN' > ~/.github_token
chmod 600 ~/.github_token

# 2. 加载 Token
source ~/.openclaw/workspace/.github-token.sh

# 3. 推送
git-push
```

---

## ⚠️ 安全警告

### 已删除的 Token

旧 Token 已经：
- ❌ 在终端命令中暴露
- ❌ 被 GitHub Secret Scanning 检测到
- ❌ 阻止推送多次

**建议立即删除此 Token！**

---

## 🚀 推荐操作

### 立即执行

1. **删除旧 Token**
   ```
   https://github.com/settings/tokens
   → 删除 ghp_wd5i0gg...
   ```

2. **配置 SSH Key**（推荐）
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   cat ~/.ssh/id_ed25519.pub
   # 添加到 GitHub
   git remote set-url origin git@github.com:Yankj/just-note.git
   ```

3. **或生成新 Token**
   ```
   https://github.com/settings/tokens/new
   → 勾选 repo 权限
   → 保存到新位置
   ```

---

## 📝 后续推送

### 如果配置了 SSH

```bash
git push  # 直接推送，无需密码
```

### 如果使用 Credential Helper

```bash
git push  # 第一次需要输入，之后自动记住
```

### 如果使用 Token 脚本

```bash
source .github-token.sh
git-push
```

---

## 📊 方案对比

| 方案 | 安全性 | 便利性 | 推荐度 |
|------|--------|--------|--------|
| SSH Key | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Credential Helper | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Token 文件 + 脚本 | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 每次手动输入 | ⭐⭐⭐⭐ | ⭐ | ⭐⭐ |

---

**请选择 SSH Key 方案！** 🔒
