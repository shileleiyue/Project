from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import get_db
from app.dependencies import get_current_user
from app.schemas.user import UserRegisterRequest, UserLoginRequest
from app.services.auth_service import AuthService
from app.utils.response_util import Result

router = APIRouter()


@router.post("/register")
async def register(req: UserRegisterRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    user = await service.register(req)
    return Result.success(data={"id": user.id, "username": user.username}, msg="注册成功")


@router.post("/login")
async def login(req: UserLoginRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    data = await service.login(req)
    return Result.success(data=data, msg="登录成功")


@router.post("/logout")
async def logout(current_user=Depends(get_current_user)):
    return Result.success(msg="退出成功")


@router.get("/me")
async def get_me(
    current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    from app.repositories.user_repo import UserRepository
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    service = AuthService(db)
    user_info = await service.get_current_user_info(user)
    return Result.success(data=user_info)