"""Redis TTL caches for hot-path data.

Caches:
- user:{id}   -> CachedUser attrs (every auth'd request)
- super:{id}  -> bool (every protected request)
- dict:{key}  -> JSON (dictionary data, rarely changes)
"""
import json
from dataclasses import asdict, dataclass
from typing import Any

from redis.asyncio import Redis

_USER_TTL = 300  # 5 min
_SUPERUSER_TTL = 300  # 5 min
_DICT_TTL = 600  # 10 min

_redis: Redis | None = None


async def init_redis(url: str) -> None:
    global _redis
    _redis = Redis.from_url(url, decode_responses=True)


async def close_redis() -> None:
    global _redis
    if _redis is not None:
        await _redis.aclose()
        _redis = None


def _get_redis() -> Redis:
    if _redis is None:
        raise RuntimeError("Redis not initialised")
    return _redis


# -- CachedUser dataclass --

@dataclass(frozen=True, slots=True)
class CachedUser:
    """Lightweight snapshot of User for auth checks."""
    id: int
    company_id: int
    user_lock: bool


# -- user cache (get_current_user) --

async def get_cached_user(
    user_id: int,
) -> CachedUser | None:
    raw = await _get_redis().get(f"user:{user_id}")
    if raw is None:
        return None
    data = json.loads(raw)
    return CachedUser(**data)


async def set_cached_user(
    user_id: int, user: CachedUser,
) -> None:
    await _get_redis().set(
        f"user:{user_id}",
        json.dumps(asdict(user)),
        ex=_USER_TTL,
    )


async def invalidate_user(user_id: int) -> None:
    await _get_redis().delete(f"user:{user_id}")


# -- superuser role cache --

async def get_cached_is_superuser(
    user_id: int,
) -> bool | None:
    raw = await _get_redis().get(f"super:{user_id}")
    if raw is None:
        return None
    return raw == "1"


async def set_cached_is_superuser(
    user_id: int, value: bool,
) -> None:
    await _get_redis().set(
        f"super:{user_id}",
        "1" if value else "0",
        ex=_SUPERUSER_TTL,
    )


async def invalidate_superuser(
    user_id: int,
) -> None:
    await _get_redis().delete(f"super:{user_id}")


# -- dictionary cache (roles list, etc.) --

async def get_cached_dict(key: str) -> Any | None:
    raw = await _get_redis().get(f"dict:{key}")
    if raw is None:
        return None
    return json.loads(raw)


async def set_cached_dict(
    key: str, value: Any,
) -> None:
    await _get_redis().set(
        f"dict:{key}",
        json.dumps(value, default=str),
        ex=_DICT_TTL,
    )


async def invalidate_dict(key: str) -> None:
    await _get_redis().delete(f"dict:{key}")
