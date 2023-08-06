from urllib.parse import urlencode

from ..forms import LoginArgs, TokenArgs

__all__ = ["BaseAPI"]


class BaseAPI(object):
    """
    基础 API 定义
    """

    @staticmethod
    def get_token_url(args: TokenArgs) -> (str, dict):
        """
        返回 获取 token 的请求网址

        :param args:
        :return: (request url, request body)
                 request method must be POST
                 form use standard form
        """
        query = args.dict()
        uri = query.pop("server_uri")
        return uri, query

    @staticmethod
    def get_login_url(args: LoginArgs) -> str:
        """
        获取登录的地址

        注意:

            这个接口使用的是 Authorization Code(授权码) 授权模式

        因为授权码模式是最安全并且最常用的,因为仅支持这个模式

        :param args:
        :return:
        """
        query: dict = args.dict()
        uri = query.pop("server_uri")
        return uri + "?" + urlencode(query)
