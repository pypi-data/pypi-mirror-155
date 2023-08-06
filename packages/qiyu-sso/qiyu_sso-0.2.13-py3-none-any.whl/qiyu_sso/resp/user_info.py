from typing import Optional

from pydantic import BaseModel, Field

__all__ = ["UserInfoResponse"]


class UserInfoResponse(BaseModel):
    username: str = Field(..., title="用户名称", description="用户的登录名称,具有唯一性")

    email: Optional[str] = Field(
        None, title="电子邮箱", description="用户的电子邮箱地址,可能为空[如果不存在 或者 应用 配置不允许返回]"
    )
    email_verified: bool = Field(False, title="电子邮箱已认证", description="用户的电子邮箱是否经过认证")

    mobile: Optional[str] = Field(
        None, title="手机号码", description="用户的真实手机号码,可能为空 [因为不存在，或者 应用 配置不允许返回]"
    )
    mobile_verified: bool = Field(False, title="手机号码已认证", description="用户的手机号码是否经过认证")

    nick_name: Optional[str] = Field(
        None, title="昵称", description="用户的昵称,可能为空[因为 没有填写 或者 应用 配置不允许返回]"
    )
    real_name: Optional[str] = Field(
        None, title="姓名", description="用户的名字,可能为空[因为 没有填写 或者 应用 配置不允许返回]"
    )
    is_staff: Optional[bool] = Field(
        None, title="员工", description="用户是否为员工用户, 可能为空[因为 应用 配置不允许返回]"
    )
    is_admin: Optional[bool] = Field(
        None, title="管理员", description="用户是否为管理员, 可能为空[因为 应用 配置不允许返回]"
    )
