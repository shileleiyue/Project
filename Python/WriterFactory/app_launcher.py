"""
作家工厂（Writer Factory）桌面应用入口。

运行逻辑：
1. 配置 Django 环境变量；
2. 首次启动自动执行数据库迁移（幂等）；
3. 在后台线程用 waitress 启动 Django WSGI 服务（127.0.0.1 本机端口）；
4. 等待端口就绪后，用 pywebview 打开原生窗口加载本地服务；
5. 窗口关闭即退出应用（后台线程为 daemon，随之结束）。

打包：pyinstaller WriterFactory.spec
"""
import os
import sys
import time
import socket
import threading
import traceback

# 应用名称与本机监听端口
APP_NAME = '作家工厂'
HOST = '127.0.0.1'
PORT = 8765


def _configure_env():
    """配置 Django 运行环境。"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'writer_factory.settings')
    # 让 Django 以非调试模式运行桌面服务
    os.environ.setdefault('DJANGO_DEBUG', 'False')


def _ensure_default_user():
    """首次启动自动创建默认演示账号（幂等：已存在则重置密码与权限）。

    默认账号：admin / admin123
    用户可登录后自行修改，或通过注册功能新建账号。
    """
    from django.contrib.auth.models import User
    username = 'admin'
    password = 'admin123'
    user = User.objects.filter(username=username).first()
    if user is None:
        User.objects.create_superuser(
            username=username, email='', password=password,
        )
    else:
        # 已存在则确保可用（重置密码、恢复管理员权限）
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(update_fields=['password', 'is_staff', 'is_superuser', 'is_active'])


def _init_database():
    """首次启动自动迁移建表，并确保默认账号存在。"""
    import django
    django.setup()
    from django.core.management import call_command
    call_command('migrate', interactive=False, verbosity=0)
    _ensure_default_user()


def _start_server():
    """在后台线程中启动 waitress WSGI 服务。"""
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    from waitress import serve
    # _quiet 关闭访问日志，避免窗口模式（无控制台）下的输出异常
    serve(application, host=HOST, port=PORT, threads=8, _quiet=True)


def _wait_until_ready(timeout=20.0):
    """轮询本机端口，等待 Django 服务就绪。"""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((HOST, PORT), timeout=1):
                return True
        except OSError:
            time.sleep(0.3)
    return False


def _show_error(title, message):
    """服务启动失败时的兜底提示。"""
    try:
        import webview
        webview.create_window(
            title,
            html=f'<html><body style="font-family:sans-serif;padding:40px;">'
                 f'<h2>启动失败</h2><pre style="white-space:pre-wrap;color:#c00;">'
                 f'{message}</pre></body></html>',
            width=560, height=360,
        )
        webview.start()
    except Exception:
        # webview 都不可用时写入 stderr（开发调试可见）
        sys.stderr.write(f'[{title}] {message}\n')


def main():
    _configure_env()
    try:
        _init_database()
    except Exception:
        _show_error(APP_NAME + ' - 数据库初始化失败', traceback.format_exc())
        return

    server_thread = threading.Thread(target=_start_server, daemon=True)
    server_thread.start()

    if not _wait_until_ready():
        _show_error(APP_NAME + ' - 服务未就绪', '本地服务在限定时间内未能启动，请重试。')
        return

    import webview
    webview.create_window(
        APP_NAME,
        f'http://{HOST}:{PORT}/',
        width=1280,
        height=820,
        min_size=(960, 640),
        text_select=True,
    )
    # 关闭窗口后主线程结束，daemon 服务线程随之退出
    webview.start()


if __name__ == '__main__':
    main()
