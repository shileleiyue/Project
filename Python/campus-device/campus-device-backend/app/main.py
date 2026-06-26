from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.middleware.cors_middleware import setup_cors
from app.routers import auth, device, borrow, repair, audit, user

app = FastAPI(title="校园设备借用与维修管理系统", version="1.0.0")

setup_cors(app)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(device.router, prefix="/api/devices", tags=["设备"])
app.include_router(borrow.router, prefix="/api/borrows", tags=["借用"])
app.include_router(repair.router, prefix="/api/repairs", tags=["维修"])
app.include_router(audit.router, prefix="/api", tags=["审核记录"])
app.include_router(user.router, prefix="/api/users", tags=["用户"])

# 静态文件（上传文件访问）
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
async def root():
    return {"message": "校园设备借用与维修管理系统 API"}