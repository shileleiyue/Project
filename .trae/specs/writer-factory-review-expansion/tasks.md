# Tasks

- [x] Task 1: 修复 novel_platform 合并冲突
  - 在 `novel_platform/urls.py` 中解决冲突，保留 HEAD 分支的 outline_rename/outline_delete/about 路由
  - 在 `chapters/views.py` 中解决冲突，保留 HEAD 分支的完整功能代码
  - 在所有模板文件（work_list.html, work_detail.html, chapter_read.html, outline.html, outline_node.html）中解决冲突
  - 在所有 CSS 文件（work_list.css, work_detail.css, outline.css, nav.css, work_create.css, trash.css, chapter_read.css）中解决冲突
  - 删除 `bass.css` 空文件

- [x] Task 2: 创建用户认证系统
  - 在 `chapters` 应用中添加用户注册、登录、登出视图
  - 创建 login.html, register.html 模板
  - 为 Work 模型添加 `user` 外键（ForeignKey 到 auth.User）
  - 修改所有视图，确保只返回当前用户的数据
  - 添加登录装饰器保护所有需要认证的视图

- [x] Task 3: 添加作品标签与分类功能
  - 创建 Tag 和 Category 模型
  - 为 Work 模型添加 `tags`（ManyToManyField）和 `category`（ForeignKey）字段
  - 生成并执行数据库迁移
  - 在作品创建/编辑表单中添加标签和分类选择
  - 在作品列表页展示标签和分类筛选

- [x] Task 4: 整合 Flask novel_manager 功能到 Django 平台
  - 创建 Character, Relationship, TimelineEvent, TechNode 模型（参考 Flask 版设计）
  - 生成并执行数据库迁移
  - 创建角色管理视图和模板（列表、添加、编辑、删除）
  - 创建关系管理视图和模板（列表、添加、编辑、删除），含角色选择下拉
  - 创建时间线管理视图和模板（列表、添加、编辑、删除），含角色多选关联
  - 创建科技树管理视图和模板（树形展示、添加、编辑、删除），含递归子节点
  - 在导航栏添加角色、关系、时间线、科技树的入口链接
  - 将角色与作品关联（Character 添加 work 外键）

- [x] Task 5: 添加搜索功能
  - 创建搜索视图，支持搜索作品、章节、角色
  - 在导航栏添加搜索框
  - 创建搜索结果页面模板

- [x] Task 6: 添加数据导出功能
  - 添加导出作品为 TXT 格式的功能（所有章节拼接）
  - 添加导出作品为 JSON 格式的功能（结构化的作品+章节数据）
  - 在作品详情页添加导出按钮

- [x] Task 7: 增强统计面板
  - 添加月度写作统计（月度总字数、每日趋势）
  - 添加累计字数统计
  - 添加写作目标设定功能（每日/每周目标字数）
  - 在统计面板展示目标进度

- [x] Task 8: 添加分页功能
  - 为作品列表添加分页
  - 为章节列表添加分页
  - 为角色列表添加分页

- [x] Task 9: 添加单元测试
  - 编写模型测试（Work, Chapter, Character 等）
  - 编写视图测试（CRUD 操作）
  - 编写认证测试（登录、注册、权限）
  - 运行测试确保所有测试通过

- [x] Task 10: 生产环境配置
  - 关闭 DEBUG 模式（通过环境变量控制）
  - 隐藏 SECRET_KEY（通过环境变量读取）
  - 配置 ALLOWED_HOSTS

# Task Dependencies
- [Task 2] 依赖于 [Task 1]（需要先修复冲突才能修改代码）
- [Task 3] 依赖于 [Task 2]（标签需要用户认证）
- [Task 4] 依赖于 [Task 1]（需要先修复冲突），可与 [Task 2] 并行
- [Task 5] 依赖于 [Task 4]（搜索需要包含角色）
- [Task 6] 无依赖，可并行
- [Task 7] 无依赖，可并行
- [Task 8] 无依赖，可并行
- [Task 9] 依赖于 [Task 1] 到 [Task 8]（测试整个系统）
- [Task 10] 依赖于 [Task 1]（需要稳定的代码基础）