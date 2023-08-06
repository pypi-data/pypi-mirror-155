import time
from typing import cast, Dict

import jwt

from .config import TOKENS_URL
from .interfaces import RefreshToken
from .make_request import make_request


access_token_cache: Dict[str, str] = {}


def reset_access_token_cache() -> None:
    global access_token_cache
    access_token_cache = {}


def get_access_token(
    refresh_token: RefreshToken,
    platform: str,
    scope: str,
) -> str:
    cache_key = f'{platform}:{scope}'

    access_token = access_token_cache.get(cache_key)

    if not access_token or has_expired(access_token):
        access_token = create_access_token(refresh_token, platform, scope)
        access_token_cache[cache_key] = access_token

    return access_token


def create_access_token(
    refresh_token: RefreshToken,
    platform: str,
    scope: str,
) -> str:
    result, _ = make_request(
        url=TOKENS_URL,
        method='POST',
        token=refresh_token['token'],
        body={
            'subject': refresh_token['subject'],
            'platform': platform,
            'scope': scope,
        },
    )

    return cast(str, result.get('token'))


def has_expired(token: str) -> bool:
    decoded_token = jwt.decode(
        token,
        algorithms=['HS256'],
        options={'verify_signature': False},
    )

    expiration = int(decoded_token.get('exp', 0))
    now = int(time.time() * 1000)

    if expiration and now - expiration >= 0:
        return True

    return False
