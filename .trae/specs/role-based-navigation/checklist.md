# Checklist

## 角色扩展
- [x] Task 1: User 模型 ROLE_CHOICES 新增 5 个角色（head_teacher, academic_director, principal, counselor, staff），迁移文件已生成

## 导航菜单上下文处理器
- [x] Task 2: `nav_menu` 上下文处理器已实现，访客返回完整菜单，各角色返回对应精简菜单，已在 settings.py 注册

## 导航栏动态渲染
- [x] Task 3: base.html 桌面端和移动端导航栏均改为动态遍历 `nav_items` 渲染，支持下拉子菜单

## 管理员后台
- [x] Task 4: admin.py 中角色字段在列表显示、筛选和编辑表单中可用

## 系统验证
- [x] Task 5: `python manage.py check` 通过，所有页面模板正常渲染