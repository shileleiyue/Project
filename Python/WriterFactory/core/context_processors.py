"""模板上下文处理器：向所有模板注入应用配置。"""
from django.conf import settings


def app_settings(request):
    """注入 APP_CONFIG 与数据目录信息，供模板渲染主题变量与设置页展示。"""
    cfg = getattr(settings, 'APP_CONFIG', {})
    data_dir = getattr(settings, 'DATA_DIR', None)
    return {
        'app_config': cfg,
        'data_dir': str(data_dir) if data_dir else '',
        'is_frozen': getattr(settings, 'IS_FROZEN', False),
    }
