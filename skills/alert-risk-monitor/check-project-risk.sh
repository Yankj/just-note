#!/bin/bash
# 项目风险检查脚本 - AI Native 示例
# 用法：./check-project-risk.sh [project_path]

set -e

PROJECT_PATH="${1:-.}"
REPORT_FILE="risk-report-$(date +%Y%m%d-%H%M%S).md"

echo "🔍 开始检查项目风险..."
echo "📁 项目路径：$PROJECT_PATH"
echo ""

# 初始化报告
cat > "$REPORT_FILE" << EOF
# 项目风险检查报告

**检查时间**: $(date '+%Y-%m-%d %H:%M')
**项目路径**: $PROJECT_PATH

---

## 🔴 高风险

EOF

# 1. 检查依赖漏洞
echo "📦 检查依赖漏洞..."
if command -v npm &> /dev/null && [ -f "$PROJECT_PATH/package.json" ]; then
    cd "$PROJECT_PATH"
    npm audit --json 2>/dev/null | jq -r '.vulnerabilities | to_entries[] | select(.value.severity == "high" or .value.severity == "critical") | "- [ ] \(.key): \(.value.severity)"' >> "../$REPORT_FILE" || true
fi

# 2. 检查 Git 状态
echo "📊 检查 Git 状态..."
if command -v git &> /dev/null && git rev-parse --git-dir > /dev/null 2>&1; then
    UNCOMMITTED=$(git status --porcelain | wc -l)
    if [ "$UNCOMMITTED" -gt 0 ]; then
        echo "- [ ] 有 $UNCOMMITTED 个未提交的文件" >> "$REPORT_FILE"
    fi
    
    BEHIND=$(git rev-list --count HEAD..origin/$(git branch --show-current) 2>/dev/null || echo "0")
    if [ "$BEHIND" -gt 0 ]; then
        echo "- [ ] 分支落后远程 $BEHIND 个提交" >> "$REPORT_FILE"
    fi
fi

# 3. 检查配置文件
echo "⚙️  检查配置文件..."
if [ -f "$PROJECT_PATH/.env" ]; then
    if grep -q "password=\|secret=\|key=" "$PROJECT_PATH/.env" 2>/dev/null; then
        echo "- [ ] ⚠️ .env 文件包含敏感信息，请确保已加入 .gitignore" >> "$REPORT_FILE"
    fi
fi

# 4. 检查测试覆盖率
echo "🧪 检查测试覆盖率..."
if [ -f "$PROJECT_PATH/coverage/coverage-summary.json" ]; then
    COVERAGE=$(jq -r '.total.lines.pct' "$PROJECT_PATH/coverage/coverage-summary.json" 2>/dev/null || echo "0")
    if (( $(echo "$COVERAGE < 70" | bc -l 2>/dev/null || echo 0) )); then
        echo "- [ ] 测试覆盖率仅 ${COVERAGE}%，建议 > 70%" >> "$REPORT_FILE"
    fi
fi

# 5. 检查大型文件
echo "📁 检查大型文件..."
LARGE_FILES=$(find "$PROJECT_PATH" -type f -size +10M -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null | head -5)
if [ -n "$LARGE_FILES" ]; then
    echo "- [ ] 发现大型文件 (>10MB):" >> "$REPORT_FILE"
    echo "$LARGE_FILES" | sed 's/^/  - /' >> "$REPORT_FILE"
fi

# 6. 检查过期依赖
echo "📦 检查过期依赖..."
if command -v npm &> /dev/null && [ -f "$PROJECT_PATH/package.json" ]; then
    cd "$PROJECT_PATH"
    OUTDATED=$(npm outdated --json 2>/dev/null | jq -r 'to_entries[] | select(.value.wanted != .value.latest) | "- [ ] \(.key): \(.value.current) → \(.value.latest)"' | head -10)
    if [ -n "$OUTDATED" ]; then
        echo "" >> "../$REPORT_FILE"
        echo "## 🟡 中风险 - 过期依赖" >> "../$REPORT_FILE"
        echo "$OUTDATED" >> "../$REPORT_FILE"
    fi
fi

# 添加总结
cat >> "$REPORT_FILE" << EOF

---

## 📋 建议操作

1. 优先修复高风险项目
2. 定期更新依赖
3. 保持测试覆盖率 > 70%
4. 清理大型未跟踪文件

**生成时间**: $(date '+%Y-%m-%d %H:%M:%S')
EOF

echo ""
echo "✅ 检查完成！"
echo "📄 报告已生成：$REPORT_FILE"
echo ""

# 如果有高风险项，显示警告
if grep -q "🔴 高风险" "$REPORT_FILE" && grep -q "\- \[ \]" "$REPORT_FILE"; then
    echo "⚠️  发现高风险项，请及时处理！"
fi
