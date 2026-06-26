# 作家工厂 UI 风格统一与代码审查 Spec

## Why
作家工厂项目在上一轮功能整合后，UI风格严重不一致：登录/注册页和所有新功能模块（角色/关系/时间线/科技树）使用硬编码蓝色(#4A90D9)和朴素白色卡片，与主应用的玻璃拟态(glassmorphism)渐变风格完全脱节。同时约一半模板未继承 base.html，导致缺乏导航栏和页脚，影响用户体验。

## What Changes

### UI 风格统一
- 将所有模板统一为继承 `base.html`，使用全局导航栏和页脚
- 将登录/注册页的内联CSS改为复用 `nav.css` 的CSS变量（`--color-primary: #5b7fff`）
- 将所有新功能模块的内联CSS中的硬编码颜色替换为CSS变量
- 在 `nav.css` 中补充全局通用组件样式（表单、按钮、卡片、表格、分页等）
- 为所有新模板应用玻璃拟态风格（渐变背景、毛玻璃效果、统一圆角）

### 代码审查修复
- 修复 `base.html` 中导航栏 `works` 变量缺失问题（需在上下文中传递）
- 在 `base.html` 导航栏添加用户信息显示和登出按钮
- 将 `about.html` 改为继承 `base.html`
- 将 `trash.html` 改为继承 `base.html`
- 将 `work_create.html` 改为继承 `base.html`
- 将 `work_detail.html` 改为继承 `base.html`
- 将 `chapter_read.html` 改为继承 `base.html`
- 将 `outline.html` 改为继承 `base.html`
- 修复 `stats.html` 中 `chart_items` 与 `chart_data_json` 的不一致
- 检查并创建缺失的CSS文件（search.css）

### 模板上下文传递修复
- 确保所有视图在为模板渲染时传递 `works` 变量（用于导航栏下拉菜单）
- 在 `base.html` 中通过 `request.user` 显示当前用户信息

## Impact
- **Affected specs**: 所有模板文件、导航栏、CSS样式系统
- **Affected code**: `chapters/templates/` 全部23个文件、`chapters/static/chapters/` 全部CSS文件、`chapters/views.py` 部分视图

## ADDED Requirements

### Requirement: 统一UI设计系统
The system SHALL use a consistent set of CSS variables across all templates.

#### Scenario: 登录页使用主色调
- **WHEN** 用户访问登录页面
- **THEN** 登录按钮使用 `var(--color-primary)` 而非硬编码 `#4A90D9`
- **THEN** 登录卡片使用玻璃拟态效果（半透明背景、模糊、渐变边框）

#### Scenario: 新功能模块使用主色调
- **WHEN** 用户访问角色/关系/时间线/科技树页面
- **THEN** 所有按钮、链接、卡片使用全局CSS变量而非硬编码颜色
- **THEN** 页面背景与主应用一致（渐变背景）

### Requirement: 所有页面继承base.html
The system SHALL ensure all pages extend base.html for consistent navigation.

#### Scenario: 独立页面集成导航
- **WHEN** 用户访问关于/回收站/新建作品/作品详情/章节阅读/大纲页面
- **THEN** 页面包含完整的顶部导航栏和页脚
- **THEN** 导航栏中包含搜索框、用户信息、登出按钮

### Requirement: 导航栏显示用户信息
The system SHALL display user info and logout button in the navigation bar.

#### Scenario: 已登录用户看到导航栏中的用户信息
- **WHEN** 已登录用户访问任何页面
- **THEN** 导航栏右侧显示用户名和登出按钮
- **THEN** 未登录用户看到登录/注册链接

### Requirement: 共享CSS组件库
The system SHALL provide shared CSS classes for common components.

#### Scenario: 统一按钮样式
- **WHEN** 开发者添加按钮
- **THEN** 使用 `.btn`、`.btn-primary`、`.btn-danger`、`.btn-sm` 等全局类
- **THEN** 所有按钮外观一致，无需在每个模板中重复定义

## MODIFIED Requirements

### Requirement: 模板继承
**变更**: 以下模板从独立HTML改为继承 `base.html`
- about.html, trash.html, work_create.html, work_detail.html, chapter_read.html, outline.html

### Requirement: 内联CSS
**变更**: 各模板中的内联CSS样式统一使用CSS变量，移除硬编码颜色值
- 所有 `#4a90d9` 替换为 `var(--color-primary)`
- 所有 `#e74c3c` 替换为 `var(--color-danger)`
- 所有 `#27ae60` 替换为 `var(--color-success)`
- 所有 `#95a5a6` 替换为 `var(--color-secondary)`

### Requirement: 视图上下文
**变更**: 所有视图需传递 `works` 变量到模板上下文
- 在 `work_list` 等视图中确保 `works` 变量始终在上下文中
- 在 `base.html` 中通过 `request.user` 判断登录状态

## REMOVED Requirements
无