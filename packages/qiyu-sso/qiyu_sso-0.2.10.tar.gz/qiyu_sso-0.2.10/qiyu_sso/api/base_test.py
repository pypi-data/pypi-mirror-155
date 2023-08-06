import secrets
from urllib.parse import urlparse, parse_qs

from .base import BaseAPI
from ..forms.login import LoginArgs

__all__ = []


def test_get_login_url():
    """
    测试获取登录地址
    :return:
    """
    client_id = secrets.token_hex(20)
    redirect_uri = "https://www.facebook.com/demo"
    state = secrets.token_hex(24)
    scope = "read"

    args = LoginArgs(
        client_id=client_id,
        redirect_uri=redirect_uri,
        state=state,
        scope=scope,
        code_challenge="",
    )

    base = BaseAPI()
    url = base.get_login_url(args)
    print(url)
    d = urlparse(url)

    assert d.scheme == "https"
    assert d.netloc == "user.qiyutech.tech"
    assert d.path == "/oauth/authorize/"
    q = parse_qs(d.query)

    assert q["response_type"] == ["code"]
    assert q["client_id"] == [client_id]
    assert q["redirect_uri"] == [redirect_uri]
    assert q["scope"] == [scope]
    assert q["state"] == [state]
