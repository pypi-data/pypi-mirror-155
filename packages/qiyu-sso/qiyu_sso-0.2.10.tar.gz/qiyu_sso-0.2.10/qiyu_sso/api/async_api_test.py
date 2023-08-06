import pytest

from .async_api import QiYuSSOAsync
from .test_helper import load_test_from_file
from ..forms import TokenArgs, UserInfoArgs

__all__ = []


@pytest.mark.asyncio
async def test_get_token_args():
    sso = QiYuSSOAsync()
    data = load_test_from_file("demo.json")
    ret = await sso.get_access_token(TokenArgs(**data))
    assert ret is None


@pytest.mark.asyncio
async def test_get_user_info():
    sso = QiYuSSOAsync()
    data = load_test_from_file("user_info.json")
    ret = await sso.get_user_info(UserInfoArgs(**data))
    print(ret)
    assert ret is not None
