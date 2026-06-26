from .models import SchoolInfo, FriendLink

def school_info(request):
    """将学校信息注入所有模板上下文"""
    try:
        info = SchoolInfo.objects.first()
    except Exception:
        info = None
    return {'school_info': info}


def friend_links(request):
    """将启用的友情链接注入所有模板上下文"""
    try:
        links = list(FriendLink.objects.filter(is_enabled=True))
    except Exception:
        links = []
    return {'friend_links': links}