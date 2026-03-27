# UI/UX Pro Max Skill - 本地实现

## 核心能力

基于 ClawHub 上的 ui-ux-pro-max skill，本地化实现 UI/UX 设计智能指导。

## 设计原则

### 1. 视觉层次 (Visual Hierarchy)
- **F 型扫描模式**: 重要内容放在左上角
- **尺寸对比**: 标题:正文 = 至少 1.5:1
- **颜色对比度**: 文字与背景对比度 ≥ 4.5:1 (WCAG AA)
- **间距系统**: 使用 4/8/12/16/24/32/48/64 节奏

### 2. 配色方案
```
主色：紫色系 (#6366f1 → #7c3aed)
辅色：蓝紫渐变 (#667eea → #764ba2)
成功：#10b981
警告：#f59e0b
危险：#ef4444
背景：渐变紫色
卡片：玻璃态 (rgba(255,255,255,0.1) + backdrop-blur)
```

### 3. 玻璃态设计 (Glassmorphism)
```css
.glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}
```

### 4. 交互细节
- **悬停效果**: transform translateY(-4px) + shadow
- **点击反馈**: scale(0.98)
- **加载状态**: 骨架屏 + 渐变动画
- **过渡动画**: all 0.3s ease

### 5. 响应式断点
```
sm: 640px
md: 768px
lg: 1024px
xl: 1280px
2xl: 1536px
```

### 6. 无障碍设计 (WCAG 2.2)
- 所有交互元素有 focus 状态
- 颜色不是唯一的信息传达方式
- 字体大小至少 14px
- 点击区域至少 44x44px

## 使用方式

### 设计审查
```bash
# 审查当前界面
skill run ui-ux-pro-max --action audit --path frontend/src/pages

# 生成配色方案
skill run ui-ux-pro-max --action palette --style glassmorphism --color purple

# 优化组件
skill run ui-ux-pro-max --action polish --component Dashboard
```

### 设计生成
```bash
# 创建新页面
skill run ui-ux-pro-max --action create --type dashboard --style modern

# 生成设计系统
skill run ui-ux-pro-max --action design-system --brand 财务自由之路
```

## 检查清单

### UI 审查清单
- [ ] 视觉层次清晰
- [ ] 配色和谐统一
- [ ] 间距一致 (8px 网格)
- [ ] 字体层次分明
- [ ] 图标风格统一
- [ ] 卡片对齐整齐
- [ ] 留白充足
- [ ] 加载状态友好

### UX 审查清单
- [ ] 导航清晰直观
- [ ] 操作反馈及时
- [ ] 错误提示明确
- [ ] 空状态有引导
- [ ] 表单验证友好
- [ ] 键盘导航可用
- [ ] 移动端适配良好
- [ ] 性能优化到位

---

**基于 ClawHub ui-ux-pro-max by @xobi667 本地化实现**
