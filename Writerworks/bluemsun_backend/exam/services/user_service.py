# exam/services/user_service.py
"""
业务逻辑层 - 用户服务
"""
from exam.models import User

class UserService:
    """用户相关业务逻辑"""

    @staticmethod
    def authenticate(username, password):
        """验证用户身份"""
        try:
            user = User.objects.get(username=username)
            if user.password == password:
                return user
            return None
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_user_by_id(user_id):
        """根据ID获取用户"""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None