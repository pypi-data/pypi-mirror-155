import uuid


def _get_coro_key(coro, prefix, unique=False):
    key = f'{prefix}::{coro.__name__}'

    return key if not unique else key + '::' + uuid.uuid4().hex


def get_rate_key(coro, unique=True):
    return _get_coro_key(coro, prefix='ratelimit', unique=unique)


def get_lock_key(coro):
    return _get_coro_key(coro, prefix='ratelock')
