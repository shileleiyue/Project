# 个性化网络学习空间 · uni-app 前端骨架

> 一套代码同时编译 Web + 微信小程序
> 开发工具：HBuilderX（https://www.dcloud.io/hbuilderx.html）
> Node.js ≥ 16 + Vue 3

## 目录结构

```
learning-app/
├── App.vue                  # 应用根组件
├── main.js                  # 入口
├── pages.json               # 路由 & TabBar 配置
├── manifest.json            # 应用配置（微信小程序 appid）
├── uni.scss                 # 全局 SCSS 变量
├── static/                  # 静态资源
│   └── logo.png
├── api/
│   └── index.js             # axios 封装（和后端 /api 对接）
├── utils/
│   ├── auth.js              # token 管理
│   └── request.js           # uni.request 二次封装
├── pages/
│   ├── login/login.vue      # 登录页
│   └── index/index.vue      # 首页（登录后根据 role 跳转）
├── pages_student/
│   ├── dashboard/dashboard.vue    # 学习总览
│   ├── courses/courses.vue        # 课程学习
│   ├── exam_center/exam_center.vue # 考试中心
│   ├── exam/exam.vue              # 答题页
│   ├── wrongbook/wrongbook.vue    # 错题本
│   ├── analytics/analytics.vue    # 学习喜好分析
│   └── profile/profile.vue        # 个人资料
├── pages_teacher/
│   ├── dashboard/dashboard.vue    # 教师工作台
│   ├── courses/courses.vue        # 课程管理 + 知识点管理
│   ├── materials/materials.vue    # 资料上传
│   ├── questions/questions.vue    # 题库管理
│   └── exams/exams.vue            # 试卷管理
└── pages_admin/
    ├── dashboard/dashboard.vue    # 管理员工作台
    └── students/students.vue      # 学生信息 CRUD
```

## 快速开始

```bash
# 方法一：HBuilderX（推荐）
# 1. 安装 HBuilderX
# 2. 文件 → 打开目录 → 选择 learning-app/
# 3. 运行 → 运行到浏览器（Web）或 运行到小程序模拟器（微信开发者工具）

# 方法二：CLI 方式
npx degit dcloudio/uni-preset-vue#vite-ts learning-app
cd learning-app
npm install
npm run dev:h5        # Web 开发
npm run dev:mp-weixin # 微信小程序（需 HBuilderX 或微信开发者工具）
```

## 与当前后端的对接

后端地址：修改 `api/index.js` 中的 `BASE_URL`
```js
// 开发时用 http://127.0.0.1:8000
// 微信小程序需要在微信公众平台后台把后端域名加入 request 合法域名列表（正式 HTTPS）
export const BASE_URL = 'http://127.0.0.1:8000/api';
```

所有接口完全对齐 Django REST Framework 的后端（见 `learning_space/README.md`）。
