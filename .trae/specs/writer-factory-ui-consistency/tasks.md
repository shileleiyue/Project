# Tasks

- [x] Task 1: 创建共享CSS组件库
  - 在 `nav.css` 中补充全局组件样式（`.btn`, `.btn-primary`, `.btn-danger`, `.btn-sm`, `.btn-secondary`, `.btn-success`）
  - 添加全局 `.card`, `.form-group`, `.form-control`, `.table`, `.empty-state`, `.back-link` 样式
  - 所有样式使用已有CSS变量（`--color-primary`, `--color-accent` 等）
  - 添加玻璃拟态卡片样式（`.glass-card`）

- [x] Task 2: 统一登录/注册页UI
  - 移除 `login.html` 和 `register.html` 中的内联CSS
  - 复用 `nav.css` 中的CSS变量和全局组件样式
  - 应用玻璃拟态效果（渐变背景、模糊卡片、渐变边框）
  - 使用 `--color-primary` 替代硬编码 `#4A90D9`

- [x] Task 3: 统一新功能模块UI（角色/关系/时间线/科技树）
  - 移除 `character_list.html`, `character_form.html`, `relationship_list.html`, `relationship_form.html`, `timeline_list.html`, `timeline_form.html`, `tech_tree.html`, `tech_tree_node.html`, `tech_form.html` 中的内联CSS
  - 复用 `nav.css` 中的全局组件样式
  - 使用 `--color-primary` 替代硬编码 `#4A90D9`
  - 应用玻璃拟态风格

- [x] Task 4: 将独立模板改为继承base.html
  - 将 `about.html` 改为 `{% extends 'chapters/base.html' %}`，移除重复的 `<html>` 结构
  - 将 `trash.html` 改为 `{% extends 'chapters/base.html' %}`
  - 将 `work_create.html` 改为 `{% extends 'chapters/base.html' %}`
  - 将 `work_detail.html` 改为 `{% extends 'chapters/base.html' %}`
  - 将 `chapter_read.html` 改为 `{% extends 'chapters/base.html' %}`
  - 将 `outline.html` 改为 `{% extends 'chapters/base.html' %}`
  - 每个模板保留自身特有的样式和内容块，继承导航栏和页脚

- [x] Task 5: 导航栏增强
  - 在 `base.html` 导航栏右侧添加用户信息显示（`{{ request.user.username }}`）
  - 添加登出按钮（`{% url 'logout' %}`）
  - 未登录用户显示登录/注册链接
  - 修复 `works` 变量在导航栏下拉菜单中的可用性
  - 保持导航栏样式一致

- [x] Task 6: 修复视图上下文
  - 确保所有视图在渲染模板时传递 `works` 变量（用于导航栏下拉菜单）
  - 修复 `stats.html` 中 `chart_items` 与 `chart_data_json` 的不一致
  - 检查并创建缺失的 `search.css` 文件
  - 运行测试确保所有功能正常

# Task Dependencies
- [Task 1] 独立，可先执行（创建共享CSS）
- [Task 2] 依赖于 [Task 1]（需要共享CSS）
- [Task 3] 依赖于 [Task 1]（需要共享CSS）
- [Task 4] 依赖于 [Task 5]（导航栏完善后继承更有意义）
- [Task 5] 独立，可与 [Task 1] 并行
- [Task 6] 依赖于 [Task 1] 到 [Task 5]（最终修复和验证）