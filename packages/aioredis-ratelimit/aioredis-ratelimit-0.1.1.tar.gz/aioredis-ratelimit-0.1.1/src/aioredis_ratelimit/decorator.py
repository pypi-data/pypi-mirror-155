import asyncio
from functools import wraps

from .exceptions import RateLimitExceeded
from .redis import get_rate_key, get_lock_key


def ratelimit(calls, period, redis, raise_on_limit=False):
    """A rate limiter decorator factory used to limit asyncio coroutine calls
    during the given time period.

    Args:
        calls (int): The maximum number of calls within a time period.
        period (datetime.timedelta): A time period within which the rate limit applies.
        redis (aioredis.client.Redis): An aioredis client instance.
        raise_on_limit (bool): A flag indicating whether to raise an exception
            when the hitting the rate limit.

    Returns:
        An asyncio coroutine decorator.

    Raises:
        RateLimitExceeded in a decorated couroutine when raise_on_limit is True
            and the defined rate limit exceeded.

    Usage:
        >>> from datetime import timedelta
        >>>
        >>> import aioredis
        >>> from aioredis_ratelimit import ratelimit
        >>>
        >>> redis = aioredis.from_url('redis://127.0.0.1:6379/0')
        >>>
        >>> @ratelimit(calls=1, period=timedelta(seconds=1), redis=redis)
        >>> async def coro():
        ...     pass
    """

    def decorator(coro):
        lock_key = get_lock_key(coro)
        rate_key = get_rate_key(coro, unique=False)

        @wraps(coro)
        async def wrapper(*args, **kwargs):

            async with redis.lock(name=lock_key):
                rate_key_cur = await redis.get(rate_key)

                if rate_key_cur is None:
                    rate_key_cur = get_rate_key(coro)
                    await redis.set(rate_key, rate_key_cur)

                counter = await redis.incr(rate_key_cur)
                key_pttl = await redis.pttl(rate_key_cur)

                if counter > calls:

                    if raise_on_limit:
                        raise RateLimitExceeded

                    await asyncio.sleep(key_pttl / 1000)

                    rate_key_cur = get_rate_key(coro)
                    await redis.set(rate_key, rate_key_cur)
                    await redis.incr(rate_key_cur)
                    key_pttl = -1

                if key_pttl == -1:
                    key_pttl = int(period.total_seconds() * 1000)
                    await redis.pexpire(rate_key_cur, key_pttl)

            return await coro(*args, **kwargs)

        return wrapper

    return decorator
