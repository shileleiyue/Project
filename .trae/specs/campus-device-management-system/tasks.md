# Tasks

## 阶段一：项目骨架搭建

- [x] Task 1: 搭建前端项目骨架
  - [ ] SubTask 1.1: 创建 `campus-device/` 目录结构（css/、js/、pages/、assets/images/）
  - [ ] SubTask 1.2: 创建 `css/reset.css` 样式重置文件
  - [ ] SubTask 1.3: 创建 `css/variables.css` CSS 变量主题文件（颜色、字号、圆角、阴影）
  - [ ] SubTask 1.4: 创建 `css/common.css` 公共样式（按钮、表单、卡片、弹窗、状态标签）
  - [ ] SubTask 1.5: 创建 `css/layout.css` 布局样式（导航栏、侧边栏、内容区）
  - [ ] SubTask 1.6: 创建 `js/config.js` 全局配置（API_BASE_URL 等）
  - [ ] SubTask 1.7: 创建 `js/utils.js` 工具函数（日期格式化、防抖节流等）
  - [ ] SubTask 1.8: 创建 `js/storage.js` localStorage 封装（token、用户信息读写）
  - [ ] SubTask 1.9: 创建 `js/api.js` API 请求封装层（统一 fetch、自动附带 Token、401 拦截）
  - [ ] SubTask 1.10: 创建 `js/auth.js` 登录/鉴权/路由守卫模块
  - [ ] SubTask 1.11: 创建 `js/toast.js` 消息提示组件
  - [ ] SubTask 1.12: 创建 `js/modal.js` 弹窗组件（确认弹窗、表单弹窗）
  - [ ] SubTask 1.13: 创建 `js/paginator.js` 分页器通用组件
  - [ ] SubTask 1.14: 创建 `js/upload.js` 文件上传组件（校验、预览）
  - [ ] SubTask 1.15: 创建 `js/app.js` 主入口/路由分发

- [x] Task 2: 搭建后端项目骨架
  - [ ] SubTask 2.1: 创建 `campus-device-backend/` 目录结构
  - [ ] SubTask 2.2: 创建 `app/main.py` FastAPI 应用入口（含 CORS 中间件、路由注册）
  - [ ] SubTask 2.3: 创建 `app/config.py` 配置管理（数据库连接、JWT 密钥、文件路径）
  - [ ] SubTask 2.4: 创建 `app/utils/response_util.py` 统一响应格式工具
  - [ ] SubTask 2.5: 创建 `app/utils/jwt_util.py` JWT 生成/验证工具
  - [ ] SubTask 2.6: 创建 `app/utils/password_util.py` 密码加密/校验工具（bcrypt）
  - [ ] SubTask 2.7: 创建 `app/utils/file_util.py` 文件处理工具
  - [ ] SubTask 2.8: 创建 `app/dependencies.py` 依赖注入（get_current_user、require_role、分页参数）
  - [ ] SubTask 2.9: 创建 `app/middleware/cors_middleware.py` CORS 中间件
  - [ ] SubTask 2.10: 创建 `requirements.txt` 依赖清单
  - [ ] SubTask 2.11: 创建 `.env` 环境变量模板和 `.gitignore`

## 阶段二：数据库与认证模块

- [x] Task 3: 数据库模型设计与创建
  - [ ] SubTask 3.1: 创建 `app/models/__init__.py` 数据库连接与 Base 声明
  - [ ] SubTask 3.2: 创建 `app/models/user.py` 用户模型（users 表）
  - [ ] SubTask 3.3: 创建 `app/models/device.py` 设备模型（devices 表）
  - [ ] SubTask 3.4: 创建 `app/models/borrow.py` 借用记录模型（borrows 表）
  - [ ] SubTask 3.5: 创建 `app/models/repair.py` 维修工单模型（repairs 表 + repair_images 表）
  - [ ] SubTask 3.6: 创建 `app/models/audit.py` 审核/状态变更记录模型（audit_logs 表）

- [x] Task 4: 认证模块实现
  - [ ] SubTask 4.1: 创建 `app/schemas/user.py` 用户请求/响应 Pydantic 模型
  - [ ] SubTask 4.2: 创建 `app/schemas/common.py` 公共模型（分页、统一响应）
  - [ ] SubTask 4.3: 创建 `app/repositories/user_repo.py` 用户数据访问层
  - [ ] SubTask 4.4: 创建 `app/services/auth_service.py` 认证业务逻辑（注册、登录、获取当前用户）
  - [ ] SubTask 4.5: 创建 `app/routers/auth.py` 认证接口路由（POST /login、POST /register、POST /logout、GET /me）

## 阶段三：设备管理模块

- [x] Task 5: 设备管理模块实现
  - [ ] SubTask 5.1: 创建 `app/schemas/device.py` 设备请求/响应 Pydantic 模型
  - [ ] SubTask 5.2: 创建 `app/repositories/device_repo.py` 设备数据访问层（分页、搜索、筛选）
  - [ ] SubTask 5.3: 创建 `app/services/device_service.py` 设备业务逻辑（CRUD、下架、状态校验）
  - [ ] SubTask 5.4: 创建 `app/routers/device.py` 设备接口路由（GET 列表/详情、POST 新增、PUT 编辑/下架、DELETE 删除）

## 阶段四：借用管理模块

- [x] Task 6: 借用管理模块实现
  - [ ] SubTask 6.1: 创建 `app/schemas/borrow.py` 借用请求/响应 Pydantic 模型
  - [ ] SubTask 6.2: 创建 `app/repositories/borrow_repo.py` 借用数据访问层
  - [ ] SubTask 6.3: 创建 `app/services/borrow_service.py` 借用业务逻辑（申请、审核、归还、确认归还、状态流转）
  - [ ] SubTask 6.4: 创建 `app/routers/borrow.py` 借用接口路由（POST 申请、GET 列表/我的、PUT 审核/归还/确认归还）

## 阶段五：维修管理模块

- [x] Task 7: 维修管理模块实现
  - [ ] SubTask 7.1: 创建 `app/schemas/repair.py` 维修请求/响应 Pydantic 模型
  - [ ] SubTask 7.2: 创建 `app/repositories/repair_repo.py` 维修数据访问层
  - [ ] SubTask 7.3: 创建 `app/services/repair_service.py` 维修业务逻辑（创建工单、分配、状态更新、确认、图片管理）
  - [ ] SubTask 7.4: 创建 `app/routers/repair.py` 维修接口路由（POST 创建、GET 列表/我的/分配/详情、PUT 分配/状态/确认、POST 上传图片）

## 阶段六：前端页面实现

- [x] Task 8: 登录与注册页面
  - [ ] SubTask 8.1: 创建 `login.html` + `css/login.css` 登录页面（手机号+密码表单、登录逻辑）
  - [ ] SubTask 8.2: 创建 `register.html` 注册页面（用户名+手机号+密码+角色选择表单）

- [x] Task 9: 设备大厅页面（首页）
  - [ ] SubTask 9.1: 创建 `index.html` + `css/device.css` 设备大厅页面（设备卡片列表、搜索栏、类型/状态筛选、分页器）
  - [ ] SubTask 9.2: 创建 `js/device.js` 设备模块逻辑（加载列表、搜索、筛选、分页）

- [x] Task 10: 设备详情页
  - [ ] SubTask 10.1: 创建 `pages/device-detail.html` 设备详情页（设备信息展示、借用申请按钮）

- [x] Task 11: 借用相关页面
  - [ ] SubTask 11.1: 创建 `pages/my-borrows.html` + `js/borrow.js` + `css/borrow.css` 我的借用记录页（列表、归还操作、损坏上报含图片上传）
  - [ ] SubTask 11.2: 创建 `pages/my-repairs.html` 我的报修记录页（报修列表及进度查看）

- [x] Task 12: 管理后台页面
  - [ ] SubTask 12.1: 创建 `pages/admin-devices.html` + `js/admin.js` + `css/admin.css` 管理设备页（设备 CRUD 操作界面）
  - [ ] SubTask 12.2: 创建 `pages/admin-borrows.html` 审核借用页（借用申请列表、审核操作）
  - [ ] SubTask 12.3: 创建 `pages/admin-repairs.html` 管理报修页（工单创建、分配维修人员、确认维修）

- [x] Task 13: 维修端页面
  - [ ] SubTask 13.1: 创建 `pages/repair-tasks.html` + `js/repair.js` + `css/repair.css` 维修工单列表页
  - [ ] SubTask 13.2: 创建 `pages/repair-detail.html` 维修详情页（状态更新、凭证上传）

## 阶段七：审核记录与文件上传

- [x] Task 14: 审核记录模块
  - [x] SubTask 14.1: 在 borrow_service 和 repair_service 中集成 audit_log 记录逻辑
  - [x] SubTask 14.2: 创建 `app/routers/audit.py` 审核记录查询接口
  - [x] SubTask 14.3: 创建 `js/audit.js` 前端审核记录查看组件
  - [x] SubTask 14.4: 在 admin-borrows.html 和 admin-repairs.html 中集成审核记录查看按钮

- [x] Task 15: 文件上传功能完善
  - [x] SubTask 15.1: 在 `app/routers/repair.py` 中完善图片上传接口（多图上传、格式校验、大小限制）
  - [x] SubTask 15.2: 创建 `uploads/` 子目录结构（avatars/、devices/、damage/、repair/）

## 阶段八：测试与收尾

- [x] Task 16: 后端测试
  - [x] SubTask 16.1: 创建 `tests/test_auth.py` 认证模块测试（15个测试用例）
  - [x] SubTask 16.2: 创建 `tests/test_device.py` 设备模块测试（15个测试用例）
  - [x] SubTask 16.3: 创建 `tests/test_borrow.py` 借用模块测试（11个测试用例）
  - [x] SubTask 16.4: 创建 `tests/test_repair.py` 维修模块测试（13个测试用例）
  - [x] SubTask 16.5: 创建 `tests/test_audit.py` 审核记录模块测试（6个测试用例）
  - [x] SubTask 16.6: 创建 `tests/conftest.py` 测试配置（SQLite 内存数据库，无需 MySQL）

- [x] Task 17: 项目文档
  - [x] SubTask 17.1: 创建 `campus-device-backend/README.md` 后端项目说明

# Task Dependencies
- Task 2（后端骨架）依赖 Task 1（前端骨架），可并行执行
- Task 3（数据库模型）依赖 Task 2（后端骨架）
- Task 4（认证模块）依赖 Task 3（数据库模型）
- Task 5（设备模块）依赖 Task 3、Task 4
- Task 6（借用模块）依赖 Task 5（设备模块）
- Task 7（维修模块）依赖 Task 5、Task 6
- Task 8-13（前端页面）依赖 Task 1（前端骨架），可与 Task 3-7 并行执行
- Task 14（审核记录）依赖 Task 6、Task 7
- Task 15（文件上传）依赖 Task 7
- Task 16（测试）依赖 Task 4-7 全部完成
- Task 17（文档）依赖所有任务完成