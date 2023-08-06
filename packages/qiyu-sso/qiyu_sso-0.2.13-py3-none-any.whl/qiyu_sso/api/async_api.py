import logging
from typing import Optional

from aiohttp import client

from .base import BaseAPI
from ..forms import TokenArgs, UserInfoArgs
from ..resp import TokenResponse, UserInfoResponse

__all__ = ["QiYuSSOAsync"]


class QiYuSSOAsync(BaseAPI):
    def __init__(self):
        super().__init__()
        self._http = client.ClientSession()

    async def get_user_info(self, args: UserInfoArgs) -> Optional[UserInfoResponse]:
        """
        使用 访问令牌 获取用户信息
        """
        r = await self._http.post(
            url=args.server_uri, json=args.dict(exclude={"server_uri"})
        )
        if not r.ok:
            logging.error(f"get user info failed: {r}")
            return None
        ret = await r.json()
        return UserInfoResponse(**ret)

    async def get_access_token(self, args: TokenArgs) -> Optional[TokenResponse]:
        """
        获取 访问令牌
        :param args:
        :return:
        """
        url, params = self.get_token_url(args)
        resp = await self._http.post(url, data=params)
        if not resp.ok:
            logging.error(f"get token failed: {resp}")
            return None

        ret = await resp.json()
        return TokenResponse(**ret)
