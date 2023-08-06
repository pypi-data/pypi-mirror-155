import json
import os

__all__ = ["load_test_from_file"]


def load_test_from_file(filename: str) -> dict:
    """
    加载配置
    :param filename:
    :return:
    """
    p = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", filename))

    with open(p) as fp:
        return json.load(fp)
