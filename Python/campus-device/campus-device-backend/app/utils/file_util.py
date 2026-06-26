import os
import uuid
from datetime import datetime

import aiofiles
from fastapi import UploadFile, HTTPException

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def validate_image(file: UploadFile) -> bool:
    """校验图片格式和大小"""
    # 检查文件扩展名
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式，仅允许: {', '.join(ALLOWED_EXTENSIONS)}",
        )
    return True


async def save_upload_file(file: UploadFile, sub_dir: str) -> str:
    """保存上传文件，返回文件路径"""
    validate_image(file)

    # 检查文件大小
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="文件大小超过限制 (最大 5MB)")

    # 生成唯一文件名（UUID + 时间戳）
    ext = os.path.splitext(file.filename or "")[1].lower()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_name = f"{uuid.uuid4().hex}_{timestamp}{ext}"

    # 确保目标目录存在
    upload_dir = os.path.join("uploads", sub_dir)
    os.makedirs(upload_dir, exist_ok=True)

    # 使用 aiofiles 异步写入文件
    file_path = os.path.join(upload_dir, unique_name)
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(content)

    return file_path