from typing import Any, Optional


class Result:
    @staticmethod
    def success(data: Any = None, msg: str = "success") -> dict:
        return {"code": 200, "msg": msg, "data": data}

    @staticmethod
    def error(code: int = 400, msg: str = "error", data: Any = None) -> dict:
        return {"code": code, "msg": msg, "data": data}