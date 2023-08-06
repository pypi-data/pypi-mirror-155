from typing import Optional

from pydantic import BaseModel, Field

from ..values import USER_CENTER_DOMAIN

__all__ = ["UserInfoArgs"]


class UserInfoArgs(BaseModel):
    """
    用户信息表单
    """

    server_uri: str = Field(
        f"{USER_CENTER_DOMAIN}/api/user/info",
        title="服务器地址",
        description="请求要访问的地址",
    )
    access_token: str = Field(..., title="访问令牌", description="使用此访问令牌可以访问指定用户的信息")

    code_verifier: Optional[str] = Field(None, title="验证令牌", description="验证用户请求的令牌")
