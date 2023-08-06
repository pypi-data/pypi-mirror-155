from .sync_api import QiYuSSOSync
from .test_helper import load_test_from_file
from ..forms import TokenArgs, UserInfoArgs

__all__ = []


def test_get_token_args():
    sso = QiYuSSOSync()
    data = load_test_from_file("demo.json")
    ret = sso.get_access_token(TokenArgs(**data))
    assert ret is not None


def test_user_info():
    sso = QiYuSSOSync()
    data = load_test_from_file("user_info.json")
    ret = sso.get_user_info(UserInfoArgs(**data))
    assert ret is not None
