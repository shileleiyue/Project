# 校园设备借用与维修管理系统 Spec

## Why
暑期培训期间教室和实验室有大量设备被学生借用（投影仪、摄像头、开发板等），传统纸质登记容易出现设备占用冲突、归还不清楚、损坏无人负责、维修进度不可追踪等问题。需要开发一个系统来管理设备借用、归还、损坏上报、维修派单和维修结果确认。

## What Changes
- 在 D:\IST\Project 下新建 `campus-device/` 前端项目（HTML+CSS+JS，无框架，MPA多页面架构，IIFE模块模式）
- 在 D:\IST\Project 下新建 `campus-device-backend/` 后端项目（Python FastAPI + SQLAlchemy 2.0 + MySQL，JWT认证）
- 新增 6 张数据库表：users、devices、borrows、repairs、repair_images、audit_logs
- 新增 4 组 RESTful API 模块：认证、设备、借用、维修
- 新增 3 类角色：学生（普通用户）、管理员、维修人员
- 新增 11 个前端页面，涵盖设备大厅、借用管理、维修管理、管理后台

## Impact
- Affected specs: 无（全新项目）
- Affected code: `D:\IST\Project\campus-device\`（前端）、`D:\IST\Project\campus-device-backend\`（后端）

## ADDED Requirements

### Requirement: 前端项目骨架搭建
系统 SHALL 在 `campus-device/` 目录下搭建基于原生 HTML+CSS+JS 的多页面前端项目，使用 IIFE 模块模式封装，CSS 变量管理主题，不依赖任何第三方框架。

#### Scenario: 项目目录结构正确
- **WHEN** 开发者查看 `campus-device/` 目录
- **THEN** 应包含 `index.html`、`login.html`、`register.html`、`css/`（reset.css、variables.css、common.css、layout.css 等）、`js/`（config.js、utils.js、storage.js、api.js、auth.js、paginator.js、upload.js、modal.js、toast.js 等）、`pages/`（device-detail.html、my-borrows.html、my-repairs.html、admin-devices.html、admin-borrows.html、admin-repairs.html、repair-tasks.html、repair-detail.html）、`assets/images/` 目录

### Requirement: 后端项目骨架搭建
系统 SHALL 在 `campus-device-backend/` 目录下搭建基于 FastAPI 的后端项目，包含分层架构（routers → services → repositories → models），统一响应格式和异常处理。

#### Scenario: 项目目录结构正确
- **WHEN** 开发者查看 `campus-device-backend/` 目录
- **THEN** 应包含 `app/`（main.py、config.py、dependencies.py、models/、schemas/、routers/、services/、repositories/、middleware/、utils/）、`uploads/`、`tests/`、`requirements.txt`、`.env`、`.gitignore`、`README.md`

### Requirement: 用户认证系统
系统 SHALL 提供基于 JWT 的用户注册、登录、退出功能，密码使用 bcrypt 加盐哈希存储，Token 有效期 24 小时。

#### Scenario: 用户登录成功
- **WHEN** 用户使用正确的手机号和密码调用 POST `/api/auth/login`
- **THEN** 返回 JWT Token 和用户信息（code=200）

#### Scenario: Token 过期处理
- **WHEN** 用户携带过期 Token 访问受保护接口
- **THEN** 返回 401 错误，前端自动跳转到登录页

### Requirement: 角色权限控制
系统 SHALL 支持三种角色（student/管理员、admin/管理员、repairer/维修人员），通过路由守卫和 API 权限依赖注入控制访问。

#### Scenario: 学生访问管理页面被拦截
- **WHEN** 学生角色用户尝试访问 `/pages/admin-devices.html`
- **THEN** 前端路由守卫弹出"无权限访问"提示并跳转到首页

#### Scenario: 管理员可访问所有页面
- **WHEN** 管理员角色用户访问任何页面
- **THEN** 允许访问

### Requirement: 设备管理（CRUD）
系统 SHALL 提供设备的增删改查功能，支持分页列表、关键词搜索、类型/状态筛选。管理员可新增、编辑、下架设备，所有登录用户可查看设备列表和详情。

#### Scenario: 分页查询设备列表
- **WHEN** 用户调用 GET `/api/devices?page=1&page_size=10&keyword=投影仪`
- **THEN** 返回包含 list、total、page、page_size、total_pages 的分页响应

#### Scenario: 管理员新增设备
- **WHEN** 管理员调用 POST `/api/devices` 提交设备名称、类型、描述等信息
- **THEN** 设备创建成功，状态为 available

### Requirement: 设备借用流程
系统 SHALL 支持学生申请借用设备 → 管理员审核通过/驳回 → 学生归还设备 → 管理员确认归还的完整流程，设备状态随流程自动流转。

#### Scenario: 借用申请成功
- **WHEN** 学生调用 POST `/api/borrows` 对 available 状态设备提交借用申请
- **THEN** 借用记录创建成功，设备状态变为 pending_borrow

#### Scenario: 管理员审核通过
- **WHEN** 管理员调用 PUT `/api/borrows/{id}/audit` 审核通过
- **THEN** 借用记录状态变为 approved（borrowing），设备状态变为 borrowed

#### Scenario: 归还设备（正常）
- **WHEN** 学生调用 PUT `/api/borrows/{id}/return` 归还设备且设备正常
- **THEN** 借用记录状态变为 pending_return，待管理员确认

### Requirement: 设备报修与维修流程
系统 SHALL 支持损坏上报 → 管理员创建维修工单 → 分配维修人员 → 维修人员更新状态 → 管理员确认完成的完整流程，支持图片上传。

#### Scenario: 维修工单创建
- **WHEN** 管理员调用 POST `/api/repairs` 创建维修工单
- **THEN** 工单状态为 pending，设备状态变为 repair_pending

#### Scenario: 维修人员更新状态
- **WHEN** 维修人员调用 PUT `/api/repairs/{id}/status` 更新为 repairing
- **THEN** 工单和设备状态同步更新

#### Scenario: 上传工单图片
- **WHEN** 用户调用 POST `/api/repairs/{id}/images` 上传图片
- **THEN** 图片保存到 `uploads/` 对应子目录，repair_images 表新增记录

### Requirement: 设备状态流转
系统 SHALL 严格按照状态机图管理设备状态：available → pending_borrow → borrowed → pending_return → available（正常归还）或 damaged → repair_pending → repairing → repaired → available（维修完成）或 scrapped（报废）。

#### Scenario: 状态流转合法性校验
- **WHEN** 尝试对 borrowed 状态的设备直接申请借用
- **THEN** 返回 409 冲突错误

### Requirement: 审核记录与状态变更追踪
系统 SHALL 在 audit_logs 表中记录每次借用审核、归还确认、工单分配、维修确认等操作，支持追溯。

#### Scenario: 审核操作记录
- **WHEN** 管理员审核借用申请
- **THEN** audit_logs 表新增一条记录，包含操作人、操作动作、状态变更前后值

### Requirement: 文件上传
系统 SHALL 支持图片上传（JPG/PNG/WebP），单张最大 5MB，最多 5 张，文件存储在 `uploads/` 目录下按类型分子目录，文件名使用 UUID+时间戳。

#### Scenario: 上传格式校验
- **WHEN** 用户上传非图片格式文件
- **THEN** 返回 422 校验失败错误

### Requirement: 分页器通用组件
前端 SHALL 提供可复用的分页器组件，支持省略号逻辑、首尾页始终显示、当前页高亮、加载状态禁用。

#### Scenario: 分页器渲染
- **WHEN** 数据总数为 100 条，每页 10 条，当前第 5 页
- **THEN** 分页器显示 [1, ..., 3, 4, 5, 6, 7, ..., 10]

### Requirement: 统一响应格式
所有 API 接口 SHALL 返回统一格式 `{ "code": 200, "msg": "success", "data": ... }`，错误码覆盖 200/400/401/403/404/409/422/500。

#### Scenario: 成功响应
- **WHEN** 任何接口调用成功
- **THEN** 返回 code=200，data 包含业务数据

### Requirement: 安全防护
系统 SHALL 实现密码 bcrypt 加密、SQLAlchemy ORM 防 SQL 注入、JWT Token 鉴权、角色权限校验、防越权（学生只能操作自己的记录）。

#### Scenario: 越权访问拦截
- **WHEN** 学生 A 尝试查看学生 B 的借用记录
- **THEN** 返回 403 权限不足错误