from typing import Optional

from pydantic import Field, BaseModel

from ..values import USER_CENTER_DOMAIN

__all__ = ["TokenArgs"]


class TokenArgs(BaseModel):
    """
    获取 Token 的参数
    """

    server_uri: str = Field(
        f"{USER_CENTER_DOMAIN}/oauth/token/",
        title="OAuth2 Token地址",
        description="使用您自己服务器的地址",
    )
    redirect_uri: str = Field(
        ..., title="跳转 URI", description="授权之后会跳转到这个 URL 并且附带 code & state 参数"
    )
    client_id: str = Field(..., title="客户ID")
    client_secret: str = Field(..., title="客户机密")
    code: str = Field(..., title="授权码")

    grant_type: str = Field(
        "authorization_code", title="授权类型", description="固定值[当前仅仅支持授权码]"
    )

    code_verifier: Optional[str] = Field(None, title="验证令牌", description="验证用户请求的令牌")
