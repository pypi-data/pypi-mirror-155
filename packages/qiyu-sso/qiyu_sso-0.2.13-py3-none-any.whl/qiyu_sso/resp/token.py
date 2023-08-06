from pydantic import BaseModel, Field

__all__ = ["TokenResponse"]


class TokenResponse(BaseModel):
    access_token: str = Field(..., title="访问令牌")
    expires_in: int = Field(..., title="过期时间", description="单位: 为秒")
    token_type: str = Field(..., title="令牌类型", description="当前为: Bearer")
    scope: str = Field(..., title="授权范围", description="多个值使用 空格 分隔")
    refresh_token: str = Field(..., title="刷新令牌")
