"""
Django settings for writer_factory project.

作家工厂（Writer Factory）桌面应用配置。

本配置同时支持两种运行模式：
- 开发模式（python manage.py runserver）：源码运行，数据库在项目目录。
- 打包模式（PyInstaller 生成的 exe，sys.frozen=True）：
  只读资源（模板/静态文件）从 PyInstaller 解包目录（sys._MEIPASS）读取；
  可写数据（SQLite 数据库、封面图、密钥）放到用户目录 %LOCALAPPDATA%/WriterFactory，
  避免覆盖安装时丢失用户数据。
"""
import os
import sys
import secrets
from pathlib import Path

# ---------------------------------------------------------------------------
# 路径判定
# ---------------------------------------------------------------------------
def _is_frozen() -> bool:
    """是否运行在 PyInstaller 打包后的环境中。"""
    return getattr(sys, 'frozen', False)


IS_FROZEN = _is_frozen()

if IS_FROZEN:
    # PyInstaller 解包出的只读资源目录（模板、静态文件、Python 包）
    RESOURCE_DIR = Path(sys._MEIPASS)  # type: ignore[attr-defined]
    # 默认用户可写数据目录：C:\Users\<用户>\AppData\Local\WriterFactory
    _appdata = os.environ.get('LOCALAPPDATA') or os.path.expanduser('~')
    DEFAULT_DATA_DIR = Path(_appdata) / 'WriterFactory'
else:
    # 开发模式：项目根目录（manage.py 所在目录）
    RESOURCE_DIR = Path(__file__).resolve().parent.parent
    DEFAULT_DATA_DIR = RESOURCE_DIR

# 数据目录可由用户在"设置"中修改（引导配置记录自定义位置）
from core import app_config  # noqa: E402
DATA_DIR = app_config.resolve_data_dir(DEFAULT_DATA_DIR)

DATA_DIR.mkdir(parents=True, exist_ok=True)
(DATA_DIR / 'media').mkdir(parents=True, exist_ok=True)

# 加载完整应用配置（主题、分页、字号等）
APP_CONFIG = app_config.load_config(DATA_DIR)

BASE_DIR = RESOURCE_DIR


# ---------------------------------------------------------------------------
# 安全配置
# ---------------------------------------------------------------------------
def _load_or_create_secret_key() -> str:
    """打包模式下密钥持久化到用户目录，首次启动随机生成；开发模式用内置默认值。"""
    env_key = os.environ.get('DJANGO_SECRET_KEY')
    if env_key:
        return env_key

    key_file = DATA_DIR / 'secret_key.txt'
    if key_file.exists():
        return key_file.read_text(encoding='utf-8').strip()

    generated = 'django-insecure-' + secrets.token_urlsafe(50)
    try:
        key_file.write_text(generated, encoding='utf-8')
    except OSError:
        # 用户目录不可写时退回内存密钥（每次重启会失效，仅兜底）
        pass
    return generated


SECRET_KEY = _load_or_create_secret_key()

# 打包模式强制关闭 DEBUG；开发模式可由环境变量控制
DEBUG = (not IS_FROZEN) and os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get(
    'DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost'
).split(',')

CSRF_TRUSTED_ORIGINS = os.environ.get(
    'DJANGO_CSRF_TRUSTED_ORIGINS', 'http://127.0.0.1:8765,http://localhost:8765'
).split(',')


# ---------------------------------------------------------------------------
# 应用配置
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'writer_factory.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [RESOURCE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.app_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'writer_factory.wsgi.application'


# ---------------------------------------------------------------------------
# 数据库（打包模式放在用户数据目录）
# ---------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(DATA_DIR / 'db.sqlite3'),
    }
}


# ---------------------------------------------------------------------------
# 密码校验
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ---------------------------------------------------------------------------
# 国际化
# ---------------------------------------------------------------------------
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ---------------------------------------------------------------------------
# 静态文件与媒体文件
# ---------------------------------------------------------------------------
STATIC_URL = '/static/'

# collectstatic 的输出目录；打包时该目录会被打进 exe
STATIC_ROOT = RESOURCE_DIR / 'staticfiles'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# 媒体文件（封面图等）放用户可写目录
MEDIA_URL = '/media/'
MEDIA_ROOT = DATA_DIR / 'media'

# 登录重定向
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'work_list'
