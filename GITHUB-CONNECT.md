# 🔗 绑定 GitHub 仓库指南

**目的**: 将本地代码推送到你的 GitHub 账号

---

## 步骤 1: 创建 GitHub 仓库

1. 打开浏览器访问：https://github.com/new
2. 创建新仓库
   - **Repository name**: `just-note` 或 `openclaw-workspace`
   - **Description**: 记一下 - 零摩擦 AI 知识记录工具
   - **Public/Private**: 公开或私有（推荐公开）
   - ❌ **不要**勾选"Initialize this repository with a README"
3. 点击"Create repository"
4. 复制仓库地址，格式如：
   ```
   https://github.com/YOUR_USERNAME/just-note.git
   ```

---

## 步骤 2: 绑定远程仓库

在终端执行以下命令（替换为你的仓库地址）：

```bash
cd ~/openclaw/workspace

# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# 验证
git remote -v
```

**预期输出**:
```
origin  https://github.com/YOUR_USERNAME/YOUR_REPO.git (fetch)
origin  https://github.com/YOUR_USERNAME/YOUR_REPO.git (push)
```

---

## 步骤 3: 推送到 GitHub

### 方式 A: 使用 Personal Access Token（推荐）

1. **生成 Token**:
   - 访问：https://github.com/settings/tokens
   - 点击"Generate new token (classic)"
   - 勾选权限：`repo` (Full control of private repositories)
   - 点击"Generate token"
   - **复制 Token**（只会显示一次！）

2. **推送代码**:
   ```bash
   cd ~/openclaw/workspace
   
   # 重命名分支为 main
   git branch -M main
   
   # 推送（会提示输入用户名和密码）
   git push -u origin main
   
   # 用户名：你的 GitHub 用户名
   # 密码：刚才生成的 Token（不是 GitHub 密码！）
   ```

### 方式 B: 使用 SSH（如果你配置过 SSH Key）

```bash
cd ~/openclaw/workspace

# 切换为 SSH 地址
git remote set-url origin git@github.com:YOUR_USERNAME/YOUR_REPO.git

# 推送
git push -u origin main
```

---

## 步骤 4: 验证推送

推送成功后，访问你的 GitHub 仓库页面，应该能看到所有代码文件。

---

## 常见问题

### Q: `git remote add origin` 提示已存在？

```bash
# 删除旧的远程仓库
git remote remove origin

# 重新添加
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
```

### Q: 推送时提示认证失败？

确保使用 **Personal Access Token** 作为密码，而不是 GitHub 账号密码。

### Q: Token 过期了？

1. 访问：https://github.com/settings/tokens
2. 删除过期的 Token
3. 生成新的 Token
4. 重新推送

---

## 快速命令参考

```bash
# 查看远程仓库
git remote -v

# 修改远程仓库
git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# 查看分支
git branch

# 重命名分支
git branch -M main

# 推送
git push -u origin main

# 查看提交历史
git log --oneline
```

---

**需要帮助？** 告诉我你的 GitHub 用户名和仓库名，我可以生成完整的命令！
