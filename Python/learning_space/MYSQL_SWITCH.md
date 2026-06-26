"""
将 Django 数据库从 SQLite 切换到 MySQL

步骤：
  1. 确保 MySQL 已启动，执行 mysql_init.sql 创建数据库
  2. 编辑 config/settings.py，找到 DATABASES 部分，
     把默认的 SQLite 注释掉，启用下面 MySQL 那段（填好密码）
  3. 在项目根目录运行：
        python manage.py migrate           # 建表
        python manage.py shell -c "exec(open('seed.py').read())"  # 导入种子数据
  4. 重启 Django runserver 即可

验证：
  python manage.py check
  浏览器访问 http://127.0.0.1:8000/api/docs/ 看 Swagger 是否正常
"""
