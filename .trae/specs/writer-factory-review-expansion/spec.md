# 作家工厂 查漏补缺与拓展 Spec

## Why
作家工厂项目目前由两个独立的应用组成（Django novel_platform 和 Flask novel_manager），存在大量合并冲突、缺失CSS文件、功能割裂、无用户认证等关键问题，亟需系统地修复缺陷、整合功能并拓展新能力，使其成为一个完整、可用的创作管理平台。

## What Changes

### 修复类
- 修复 novel_platform 中所有未解决的合并冲突（Git冲突标记 `<<<<<<< HEAD` / `=======` / `>>>>>>>`）
- 解决模板中不一致的URL引用（如 `outline_rename` vs `outline_view`）
- 补全缺失的静态CSS文件（nav.css 已有，但各模板引用的CSS文件多数存在合并冲突）
- 修复 `bass.css` 空文件问题

### 整合类
- 将 Flask novel_manager 的四大核心功能（角色管理、关系管理、时间线、科技树）整合到 Django novel_platform 中
- 统一数据库管理，使用单一 Django 项目

### 新增类
- **用户认证系统**：注册、登录、登出，作品与用户绑定
- **作品标签/分类**：支持为作品添加标签和分类
- **搜索功能**：全局搜索作品、章节、角色
- **数据导出**：导出作品为 TXT/JSON 格式
- **统计面板增强**：更多可视化写作统计（月度趋势、累计字数等）
- **写作目标**：设定每日/每周码字目标，进度追踪
- **角色/关系/时间线/科技树管理界面**：从 Flask 迁移并增强

### 改进类
- 添加单元测试
- 配置生产环境安全设置（关闭 DEBUG、隐藏 SECRET_KEY）
- 添加分页功能
- 优化前端 UI/UX

## Impact
- **Affected specs**: 作品管理、章节编辑、大纲树、回收站、统计
- **Affected code**: `novel_platform/` 全部文件、`novel_manager/` 全部文件、`Writerworks/` 相关文件

## ADDED Requirements

### Requirement: 用户认证系统
The system SHALL provide user registration, login, and logout functionality.

#### Scenario: 用户注册
- **WHEN** 新用户填写注册表单并提交
- **THEN** 系统创建用户账户，自动登录并跳转到作品列表页

#### Scenario: 用户登录
- **WHEN** 已注册用户输入正确的用户名和密码
- **THEN** 系统建立会话，跳转到该用户的作品列表页

#### Scenario: 用户登出
- **WHEN** 已登录用户点击登出
- **THEN** 系统清除会话，跳转到登录页

### Requirement: 作品与用户绑定
The system SHALL associate works with the authenticated user.

#### Scenario: 用户只能看到自己的作品
- **WHEN** 用户访问作品列表
- **THEN** 系统只显示该用户创建的作品

### Requirement: 作品标签与分类
The system SHALL support tags and categories for works.

#### Scenario: 添加标签
- **WHEN** 用户在创建/编辑作品时添加标签
- **THEN** 系统保存标签，并在作品列表和详情页展示

### Requirement: 搜索功能
The system SHALL provide global search across works, chapters, and characters.

#### Scenario: 搜索作品
- **WHEN** 用户在搜索框输入关键词并搜索
- **THEN** 系统返回匹配的作品、章节和角色结果

### Requirement: 数据导出
The system SHALL allow exporting works to TXT and JSON formats.

#### Scenario: 导出作品
- **WHEN** 用户点击导出按钮选择格式
- **THEN** 系统生成包含该作品所有章节内容的文件并下载

### Requirement: 角色管理 (整合)
The system SHALL provide character management within the Django platform.

#### Scenario: 管理角色
- **WHEN** 用户创建/编辑/删除角色
- **THEN** 系统在数据库中保存变更，并在角色列表页展示

### Requirement: 关系管理 (整合)
The system SHALL manage relationships between characters.

#### Scenario: 管理关系
- **WHEN** 用户为两个角色添加关系类型和描述
- **THEN** 系统保存关系，并在关系列表页展示

### Requirement: 时间线管理 (整合)
The system SHALL manage timeline events linked to characters.

#### Scenario: 管理时间线事件
- **WHEN** 用户添加/编辑带日期的事件，并关联角色
- **THEN** 系统保存事件，在时间线视图按日期排序展示

### Requirement: 科技树管理 (整合)
The system SHALL provide a tech tree with hierarchical nodes.

#### Scenario: 管理科技树节点
- **WHEN** 用户添加/编辑/删除树形节点
- **THEN** 系统维护父子关系，在科技树页面递归展示

### Requirement: 写作目标
The system SHALL support daily/weekly writing goals.

#### Scenario: 设定目标
- **WHEN** 用户在设置页面设定每日/每周目标字数
- **THEN** 系统在统计面板显示目标进度

### Requirement: 统计面板增强
The system SHALL provide enhanced writing statistics.

#### Scenario: 查看统计
- **WHEN** 用户访问统计面板
- **THEN** 系统展示月度趋势图、累计字数、日均字数等可视化数据

## MODIFIED Requirements

### Requirement: 作品管理
- 新增 `user` 外键关联到用户模型
- 新增 `tags` 多对多字段
- 新增 `category` 分类字段

### Requirement: 章节管理
- 章节编辑界面新增字数实时统计
- 自动保存时更新字数统计和创作时长

### Requirement: 回收站
- 回收站中的作品/章节操作需验证用户所有权

## REMOVED Requirements
无