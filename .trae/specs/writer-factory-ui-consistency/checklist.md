# 检查清单

## 共享CSS组件库
- [x] `nav.css` 包含全局 `.btn` 系列样式
- [x] `nav.css` 包含全局 `.card`、`.form-group`、`.form-control` 样式
- [x] `nav.css` 包含全局 `.table`、`.empty-state`、`.back-link` 样式
- [x] 所有组件使用CSS变量而非硬编码值

## 登录/注册页UI统一
- [x] 登录页使用玻璃拟态风格
- [x] 登录页使用 `--color-primary` 替代 `#4A90D9`
- [x] 注册页与登录页风格一致
- [x] 登录/注册页内联CSS已移除（复用全局样式）

## 新功能模块UI统一
- [x] 角色列表/表单页使用玻璃拟态风格
- [x] 关系列表/表单页使用玻璃拟态风格
- [x] 时间线列表/表单页使用玻璃拟态风格
- [x] 科技树列表/表单页使用玻璃拟态风格
- [x] 所有页面的按钮、卡片、表格使用CSS变量

## 独立模板继承base.html
- [x] about.html 继承 base.html
- [x] trash.html 继承 base.html
- [x] work_create.html 继承 base.html
- [x] work_detail.html 继承 base.html
- [x] chapter_read.html 继承 base.html
- [x] outline.html 继承 base.html
- [x] 所有页面包含导航栏和页脚（共19个模板继承base.html）

## 导航栏增强
- [x] 导航栏显示当前用户名
- [x] 导航栏包含登出按钮
- [x] 未登录用户显示登录/注册链接
- [x] 导航栏下拉菜单中 `works` 变量正常工作

## 代码修复
- [x] 所有视图传递 `works` 变量到模板上下文
- [x] `stats.html` 中 `chart_items` 与 `chart_data_json` 一致
- [x] `search.css` 文件存在且内容正确
- [x] 所有24个测试通过（`python manage.py test chapters`）