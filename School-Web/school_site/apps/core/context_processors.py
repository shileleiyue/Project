from .models import SchoolInfo

def school_info(request):
    """将学校信息注入所有模板上下文"""
    try:
        info = SchoolInfo.objects.first()
    except Exception:
        info = None
    return {'school_info': info}