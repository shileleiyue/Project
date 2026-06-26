def user_info(request):
    """向所有模板注入用户信息"""
    if request.user.is_authenticated:
        return {
            'current_user': request.user,
            'is_whiteboard': request.user.role == 'whiteboard',
        }
    return {}


def nav_menu(request):
    """角色驱动的导航菜单上下文处理器"""

    # ---- 访客（未登录）完整公开菜单 ----
    guest_menu = [
        {'name': '首页', 'url': 'core:home', 'children': []},
        {'name': '学校概况', 'url': '#', 'children': [
            {'name': '学校简介', 'url': 'pages:about'},
            {'name': '历史沿革', 'url': 'pages:school_history'},
            {'name': '校园文化', 'url': 'pages:campus_culture'},
            {'name': '办学理念', 'url': 'pages:education_philosophy'},
            {'name': '学校愿景', 'url': 'pages:school_vision'},
        ]},
        {'name': '组织架构', 'url': 'organization:departments', 'children': []},
        {'name': '信息发布', 'url': 'news:article_list', 'children': []},
        {'name': '招生招聘', 'url': 'admissions:brochures', 'children': []},
        {'name': '毕业生', 'url': 'graduates:list', 'children': []},
        {'name': '校园风光', 'url': 'gallery:album_list', 'children': []},
        {'name': '互动交流', 'url': 'contact:message_list', 'children': []},
    ]

    # 未登录用户返回访客菜单
    if not request.user.is_authenticated:
        return {'nav_items': guest_menu}

    role = request.user.role

    # ---- 各角色菜单定义 ----
    role_menus = {
        'student': [
            {'name': '首页', 'url': 'core:home', 'children': []},
            {'name': '信息发布', 'url': 'news:article_list', 'children': []},
            {'name': '班级空间', 'url': 'core:home', 'children': []},
            {'name': '个人中心', 'url': 'accounts:profile', 'children': []},
        ],
        'parent': [
            {'name': '首页', 'url': 'core:home', 'children': []},
            {'name': '信息发布', 'url': 'news:article_list', 'children': []},
            {'name': '孩子信息', 'url': 'accounts:parent_bind', 'children': []},
            {'name': '家校互动', 'url': 'contact:principal_mail', 'children': []},
            {'name': '个人中心', 'url': 'accounts:profile', 'children': []},
        ],
        'head_teacher': [
            {'name': '首页', 'url': 'core:home', 'children': []},
            {'name': '信息发布', 'url': 'news:article_list', 'children': []},
            {'name': '班级管理', 'url': 'core:home', 'children': []},
            {'name': '学生管理', 'url': 'organization:teachers', 'children': []},
            {'name': '个人中心', 'url': 'accounts:profile', 'children': []},
        ],
        'academic_director': [
            {'name': '首页', 'url': 'core:home', 'children': []},
            {'name': '信息发布', 'url': 'news:article_list', 'children': []},
            {'name': '教学管理', 'url': 'core:home', 'children': []},
            {'name': '课程安排', 'url': 'core:home', 'children': []},
            {'name': '师资队伍', 'url': 'organization:teachers', 'children': []},
            {'name': '个人中心', 'url': 'accounts:profile', 'children': []},
        ],
        'principal': [
            {'name': '首页', 'url': 'core:home', 'children': []},
            {'name': '信息发布', 'url': 'news:article_list', 'children': []},
            {'name': '组织架构', 'url': 'organization:departments', 'children': []},
            {'name': '校园风光', 'url': 'gallery:album_list', 'children': []},
            {'name': '数据统计', 'url': 'core:home', 'children': []},
            {'name': '个人中心', 'url': 'accounts:profile', 'children': []},
        ],
        'admin': [
            {'name': '首页', 'url': 'core:home', 'children': []},
            {'name': '信息发布', 'url': 'news:article_list', 'children': []},
            {'name': '组织架构', 'url': 'organization:departments', 'children': []},
            {'name': '招生招聘', 'url': 'admissions:brochures', 'children': []},
            {'name': '校园风光', 'url': 'gallery:album_list', 'children': []},
            {'name': '后台管理', 'url': '/admin/', 'children': []},
            {'name': '个人中心', 'url': 'accounts:profile', 'children': []},
        ],
        'teacher': [
            {'name': '首页', 'url': 'core:home', 'children': []},
            {'name': '信息发布', 'url': 'news:article_list', 'children': []},
            {'name': '教学资源', 'url': 'core:home', 'children': []},
            {'name': '个人中心', 'url': 'accounts:profile', 'children': []},
        ],
        'counselor': [
            {'name': '首页', 'url': 'core:home', 'children': []},
            {'name': '信息发布', 'url': 'news:article_list', 'children': []},
            {'name': '学生辅导', 'url': 'core:home', 'children': []},
            {'name': '个人中心', 'url': 'accounts:profile', 'children': []},
        ],
        'staff': [
            {'name': '首页', 'url': 'core:home', 'children': []},
            {'name': '信息发布', 'url': 'news:article_list', 'children': []},
            {'name': '资源管理', 'url': 'core:home', 'children': []},
            {'name': '个人中心', 'url': 'accounts:profile', 'children': []},
        ],
        'whiteboard': [
            {'name': '首页', 'url': 'core:home', 'children': []},
            {'name': '信息发布', 'url': 'news:article_list', 'children': []},
            {'name': '班级空间', 'url': 'core:home', 'children': []},
            {'name': '个人中心', 'url': 'accounts:profile', 'children': []},
        ],
    }

    return {'nav_items': role_menus.get(role, guest_menu)}