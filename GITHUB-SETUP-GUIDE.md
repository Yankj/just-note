# GitHub 自动提交流程配置指南

**创建时间**: 2026-03-28  
**目的**: 配置 OpenClaw 自动提交代码到 GitHub 的完整流程

---

## 一、已完成配置 ✅

### 1. Git 仓库初始化

```bash
✓ Git 仓库已初始化：~/openclaw/workspace/.git
✓ Git 用户信息已配置:
  - user.name = OpenClaw Agent
  - user.email = agent@openclaw.local
```

### 2. 已创建文件

| 文件 | 说明 |
|------|------|
| `.gitignore` | Git 忽略文件配置 |
| `scripts/auto-commit.sh` | 自动提交脚本 |
| `skills/github-auto-commit/SKILL.md` | GitHub 提交 Skill |
| `GITHUB-SETUP-GUIDE.md` | 本配置指南 |

---

## 二、需要配置的步骤 ⚠️

### 步骤 1: 创建 GitHub 仓库

1. 访问 https://github.com/new
2. 创建新仓库（公开或私有）
3. **不要**勾选"Initialize this repository with a README"
4. 记下仓库地址，例如：`https://github.com/yourname/openclaw-workspace.git`

### 步骤 2: 添加远程仓库

```bash
cd ~/openclaw/workspace

# 替换为你的仓库地址
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# 验证
git remote -v
```

### 步骤 3: 配置 GitHub 认证

**推荐方式 1: GitHub CLI（最简单）**

```bash
# 安装 GitHub CLI
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh -y

# 登录
gh auth login
# 选择 GitHub.com → HTTPS → Login with a web browser
# 复制 One-Time Code 并在浏览器授权
```

**方式 2: Personal Access Token**

```bash
# 1. 访问 https://github.com/settings/tokens
# 2. 生成新 Token（经典），勾选 repo 权限
# 3. 保存 Token（只会显示一次）

# 4. 配置 Git 使用 Token
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/YOUR_REPO.git
```

**方式 3: SSH Key**

```bash
# 生成 SSH Key
ssh-keygen -t ed25519 -C "your_email@example.com"

# 查看公钥
cat ~/.ssh/id_ed25519.pub

# 复制公钥内容，添加到 GitHub:
# https://github.com/settings/ssh/new

# 切换远程仓库为 SSH
git remote set-url origin git@github.com:YOUR_USERNAME/YOUR_REPO.git
```

### 步骤 4: 首次推送

```bash
cd ~/openclaw/workspace

# 创建初始提交
git add -A
git commit -m "chore: 初始化项目，配置 GitHub 自动提交流程"

# 推送到 GitHub
git branch -M main
git push -u origin main
```

---

## 三、使用方法

### 方法 1: 使用自动提交脚本

```bash
# 提交所有变更
./scripts/auto-commit.sh "feat: 添加新功能"

# 或者不带参数（使用默认提交信息）
./scripts/auto-commit.sh
```

### 方法 2: 让 AI 自动提交

**告诉 AI**:
- "把刚才写的代码提交到 GitHub"
- "提交所有变更并推送"
- "创建一个新分支 feature-xxx 并提交"
- "查看最近的提交历史"

**AI 会自动**:
1. 检测文件变更
2. 生成有意义的提交信息
3. 执行 `git add` → `git commit` → `git push`
4. 返回提交结果

### 方法 3: 手动 Git 命令

```bash
# 查看变更
git status

# 添加文件
git add <file>

# 提交
git commit -m "你的提交信息"

# 推送
git push origin main
```

---

## 四、提交流程图

```
AI 写代码
    ↓
检测文件变更 (git status)
    ↓
生成提交信息 (分析变更内容)
    ↓
添加文件 (git add -A)
    ↓
提交 (git commit -m "...")
    ↓
推送 (git push origin main)
    ↓
✅ 完成！
```

---

## 五、提交信息规范

采用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(note): 添加日记视图` |
| `fix` | Bug 修复 | `fix(cli): 修复日期比较错误` |
| `docs` | 文档更新 | `docs(readme): 更新安装说明` |
| `style` | 代码格式 | `style(format): 格式化代码` |
| `refactor` | 重构 | `refactor(core): 重构分类逻辑` |
| `test` | 测试 | `test(cli): 添加单元测试` |
| `chore` | 构建/工具 | `chore(deps): 更新依赖` |
| `auto` | AI 自动提交 | `auto: 自动提交代码变更` |

---

## 六、常用命令速查

```bash
# 查看状态
git status

# 查看提交历史
git log --oneline

# 查看变更
git diff

# 撤销未提交的变更
git checkout -- <file>

# 撤销已添加的文件
git reset HEAD <file>

# 修改最后一次提交
git commit --amend -m "新信息"

# 创建新分支
git checkout -b feature/xxx

# 切换分支
git checkout <branch>

# 合并分支
git merge <branch>

# 拉取远程变更
git pull origin main

# 强制推送（慎用！）
git push -f origin main
```

---

## 七、故障排查

### 问题 1: 推送失败（认证错误）

```bash
# 检查认证状态
gh auth status

# 重新登录
gh auth logout
gh auth login

# 或者使用 Token
git remote set-url origin https://TOKEN@github.com/USER/REPO.git
```

### 问题 2: 冲突

```bash
# 先拉取远程变更
git pull --rebase origin main

# 解决冲突后
git add <resolved-files>
git commit -m "fix: 解决合并冲突"
git push
```

### 问题 3: 大文件被拒绝

```bash
# 安装 Git LFS
git lfs install

# 追踪大文件类型
git lfs track "*.png"
git lfs track "*.zip"

# 提交 .gitattributes
git add .gitattributes
git commit -m "chore: 配置 Git LFS"
```

---

## 八、安全检查清单

提交前检查：

- [ ] 没有敏感信息（API Keys、密码等）
- [ ] `.gitignore` 配置正确
- [ ] 代码已测试能正常运行
- [ ] 提交信息清晰有意义
- [ ] 没有不必要的大文件

---

## 九、下一步

1. **创建 GitHub 仓库** → 添加远程仓库
2. **配置认证** → 选择 CLI/Token/SSH
3. **首次推送** → `git push -u origin main`
4. **开始使用** → 让 AI 写代码并自动提交

---

## 十、相关文件

- `scripts/auto-commit.sh` - 自动提交脚本
- `.gitignore` - Git 忽略配置
- `skills/github-auto-commit/SKILL.md` - Skill 定义

---

> **提示**: 配置完成后，你只需要告诉 AI「写代码并提交」，剩下的交给 AI！
