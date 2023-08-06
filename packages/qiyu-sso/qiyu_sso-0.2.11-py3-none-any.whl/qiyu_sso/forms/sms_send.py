from pydantic import Field

from .client_base import ClientBaseForm

__all__ = ["SmsSendForm"]


class SmsSendForm(ClientBaseForm):
    """
    发送短信的接口
    """

    mobile: str = Field(..., title="手机号码")
