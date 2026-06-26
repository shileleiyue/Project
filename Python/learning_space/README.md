# 个性化网络学习空间 (Personalized E-Learning Platform)

**Django 5 + Django REST Framework + MySQL + Vue 3 (uni-app 可选)**

---

## 功能总览

| 模块 | 学生 | 教师 | 管理员 |
|---|---|---|---|
| 登录/注册/JWT | ✅ | ✅ | ✅ |
| 个人资料查看/修改 | ✅ (含联系方式) | ✅ | ✅ |
| **学生 CRUD** | ❌ | ❌ | ✅ (姓名/学号/联系方式/学院/课程/成绩) |
| **课程/知识点管理** | 只读 | ✅ | 只读 |
| **学习资料上传** | ❌ | ✅ (文档/视频/外链) | 只读 |
| **题库管理** | ❌ | ✅ (单选/多选/判断) | 只读 |
| **试卷管理/发布** | ❌ | ✅ | ❌ |
| **在线考试 + 自动评分** | ✅ | 看全班成绩 | ❌ |
| **错题本 + 相关资料推荐** | ✅ | ❌ | ❌ |
| **学习强度/情况统计** | ✅ | ❌ | ❌ |
| **学习喜好分析** | ✅ | ❌ | ❌ |
| **个性化资料推荐** | ✅ | ❌ | ❌ |

## 快速开始（一键）

```powershell
cd d:\IST\Project\Python\learning_space
.\start.ps1
```

然后浏览器打开 **http://127.0.0.1:8080**

## 手动步骤

```bash
# 1. 创建虚拟环境 + 安装依赖
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# 2. 数据库迁移（默认 SQLite，切 MySQL 见 MYSQL_SWITCH.md）
python manage.py migrate

# 3. 导入种子数据（3 个账号 + 课程 + 知识点 + 题库 + 试卷 + 资料）
python manage.py shell -c "exec(open('seed.py', encoding='utf-8').read())"

# 4. 启动后端（8000） + 前端静态服务器（8080）
python manage.py runserver 0.0.0.0:8000       # 后端
cd frontend && python -m http.server 8080     # 前端
```

## 测试账号（seed.py 导入）

| 角色 | 用户名 | 密码 |
|---|---|---|
| 管理员 | admin | admin123 |
| 教师 | teacher | teacher123 |
| 学生 | student | student123 |

## 核心目录

```
learning_space/
├── config/                 # Django 配置 (settings.py / urls.py)
├── accounts/               # 用户体系（自定义 User + 权限类）
├── courses/                # 课程 + 知识点（树形）
├── materials/              # 学习资料（文档/视频/外链）
├── exams/                  # 题库 + 试卷 + 考试 + 自动评分
├── analytics/              # 学习统计 + 薄弱点 + 喜好 + 推荐
├── frontend/               # Vue 3 CDN 版前端（零构建）
│   ├── index.html          # 登录页
│   ├── app.html            # 主应用壳
│   ├── css/app.css
│   └── js/
│       ├── api.js          # axios 封装（自动补 trailing slash）
│       └── pages.js        # 所有角色页面组件
├── mysql_init.sql          # MySQL 建库脚本
├── MYSQL_SWITCH.md         # 切换 MySQL 指南
├── UNIAPP.md               # uni-app (Web+微信小程序) 脚手架说明
├── seed.py                 # 种子数据
└── start.ps1               # 一键启动脚本
```

## API 概览（http://127.0.0.1:8000/api/docs/ Swagger）

```
POST   /api/auth/login/            # 登录 (JWT)
POST   /api/auth/register/         # 注册
GET/PUT /api/auth/me/              # 本人信息
GET    /api/students/              # 管理员：学生列表
POST   /api/students/              # 管理员：批量建学生（同时建 User + Student）
GET    /api/students/me/           # 学生：自己
GET/PUT /api/students/{id}/        # 管理员 CRUD
GET    /api/courses/               # 课程列表
POST   /api/courses/               # 教师：新建
GET    /api/courses/{id}/knowledge/ # 知识点树
GET    /api/materials/             # 资料列表
POST   /api/materials/             # 教师：上传
POST   /api/materials/{id}/view/   # 学生：上报学习行为
GET    /api/questions/             # 题库
POST   /api/questions/             # 教师：新建
GET    /api/exams/                 # 试卷列表
POST   /api/exams/                 # 教师：创建（带 items）
POST   /api/exams/{id}/publish/    # 发布
POST   /api/exams/{id}/start/      # 学生：开考
POST   /api/exams/{id}/submit/     # 学生：交卷（自动评分）
GET    /api/exam-records/{id}/wrong/ # 错题 + 相关资料
GET    /api/stats/overview/        # 学习总览
GET    /api/stats/daily-trend/     # 近 7 天
GET    /api/stats/weak-points/     # 薄弱知识点
GET    /api/stats/preferences/     # 学习喜好分析
GET    /api/stats/recommendations/ # 推荐资料
```

## 技术亮点

- **RBAC 权限体系**：`IsAdmin / IsTeacher / IsStudent / IsOwnerOrAdmin / IsTeacherOrAdmin` 5 个自定义权限类
- **自动评分**：单选/多选/判断题全部实现，多选题集合比较
- **错题驱动的推荐**：根据错题数 + 掌握度 → 薄弱知识点 → 该知识点下未看过的资料
- **学习喜好分析**：从 MaterialView 记录自动生成活跃时段分布 + 学科权重 + 偏好资料类型
- **JWT 鉴权**：SimpleJWT，访问 6 小时 / 刷新 7 天
- **前端零构建**：Vue 3 + Element Plus CDN 版，浏览器直接打开

## 切 MySQL（一步）

编辑 `config/settings.py`，把 `DATABASES` 段注释换成：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'learning_space',
        'USER': 'root',
        'PASSWORD': 'YOUR_ROOT_PASSWORD',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
```

然后：

```bash
mysql -u root -p < mysql_init.sql
python manage.py migrate
python manage.py shell -c "exec(open('seed.py').read())"
```

## 切 uni-app（Web + 微信小程序）

详见 `UNIAPP.md`。需要：HBuilderX + Node.js 16+。后端 API 完全兼容，只需改 `BASE_URL`。

---

© 2026 Personalized E-Learning Platform · Powered by Django REST Framework
