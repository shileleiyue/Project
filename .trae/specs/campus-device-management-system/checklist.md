# Checklist

## 前端项目骨架
- [x] `campus-device/` 目录结构完整，包含 css/、js/、pages/、assets/images/ 子目录
- [x] `css/reset.css` 样式重置文件存在且内容正确
- [x] `css/variables.css` CSS 变量文件存在，包含颜色、字号、圆角、阴影等主题变量
- [x] `css/common.css` 公共样式文件存在，包含按钮、表单、卡片、弹窗、状态标签样式
- [x] `css/layout.css` 布局样式文件存在，包含导航栏、侧边栏、内容区样式
- [x] `js/config.js` 全局配置文件存在，包含 API_BASE_URL
- [x] `js/utils.js` 工具函数文件存在，包含日期格式化、防抖节流等
- [x] `js/storage.js` localStorage 封装文件存在，包含 token 和用户信息读写
- [x] `js/api.js` API 封装层文件存在，支持 GET/POST/PUT/DELETE、自动附带 Token、401 拦截
- [x] `js/auth.js` 鉴权模块文件存在，包含 checkAuth 路由守卫函数
- [x] `js/toast.js` 消息提示组件文件存在
- [x] `js/modal.js` 弹窗组件文件存在
- [x] `js/paginator.js` 分页器组件文件存在，支持省略号逻辑
- [x] `js/upload.js` 文件上传组件文件存在，支持格式和大小校验
- [x] `js/app.js` 主入口文件存在
- [x] `js/audit.js` 审核记录查看组件存在

## 后端项目骨架
- [x] `campus-device-backend/` 目录结构完整，包含 app/、uploads/、tests/ 子目录
- [x] `app/main.py` 应用入口文件存在，包含 CORS 中间件和路由注册
- [x] `app/config.py` 配置文件存在，包含数据库、JWT、文件路径配置
- [x] `app/utils/response_util.py` 统一响应格式工具存在
- [x] `app/utils/jwt_util.py` JWT 工具存在
- [x] `app/utils/password_util.py` 密码加密工具存在（bcrypt）
- [x] `app/utils/file_util.py` 文件处理工具存在
- [x] `app/dependencies.py` 依赖注入存在（get_current_user、require_role、分页参数）
- [x] `app/middleware/cors_middleware.py` CORS 中间件存在
- [x] `requirements.txt` 依赖清单存在，包含 fastapi、uvicorn、sqlalchemy、python-jose、passlib、bcrypt、pydantic 等
- [x] `.env` 环境变量模板和 `.gitignore` 存在

## 数据库模型
- [x] `app/models/__init__.py` 数据库连接与 Base 声明存在
- [x] `app/models/user.py` users 表模型存在，字段完整（id、username、phone、email、password_hash、role、avatar、is_active、created_at、updated_at）
- [x] `app/models/device.py` devices 表模型存在，字段完整（id、name、type、description、image、status、location、created_by、created_at、updated_at）
- [x] `app/models/borrow.py` borrows 表模型存在，字段完整（id、device_id、user_id、status、borrow_reason、borrow_time、expected_return_time、actual_return_time、return_status、damage_description、audit_by、audit_time、audit_remark、created_at、updated_at）
- [x] `app/models/repair.py` repairs 表和 repair_images 表模型存在，字段完整
- [x] `app/models/audit.py` audit_logs 表模型存在，字段完整

## 认证模块
- [x] `app/schemas/user.py` 用户 Pydantic 模型存在
- [x] `app/schemas/common.py` 公共模型存在（分页、统一响应）
- [x] `app/repositories/user_repo.py` 用户数据访问层存在
- [x] `app/services/auth_service.py` 认证业务逻辑存在（注册、登录、获取当前用户）
- [x] `app/routers/auth.py` 认证接口路由存在（POST /login、POST /register、POST /logout、GET /me）
- [x] 密码使用 bcrypt 加盐哈希存储
- [x] 登录成功返回 JWT Token
- [x] Token 过期返回 401

## 设备管理模块
- [x] `app/schemas/device.py` 设备 Pydantic 模型存在
- [x] `app/repositories/device_repo.py` 设备数据访问层存在（支持分页、搜索、筛选）
- [x] `app/services/device_service.py` 设备业务逻辑存在（CRUD、下架）
- [x] `app/routers/device.py` 设备接口路由存在（GET 列表/详情、POST 新增、PUT 编辑/下架、DELETE 删除）
- [x] 分页响应格式包含 list、total、page、page_size、total_pages

## 借用管理模块
- [x] `app/schemas/borrow.py` 借用 Pydantic 模型存在
- [x] `app/repositories/borrow_repo.py` 借用数据访问层存在
- [x] `app/services/borrow_service.py` 借用业务逻辑存在（申请、审核、归还、确认归还）
- [x] `app/routers/borrow.py` 借用接口路由存在（POST 申请、GET 列表/我的、PUT 审核/归还/确认归还）
- [x] 设备状态随借用流程自动流转（available → pending_borrow → borrowed → pending_return → available/damaged）
- [x] 学生只能操作自己的借用记录

## 维修管理模块
- [x] `app/schemas/repair.py` 维修 Pydantic 模型存在
- [x] `app/repositories/repair_repo.py` 维修数据访问层存在
- [x] `app/services/repair_service.py` 维修业务逻辑存在（创建工单、分配、状态更新、确认、图片管理）
- [x] `app/routers/repair.py` 维修接口路由存在（POST 创建、GET 列表/我的/分配/详情、PUT 分配/状态/确认、POST 上传图片）
- [x] 设备状态随维修流程自动流转（damaged → repair_pending → repairing → repaired → available/scrapped）
- [x] 维修人员只能查看分配给自己的工单

## 审核记录
- [x] borrow_service 和 repair_service 中集成了 audit_log 记录逻辑
- [x] 每次状态变更操作自动记录到 audit_logs 表
- [x] audit router 提供 GET /api/audit-logs 查询接口
- [x] 前端 audit.js 组件支持审核记录弹窗查看
- [x] admin-borrows.html 和 admin-repairs.html 中集成审核记录查看按钮

## 文件上传
- [x] `uploads/` 子目录结构存在（avatars/、devices/、damage/、repair/）
- [x] 图片上传支持 JPG/PNG/WebP 格式校验
- [x] 单张图片大小限制 5MB
- [x] 文件命名使用 UUID+时间戳

## 前端页面
- [x] `login.html` 登录页面存在，包含手机号+密码表单
- [x] `register.html` 注册页面存在
- [x] `index.html` 设备大厅页面存在，包含设备列表、搜索、筛选、分页
- [x] `pages/device-detail.html` 设备详情页存在
- [x] `pages/my-borrows.html` 我的借用记录页存在，支持归还操作和损坏上报
- [x] `pages/my-repairs.html` 我的报修记录页存在
- [x] `pages/admin-devices.html` 管理设备页存在，支持 CRUD 操作
- [x] `pages/admin-borrows.html` 审核借用页存在，含审核记录查看按钮
- [x] `pages/admin-repairs.html` 管理报修页存在，支持工单创建和分配，含审核记录查看按钮
- [x] `pages/repair-tasks.html` 维修工单列表页存在
- [x] `pages/repair-detail.html` 维修详情页存在，支持状态更新和凭证上传
- [x] 所有页面包含路由守卫（auth.js checkAuth）
- [x] 导航栏根据角色显示不同菜单

## 测试与文档
- [x] `tests/test_auth.py` 认证模块测试存在（15个测试用例）
- [x] `tests/test_device.py` 设备模块测试存在（15个测试用例）
- [x] `tests/test_borrow.py` 借用模块测试存在（11个测试用例）
- [x] `tests/test_repair.py` 维修模块测试存在（13个测试用例）
- [x] `tests/test_audit.py` 审核记录模块测试存在（6个测试用例）
- [x] `tests/conftest.py` 测试配置存在（SQLite 数据库，无需 MySQL）
- [x] `campus-device-backend/README.md` 后端项目说明存在（含审核模块）
- [x] `get_current_user` 返回 TokenPayload 对象（.id/.role 属性），路由正确访问