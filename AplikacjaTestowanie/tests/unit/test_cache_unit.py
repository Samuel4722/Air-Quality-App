from app.services.cache import set_cache, get_from_cache, CACHE
import time


def test_cache_store_and_retrieve():
    CACHE.clear()
    set_cache("test:key", {"value": 123})

    result = get_from_cache("test:key")
    assert result == {"value": 123}


def test_cache_expiration():
    CACHE.clear()
    set_cache("expire:key", {"value": 999}, ttl=1)

    time.sleep(2)

    result = get_from_cache("expire:key")
    assert result is None
