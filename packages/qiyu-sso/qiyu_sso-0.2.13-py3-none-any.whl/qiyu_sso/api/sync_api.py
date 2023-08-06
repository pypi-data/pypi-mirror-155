import logging
from typing import Optional

import requests

from .base import BaseAPI
from ..forms import TokenArgs, UserInfoArgs
from ..resp import TokenResponse, UserInfoResponse

__all__ = ["QiYuSSOSync"]


class QiYuSSOSync(BaseAPI):
    @staticmethod
    def get_user_info(args: UserInfoArgs) -> Optional[UserInfoResponse]:
        """
        使用 访问令牌 获取用户信息
        """
        r = requests.post(url=args.server_uri, json=args.dict(exclude={"server_uri"}))
        if not r.ok:
            logging.error(f"get user info failed: {r}")
            return None
        ret = r.json()
        return UserInfoResponse(**ret)

    def get_access_token(self, args: TokenArgs) -> Optional[TokenResponse]:
        """
        获取访问令牌
        """

        url, data = self.get_token_url(args)
        r = requests.post(url=url, data=data)
        if not r.ok:
            logging.error(f"get token failed: {r.status_code} {r.headers} {r.text}")
            return None
        ret = r.json()
        return TokenResponse(**ret)
