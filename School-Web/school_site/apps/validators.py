import os
from django.core.exceptions import ValidationError


def validate_file_extension(allowed_extensions):
    """
    返回一个验证器，检查文件扩展名是否在允许列表中。
    用法：validators=[validate_file_extension(['pdf', 'jpg'])]
    """
    def validator(value):
        ext = os.path.splitext(value.name)[1].lower().lstrip('.')
        if ext not in allowed_extensions:
            raise ValidationError(
                f'不支持的文件类型 ".{ext}"，仅允许：{", ".join(allowed_extensions)}'
            )
    return validator


def validate_file_size(max_size_mb):
    """
    返回一个验证器，检查文件大小（MB）。
    用法：validators=[validate_file_size(10)]
    """
    def validator(value):
        limit = max_size_mb * 1024 * 1024
        if value.size > limit:
            raise ValidationError(
                f'文件大小不能超过 {max_size_mb} MB'
            )
    return validator