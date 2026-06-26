"""权限类"""
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """仅限管理员"""
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, 'is_admin', False)
        )


class IsTeacher(BasePermission):
    """仅限教师"""
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, 'is_teacher', False)
        )


class IsStudent(BasePermission):
    """仅限学生"""
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, 'is_student', False)
        )


class IsOwnerOrAdmin(BasePermission):
    """对象级别：本人或管理员"""
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if getattr(user, 'is_admin', False):
            return True
        # 看对象上有没有 user / student / creator / uploader 等关联用户
        for attr in ('user', 'student', 'creator', 'uploader', 'owner'):
            if hasattr(obj, attr):
                owner = getattr(obj, attr)
                if owner == user:
                    return True
                break
        return False


class IsTeacherOrAdmin(BasePermission):
    """教师或管理员"""
    def has_permission(self, request, view):
        u = request.user
        return bool(u and u.is_authenticated and (u.is_teacher or u.is_admin))
