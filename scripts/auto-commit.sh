#!/bin/bash
# OpenClaw 自动提交 GitHub 脚本
# 用法：./auto-commit-commit.sh [commit message]

set -e

WORKSPACE="$HOME/openclaw/workspace"
cd "$WORKSPACE"

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  OpenClaw 自动提交 GitHub${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 检查 Git 配置
if ! git config user.name > /dev/null 2>&1; then
    echo -e "${YELLOW}配置 Git 用户信息...${NC}"
    git config user.name "OpenClaw Agent"
    git config user.email "agent@openclaw.local"
fi

# 检查远程仓库
REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")
if [ -z "$REMOTE_URL" ]; then
    echo -e "${YELLOW}未配置远程仓库${NC}"
    echo "请输入 GitHub 仓库地址 (例如：https://github.com/username/repo.git):"
    read -r REPO_URL
    if [ -n "$REPO_URL" ]; then
        git remote add origin "$REPO_URL"
        echo -e "${GREEN}✓ 已添加远程仓库${NC}"
    else
        echo -e "${RED}✗ 未输入仓库地址，退出${NC}"
        exit 1
    fi
fi

# 查看变更
echo -e "${YELLOW}检查文件变更...${NC}"
git status --short

# 如果有变更
if [ -n "$(git status --short)" ]; then
    echo ""
    echo -e "${YELLOW}发现文件变更${NC}"
    
    # 自动提交消息
    COMMIT_MSG="${1:-auto: 自动提交代码变更}"
    
    # 添加所有变更
    echo -e "${GREEN}添加文件...${NC}"
    git add -A
    
    # 提交
    echo -e "${GREEN}提交变更...${NC}"
    git commit -m "$COMMIT_MSG"
    
    # 推送
    echo -e "${GREEN}推送到 GitHub...${NC}"
    git push origin $(git branch --show-current)
    
    echo ""
    echo -e "${GREEN}✓ 提交成功！${NC}"
    echo -e "提交信息：$COMMIT_MSG"
else
    echo -e "${GREEN}✓ 没有文件变更${NC}"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
