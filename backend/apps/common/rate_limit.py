from django.core.cache import cache
from rest_framework.exceptions import Throttled


def check_rate_limit(key: str, limit: int = 20, window_seconds: int = 60) -> None:
    current = cache.get(key, 0)
    if current >= limit:
        raise Throttled(detail="Rate limit exceeded. Try again later.")
    cache.set(key, current + 1, timeout=window_seconds)
