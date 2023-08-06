import traceback
from pathlib import Path

import ring

import diskcache

cache_dir = Path("~/.diskcache/ktool").expanduser().absolute()
cache_dir.mkdir(parents=True, exist_ok=True)

storage = diskcache.Cache(cache_dir)


def cache(*args, **kwargs):
    return ring.disk(storage, *args, **kwargs)
