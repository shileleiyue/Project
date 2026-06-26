from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repo import UserRepository
from app.models.user import User, UserRole
from app.schemas.user import UserRegisterRequest, UserLoginRequest
from app.utils.password_util import hash_password, verify_password
from app.utils.jwt_util import create_access_token


class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def register(self, req: UserRegisterRequest):
        # 检查手机号是否已注册
        existing_phone = await self.user_repo.get_by_phone(req.phone)
        if existing_phone:
            raise HTTPException(status_code=409, detail="手机号已注册")

        # 检查用户名是否已存在
        existing_username = await self.user_repo.get_by_username(req.username)
        if existing_username:
            raise HTTPException(status_code=409, detail="用户名已存在")

        # 校验角色
        if req.role not in [r.value for r in UserRole]:
            req.role = UserRole.student.value

        user = User(
            username=req.username,
            phone=req.phone,
            password_hash=hash_password(req.password),
            role=UserRole(req.role),
        )
        return await self.user_repo.create(user)

    async def login(self, req: UserLoginRequest):
        user = await self.user_repo.get_by_phone(req.phone)
        if not user:
            raise HTTPException(status_code=401, detail="手机号或密码错误")

        if not user.is_active:
            raise HTTPException(status_code=403, detail="账号已被禁用")

        if not verify_password(req.password, user.password_hash):
            raise HTTPException(status_code=401, detail="手机号或密码错误")

        token = create_access_token(
            data={"user_id": user.id, "role": user.role.value}
        )
        return {
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "phone": user.phone,
                "email": user.email,
                "role": user.role.value,
                "avatar": user.avatar,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat() if user.created_at else None,
            },
        }

    async def get_current_user_info(self, user: User):
        return {
            "id": user.id,
            "username": user.username,
            "phone": user.phone,
            "email": user.email,
            "role": user.role.value,
            "avatar": user.avatar,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        }