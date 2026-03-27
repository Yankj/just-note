---
name: github-auto-commit
description: |
  自动将代码变更提交到 GitHub。支持自动检测变更、生成提交信息、推送到远程仓库。
  使用 OpenClaw 内置的 git 命令直接操作 workspace。
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
---

# GitHub 自动提交 Skill

## 一句话定位

> AI 写代码后自动提交到 GitHub，无需手动操作。

## 核心功能

1. **自动检测变更** - 识别 workspace 中的文件变更
2. **智能提交信息** - 根据变更内容生成有意义的 commit message
3. **一键推送** - 自动推送到 GitHub 远程仓库
4. **分支管理** - 支持创建新分支或提交到当前分支

## 快速开始

### 首次配置

```bash
# 1. 初始化 Git 仓库（如果还没有）
cd ~/openclaw/workspace && git init

# 2. 配置用户信息
git config user.name "Your Name"
git config user.email "your@email.com"

# 3. 添加远程仓库
git remote add origin https://github.com/username/repo.git

# 4. 测试连接
gh auth status  # 如果安装了 GitHub CLI
```

### 使用方法

**方法 1: 直接调用脚本**
```bash
./scripts/auto-commit.sh "feat: 添加新功能"
```

**方法 2: 让 AI 自动提交**

告诉 AI：
- "把刚才写的代码提交到 GitHub"
- "提交所有变更并推送"
- "创建一个新分支 feature-xxx 并提交"

## 提交流程

### 标准流程

1. **检测变更**
   ```bash
   git status --short
   ```

2. **生成提交信息**
   - 分析变更文件
   - 识别变更类型（feat/fix/docs/style/refactor/test/chore）
   - 生成符合 Conventional Commits 的消息

3. **提交并推送**
   ```bash
   git add -A
   git commit -m "type: message"
   git push origin <branch>
   ```

### 分支策略

| 场景 | 分支命名 | 说明 |
|------|---------|------|
| 新功能 | `feature/xxx` | 从 main 创建 |
| Bug 修复 | `fix/xxx` | 从 main 创建 |
| 紧急修复 | `hotfix/xxx` | 从 main 创建 |
| 日常提交 | `main` | 直接提交 |

## 提交信息规范

采用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Type 类型

| Type | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(note): 添加日记视图` |
| `fix` | Bug 修复 | `fix(cli): 修复日期比较错误` |
| `docs` | 文档更新 | `docs(readme): 更新安装说明` |
| `style` | 代码格式 | `style(format): 格式化代码` |
| `refactor` | 重构 | `refactor(core): 重构分类逻辑` |
| `test` | 测试 | `test(cli): 添加单元测试` |
| `chore` | 构建/工具 | `chore(deps): 更新依赖` |
| `auto` | AI 自动提交 | `auto: 自动提交代码变更` |

### 示例

```bash
# 新功能
feat(just-note): 添加 AI 每日总结功能

- 实现 daily-summary 命令
- 添加 AI 分析 Prompt
- 支持 Markdown 格式输出

# Bug 修复
fix(cli): 修复日记视图日期比较错误

- 修复 bash [[ ]] 语法问题
- 改用简化日期比较逻辑

# 文档更新
docs(readme): 更新快速开始指南

- 添加安装步骤
- 补充使用示例
```

## 自动化场景

### 场景 1: AI 写完代码自动提交

**用户**: "帮我写一个计算器组件，写完后提交到 GitHub"

**AI 流程**:
1. 编写代码
2. 测试功能
3. 运行 `./scripts/auto-commit.sh "feat(calculator): 添加计算器组件"`
4. 返回提交结果

### 场景 2: 批量提交多个文件

**用户**: "把所有修改的文件提交上去"

**AI 流程**:
1. `git status --short` 查看变更
2. 分析变更内容生成提交信息
3. `git add -A && git commit -m "..." && git push`

### 场景 3: 创建功能分支

**用户**: "在新分支上开发这个功能"

**AI 流程**:
1. `git checkout -b feature/xxx`
2. 开发功能
3. 提交并推送：`git push -u origin feature/xxx`

## 配置项

### 环境变量（可选）

```bash
# 设置默认远程仓库
export OPENCLAW_GIT_REMOTE="origin"

# 设置默认分支
export OPENCLAW_GIT_BRANCH="main"

# 设置提交者信息
export GIT_AUTHOR_NAME="Your Name"
export GIT_AUTHOR_EMAIL="your@email.com"
```

### Git 配置

```bash
# 查看配置
git config --list

# 修改配置
git config user.name "Your Name"
git config user.email "your@email.com"
git config init.defaultBranch main
```

## 故障排查

### 问题 1: 推送失败（认证错误）

**错误**: `remote: Authentication failed`

**解决**:
```bash
# 方法 1: 使用 GitHub CLI
gh auth login

# 方法 2: 使用 Personal Access Token
git remote set-url origin https://<TOKEN>@github.com/username/repo.git

# 方法 3: 配置 SSH
ssh-keygen -t ed25519 -C "your@email.com"
# 添加公钥到 GitHub Settings → SSH Keys
git remote set-url origin git@github.com:username/repo.git
```

### 问题 2: 冲突

**错误**: `hint: Updates were rejected because the remote contains work that you do not have`

**解决**:
```bash
# 先拉取远程变更
git pull --rebase origin main

# 解决冲突后继续
git rebase --continue

# 或者强制推送（慎用！）
git push -f origin main
```

### 问题 3: 大文件

**错误**: `error: File is too big`

**解决**:
```bash
# 安装 Git LFS
git lfs install

# 追踪大文件
git lfs track "*.png"
git lfs track "*.zip"

# 提交 .gitattributes
git add .gitattributes
git commit -m "chore: 配置 Git LFS"
```

## 相关文件

- `scripts/auto-commit.sh` - 自动提交脚本
- `.gitignore` - Git 忽略文件配置
- `.git/config` - Git 仓库配置

## 最佳实践

1. **小步提交** - 每次提交一个完整的小功能
2. **有意义的提交信息** - 说明「为什么」而不是「是什么」
3. **提交前测试** - 确保代码能正常运行
4. **及时推送** - 避免本地丢失
5. **使用分支** - 新功能在分支上开发，完成后合并

## 安全提示

- ⚠️ 不要提交敏感信息（API Keys、密码等）
- ⚠️ 检查 `.gitignore` 配置
- ⚠️ 私有仓库注意权限设置
- ⚠️ 使用 Personal Access Token 而非密码

---

> **核心理念**: 让 AI 写代码和提交像呼吸一样自然。
