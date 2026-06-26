# 修复 FriendLink 表不存在的错误计划

## 问题描述
访问首页时抛出 `ProgrammingError: (1146, "Table 'school_db.core_friendlink' doesn't exist")`。原因是 `FriendLink` 模型已创建迁移文件，但尚未应用到数据库，而 `friend_links` 上下文处理器在模板渲染时尝试查询该表导致出错。

## 修复步骤

### Step 1: 让上下文处理器优雅处理表不存在的情况
修改 `apps/core/context_processors.py` 中的 `friend_links` 函数，用 `try-except` 捕获 `ProgrammingError` 和 `OperationalError`，当数据库表不存在时返回空列表，避免影响首页正常渲染。

### Step 2: 应用数据库迁移
在终端运行 `python manage.py migrate core` 命令，创建 `core_friendlink` 表。

### Step 3: 验证修复
- 访问首页，确认不再报错
- 检查 `friend_links` 上下文处理器正常返回空列表或数据

## 涉及文件
- `d:\IST\Project\School-Web\school_site\apps\core\context_processors.py` — 需要修改
- `d:\IST\Project\School-Web\School-venv\Scripts\python.exe` — 用于运行迁移命令