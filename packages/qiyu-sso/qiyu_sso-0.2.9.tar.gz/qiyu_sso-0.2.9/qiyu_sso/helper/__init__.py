import secrets
import random
import base64
import hashlib

__all__ = ["gen_code_verifier", "compute_code_challenge"]


def gen_code_verifier() -> str:
    """
    生成 Code Verifier https://datatracker.ietf.org/doc/html/rfc7636#section-4.1
    :return:
    """
    code_verifier = secrets.token_bytes(random.randint(43, 128))
    return base64.urlsafe_b64encode(code_verifier).decode()


def compute_code_challenge(code_verifier: str) -> str:
    """
    计算 S256 挑战码
    :param code_verifier:
    :return:
    """
    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(code_challenge).decode("utf-8").replace("=", "")
