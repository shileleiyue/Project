# 校园设备借用与维修管理系统 - 后端

## 技术栈
- Python 3.10+
- FastAPI
- SQLAlchemy 2.0 (异步)
- MySQL 8.0
- JWT 认证
- bcrypt 密码加密

## 项目结构
```
app/
├── main.py          # FastAPI 应用入口
├── config.py        # 配置管理
├── dependencies.py  # 依赖注入
├── models/          # SQLAlchemy 数据模型
├── schemas/         # Pydantic 校验模型
├── routers/         # API 路由
├── services/        # 业务逻辑层
├── repositories/    # 数据访问层
├── middleware/       # 中间件
├── utils/           # 工具函数
└── uploads/         # 上传文件存储
```

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境变量
编辑 `.env` 文件，配置数据库连接和 JWT 密钥。

### 3. 创建数据库
```sql
CREATE DATABASE campus_device CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 启动服务
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 访问 API 文档
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 模块

| 模块 | 前缀 | 说明 |
|------|------|------|
| 认证 | /api/auth | 注册、登录、退出、获取当前用户 |
| 设备 | /api/devices | 设备 CRUD、列表查询 |
| 借用 | /api/borrows | 借用申请、审核、归还 |
| 维修 | /api/repairs | 工单管理、分配、状态更新 |
| 审核 | /api | 审核日志查询 |

## 角色权限
- student: 借用设备、归还设备、查看自己的记录
- admin: 管理设备、审核借用、管理维修工单
- repairer: 查看分配工单、更新维修状态