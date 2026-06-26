# 角色驱动导航栏与内容展示 Spec

## Why
当前网站对所有用户（访客和已登录用户）展示完全相同的导航栏，无法体现不同角色的功能差异。需要实现：访客看完整公开内容，登录后根据用户角色（学生、班主任、教务主任、校长、管理员等）展示精简且针对性的导航，提升用户体验和操作效率。

## What Changes
- **用户角色扩展**：在现有 User 模型的 ROLE_CHOICES 中新增 `head_teacher`（班主任）、`academic_director`（教务主任）、`principal`（校长）、`counselor`（辅导员）、`staff`（后勤/行政），保留原有 `student`、`parent`、`teacher`、`whiteboard`、`admin`
- **角色选择**：登录/注册时允许用户选择角色（或由管理员在后台分配）
- **导航栏自适应**：**BREAKING** — 导航栏不再硬编码，改为由上下文处理器根据用户角色动态生成菜单项
- **访客模式**：未登录时展示完整公开导航（与当前一致）
- **登录后精简模式**：每种角色看到专属导航项

## Impact
- Affected specs: accounts
- Affected code: [accounts/models.py](file:///d:/IST/Project/School-Web/school_site/apps/accounts/models.py)、[accounts/forms.py](file:///d:/IST/Project/School-Web/school_site/apps/accounts/forms.py)、[accounts/context_processors.py](file:///d:/IST/Project/School-Web/school_site/apps/accounts/context_processors.py)、[templates/base.html](file:///d:/IST/Project/School-Web/school_site/templates/base.html)、[accounts/admin.py](file:///d:/IST/Project/School-Web/school_site/apps/accounts/admin.py)

## ADDED Requirements

### Requirement: 角色扩展
The system SHALL 支持以下用户角色类型：
- 学生（student）、家长（parent）、班主任（head_teacher）、普通教师（teacher）、教务主任（academic_director）、校长（principal）、辅导员（counselor）、后勤/行政（staff）、班级账户（whiteboard）、管理员（admin）

#### Scenario: 管理员在后台为用户分配角色
- **WHEN** 管理员在 Django Admin 编辑用户
- **THEN** 可从角色下拉列表中选择上述任意角色

### Requirement: 角色驱动的导航菜单
The system SHALL 根据用户角色动态生成导航栏菜单项。

#### Scenario: 访客访问
- **WHEN** 用户未登录
- **THEN** 导航栏展示完整公开菜单：首页、学校概况（下拉）、组织架构、信息发布、招生招聘、毕业生、校园风光、互动交流

#### Scenario: 学生登录
- **WHEN** 学生角色用户登录
- **THEN** 导航栏展示：首页、信息发布、班级空间、个人中心

#### Scenario: 班主任登录
- **WHEN** 班主任角色用户登录
- **THEN** 导航栏展示：首页、信息发布、班级管理、学生管理、个人中心

#### Scenario: 教务主任登录
- **WHEN** 教务主任角色用户登录
- **THEN** 导航栏展示：首页、信息发布、教学管理、课程安排、师资队伍、个人中心

#### Scenario: 校长登录
- **WHEN** 校长角色用户登录
- **THEN** 导航栏展示：首页、信息发布、组织架构、校园风光、数据统计、个人中心

#### Scenario: 管理员登录
- **WHEN** 管理员角色用户登录
- **THEN** 导航栏展示：首页、信息发布、组织架构、招生招聘、校园风光、后台管理、个人中心

#### Scenario: 家长登录
- **WHEN** 家长角色用户登录
- **THEN** 导航栏展示：首页、信息发布、孩子信息、家校互动、个人中心

#### Scenario: 普通教师登录
- **WHEN** 普通教师角色用户登录
- **THEN** 导航栏展示：首页、信息发布、教学资源、个人中心

#### Scenario: 辅导员登录
- **WHEN** 辅导员角色用户登录
- **THEN** 导航栏展示：首页、信息发布、学生辅导、个人中心

#### Scenario: 后勤/行政登录
- **WHEN** 后勤/行政角色用户登录
- **THEN** 导航栏展示：首页、信息发布、资源管理、个人中心

### Requirement: 导航菜单上下文处理器
The system SHALL 通过上下文处理器 `nav_menu` 向所有模板注入当前用户对应的导航菜单数据。

#### Scenario: 导航数据正确注入
- **WHEN** 任意页面渲染
- **THEN** 模板上下文中存在 `nav_items` 变量，包含当前角色对应的菜单列表

## MODIFIED Requirements

### Requirement: User 模型 ROLE_CHOICES
**变更**: 扩展角色选项，新增 `head_teacher`、`academic_director`、`principal`、`counselor`、`staff`
- 需要创建数据库迁移

### Requirement: base.html 导航栏
**变更**: 从硬编码菜单列表改为遍历 `nav_items` 动态渲染
- 桌面端导航栏：`{% for item in nav_items %}` 循环渲染
- 移动端导航栏：同样遍历 `nav_items` 渲染
- 支持下拉子菜单结构（`item.children`）

## REMOVED Requirements
无