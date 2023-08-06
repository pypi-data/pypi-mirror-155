import datetime
from functools import wraps
from typing import Any, Optional

from rest_framework.request import Request
from rest_framework.response import Response

from dj_ratelimit.src.redis_client import (
    RatelimitRedisClientFactory,
    RatelimitRedisClient,
)


class RateLimitExceeded(Response):
    status_code = 429

    def __init__(self, data=None, status=None, template_name=None, headers=None, exception=False, content_type=None):
        super().__init__(data, status, template_name, headers, exception, content_type)


class InvalidRateLimit(Exception):
    pass


def ratelimit(rate: Any = None, burst_limit: Any = None, bucket: Any = None) -> Any:
    bucket = bucket or Bucket(rate, burst_limit)

    def decorator(fn: Any) -> Any:
        @wraps(fn)
        def _wrapped(cls: Any, request: Request, *args: Any, **kw: Any) -> Any:
            ratelimited = bucket.insert(request)
            if ratelimited:
                return RateLimitExceeded()
            return fn(cls, request, *args, **kw)

        return _wrapped

    return decorator


class Bucket:
    DEFAULT_CAPACITY = 20
    DEFAULT_LEAK_RATE = "10/m"
    DEFAULT_INTERVAL_IN_SECONDS = 60  # Default rate interval of requests per minute

    interval_map = {
        "s": 1,
        "m": 60,
        "h": 60 * 60,
        "d": 60 * 60 * 24,
    }

    def __init__(self, rate: str = DEFAULT_LEAK_RATE, burst_limit: int = DEFAULT_CAPACITY, key_fn=lambda req: "") -> None:
        self.leak_rate, self.interval_s = Bucket._parse_rate_interval(rate) if rate else (Bucket.DEFAULT_LEAK_RATE, Bucket.DEFAULT_INTERVAL_IN_SECONDS)
        self.capacity = burst_limit or Bucket.DEFAULT_CAPACITY  # max capacity (burst limit)
        self.client: RatelimitRedisClient = RatelimitRedisClientFactory.get_client()
        self.key_fn = key_fn

    def _leak(self, key: str) -> bool:
        now = datetime.datetime.now().timestamp()

        if not self.client.has_key(key):
            self.client.make_request(key, now)
            return False

        min_timestamp = now - self.interval_s

        # Leak requests older than rate interval
        self.client.remove_requests(key, min_timestamp)

        last_timestamp = self.client.get_last_request(key)
        if not last_timestamp:
            self.client.make_request(key, now + (1 / self.leak_rate))
            return False

        next_time = last_timestamp + (1 / self.leak_rate)

        if self.client.length(key) >= self.capacity:
            return True

        self.client.make_request(key, next_time)
        return False

    def insert(self, request: Request) -> bool:
        key = self.key_fn(request)
        return self._leak(key)

    @staticmethod
    def _parse_rate_interval(rate: str) -> Optional[tuple[int, int]]:
        if not rate:
            return None
        try:
            rate_str, interval_str = rate.split("/")

            return int(rate_str), Bucket.interval_map[interval_str]

        except (ValueError, KeyError):
            raise InvalidRateLimit("Specify rate limit as rate/interval [e.g. 5/m] Valid delimiters: [s, m, h, d]")
