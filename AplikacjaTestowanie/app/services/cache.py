import time

CACHE = {}
CACHE_TTL = 300  # 5 minut


def get_from_cache(key: str):
    if key in CACHE:
        value, timestamp, ttl = CACHE[key]
        if time.time() - timestamp < ttl:
            return value
        else:
            del CACHE[key]
    return None


def set_cache(key: str, value, ttl=CACHE_TTL):
    CACHE[key] = (value, time.time(), ttl)
