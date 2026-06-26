# Tasks

## Task 1: 扩展 User 模型角色字段
- [x] 修改 `apps/accounts/models.py`，在 `ROLE_CHOICES` 中新增 `head_teacher`、`academic_director`、`principal`、`counselor`、`staff` 角色选项
- [x] 创建并运行数据库迁移

## Task 2: 实现导航菜单上下文处理器
- [x] 在 `apps/accounts/context_processors.py` 中新增 `nav_menu` 函数
- [x] 定义 10 种角色的导航菜单数据结构（字典，包含 name、url、children）
- [x] 未登录时返回完整公开菜单
- [x] 已登录时根据 `request.user.role` 返回对应精简菜单
- [x] 在 `settings.py` 的 `TEMPLATES.OPTIONS.context_processors` 中注册 `nav_menu`

## Task 3: 改造 base.html 导航栏为动态渲染
- [x] 桌面端导航栏改为 `{% for item in nav_items %}` 遍历渲染
- [x] 移动端导航栏改为同样遍历 `nav_items` 渲染
- [x] 支持一级菜单项和带子菜单的下拉项（`item.children`）
- [x] 保持现有 CSS 类和结构兼容性

## Task 4: 管理员后台用户列表优化
- [x] 修改 `apps/accounts/admin.py`，list_display/list_filter 已含 role，新增 search_fields 支持真实姓名搜索
- [x] role 字段在后台编辑表单中可见

## Task 5: 验证与测试
- [x] 执行 `python manage.py check` 确认无错误
- [x] 验证迁移文件生成正确
- [x] 确认所有现有页面模板不受影响

# Task Dependencies
- [Task 2] 依赖于 [Task 1]（上下文处理器需要新的角色名称）
- [Task 3] 依赖于 [Task 2]（base.html 需要 `nav_items` 变量）
- [Task 4] 独立，可并行执行
- [Task 5] 依赖于所有任务完成