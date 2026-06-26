# 学校网站内容整理与查漏补缺 Spec

## Why
学校网站项目已经搭建了基本的 Django 框架和功能模块，但存在内容缺失、功能不完整、模板重复、安全风险等问题，需要全面梳理现有内容，识别并修复缺失项，确保网站功能完整、内容充实、安全可靠。

## What Changes

### 内容整理
- 梳理所有 app 的模型、视图、URL 路由和模板，确保功能链路完整
- 统一模板目录结构，解决模板文件重复问题（同时存在于 `apps/templates/` 和 `apps/<app>/templates/`）
- 补充缺失的模板文件内容

### 功能补全
- 添加搜索功能（导航栏已有搜索按钮但未实现）
- 补全学校概况页面内容（about 页面数据填充）
- 添加通知公告与新闻的区分能力
- 添加友情链接管理功能
- 添加站点地图（sitemap）
- 添加网站地图页面

### 安全修复
- **数据库密码从 settings.py 硬编码移除，改为环境变量读取**
- 添加 CSRF 保护中间件检查
- 统一错误页面样式

### 用户体验优化
- 完善导航栏响应式设计
- 添加面包屑导航
- 统一页面标题和描述
- 添加分页功能检查

## Impact
- Affected specs: core, pages, organization, news, admissions, graduates, contact, gallery, accounts
- Affected code: 所有 app 的 views.py、models.py、urls.py、templates；settings.py；static 文件

## ADDED Requirements

### Requirement: 搜索功能
The system SHALL provide站内搜索功能。
- **WHEN** 用户在搜索框输入关键词并提交
- **THEN** 系统返回匹配的新闻、页面、教师等内容的搜索结果列表

### Requirement: 友情链接管理
The system SHALL provide友情链接管理功能。
- **WHEN** 管理员在后台添加友情链接
- **THEN** 网站底部显示友情链接列表

### Requirement: 站点地图
The system SHALL provide站点地图页面。
- **WHEN** 用户访问 /sitemap/
- **THEN** 显示网站所有可访问页面的结构列表

### Requirement: 通知公告与新闻区分
The system SHALL 区分通知公告和普通新闻文章。
- **WHEN** 用户访问信息发布页面
- **THEN** 可以看到分类筛选，区分通知公告和新闻

### Requirement: 安全配置修复
The system SHALL 从环境变量读取数据库密码。
- **WHEN** 项目启动时
- **THEN** 数据库密码从环境变量 `DB_PASSWORD` 读取，而非硬编码

## MODIFIED Requirements

### Requirement: 模板目录结构统一
**变更**: 解决模板文件重复问题
- 统一使用 `apps/<app>/templates/<app>/` 目录结构
- 删除 `apps/templates/` 下的重复模板文件
- 确保所有模板继承自 `base.html`

### Requirement: 学校概况页面
**变更**: 完善 about 页面
- 添加多种学校概况页面模板（学校简介、历史沿革、校园文化、办学理念等）
- 通过 pages app 管理多个固定页面

### Requirement: 错误页面
**变更**: 完善 404 和 500 错误页面
- 添加样式和导航链接
- 确保错误页面可正常返回首页

## REMOVED Requirements
无