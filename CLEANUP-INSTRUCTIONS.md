# 🚨 紧急清理说明

**问题**: 不小心推送了整个 OpenClaw workspace 到 GitHub

**解决**: 需要从 Git 历史中删除敏感文件并强制推送

---

## 已完成的清理

✅ 已从 Git 索引中删除以下目录：
- `.openclaw/` - OpenClaw 系统文件
- `skills/` - 安装的 Skills
- `memory/` - 用户笔记/记忆
- `agents/` - Agent 配置
- `*.skill` - Skill 文件
- `config/` - 配置
- `templates/` - 模板
- `reports/` - 报告
- `finance-app/` - 其他项目

✅ 已更新 `.gitignore` 防止再次推送

---

## 需要手动执行的操作

### 方式一：强制推送（推荐）

```bash
cd ~/openclaw/workspace

# 执行强制推送（会重写 GitHub 历史）
git push -f origin main
```

**需要认证**:
- 用户名：Yankj
- 密码：使用新的 Personal Access Token

### 方式二：在 GitHub 上删除仓库重新创建

1. 访问：https://github.com/Yankj/just-note/settings
2. 滚动到底部，点击"Delete this repository"
3. 确认删除
4. 重新创建空仓库
5. 重新推送：
   ```bash
   git push -u origin main
   ```

---

## 清理后保留的文件

只保留「记一下」Web App 相关文件：

```
apps/just-note-web/       # ✅ 保留
docs/                     # ✅ 保留
GITHUB-*.md              # ✅ 保留（GitHub 相关文档）
```

---

## 验证清理

推送后访问：https://github.com/Yankj/just-note

应该只看到：
- `apps/just-note-web/` - Web App 代码
- `docs/` - 文档
- `GITHUB-*.md` - GitHub 配置文档

**不应该看到**:
- ❌ `.openclaw/`
- ❌ `skills/`
- ❌ `memory/`
- ❌ `agents/`
- ❌ `*.skill`

---

**请立即执行强制推送！** 🚨
