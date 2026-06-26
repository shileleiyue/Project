from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class FileSizeValidator:
    """可序列化的文件大小验证器"""
    def __init__(self, max_size_mb):
        self.max_size_mb = max_size_mb

    def __call__(self, value):
        limit = self.max_size_mb * 1024 * 1024
        if value.size > limit:
            raise ValidationError(f'文件大小不能超过 {self.max_size_mb} MB')

    def __eq__(self, other):
        return isinstance(other, FileSizeValidator) and self.max_size_mb == other.max_size_mb