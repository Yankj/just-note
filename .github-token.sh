#!/bin/bash
# GitHub Token 安全管理脚本
# 用法：source .github-token.sh

# 从安全位置读取 Token
TOKEN_FILE="$HOME/.github_token"

if [ ! -f "$TOKEN_FILE" ]; then
    echo "❌ Token 未设置，请先设置 Token:"
    echo "  echo 'YOUR_TOKEN' > $TOKEN_FILE"
    echo "  chmod 600 $TOKEN_FILE"
    return 1
fi

# 设置 Token 到环境变量（仅当前会话有效）
export GITHUB_TOKEN=$(cat "$TOKEN_FILE")

# 推送函数
git-push() {
    local branch="${1:-main}"
    echo "📦 推送到 $branch 分支..."
    git push "https://${GITHUB_TOKEN}@github.com/Yankj/just-note.git" "$branch"
}

# 别名
alias ghp='git-push'

echo "✅ GitHub Token 已加载"
echo "使用方法:"
echo "  git-push          # 推送到 main 分支"
echo "  git-push feature  # 推送到 feature 分支"
echo "  ghp               # 简写"
