#!/bin/bash
# GitHub 推送脚本
# 功能：
# 1. 推送完整代码到 feature/full-workspace 分支
# 2. 推送清理后的代码到 main 分支

set -e

cd /home/admin/openclaw/workspace

echo "======================================"
echo "  GitHub 推送"
echo "======================================"
echo ""

# 切换到 feature 分支
echo "📦 准备推送完整代码到 feature/full-workspace..."
git checkout feature/full-workspace

# 推送 feature 分支
echo "🚀 推送到 GitHub..."
git push -u origin feature/full-workspace

echo "✅ feature/full-workspace 推送完成！"
echo ""

# 切换到 main 分支
echo "📦 准备推送清理后代码到 main..."
git checkout main

# 推送 main 分支
echo "🚀 推送到 GitHub..."
git push -u origin main

echo "✅ main 推送完成！"
echo ""

echo "======================================"
echo "  ✅ 推送完成！"
echo "======================================"
echo ""
echo "分支说明："
echo "  - main: 只包含「记一下」Web App"
echo "  - feature/full-workspace: 完整的 OpenClaw workspace"
echo ""
echo "访问：https://github.com/Yankj/just-note"
echo "======================================"
