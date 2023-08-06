from typing import Optional

import redis
import fakeredis
from datetime import timedelta
from django.conf import settings


class RatelimitRedisClient:

    RATELIMIT_TTL = timedelta(minutes=2)

    def __init__(self) -> None:
        self._connect()

    def make_request(self, key: str, request_timestamp: float) -> None:
        """
        Insert request timestamp, expire key after RATELIMIT_TTL to prevent filling queue
        """
        self._client.zadd(key, {str(request_timestamp): request_timestamp})
        self._client.expire(key, RatelimitRedisClient.RATELIMIT_TTL)

    def remove_requests(self, key: str, min_time: float) -> None:
        self._client.zremrangebyscore(key, "-inf", min_time)

    def get_last_request(self, key: str) -> Optional[float]:
        val = self._client.zrange(key, -1, -1)
        return float(val[0].decode("utf-8")) if val else None

    def length(self, key: str) -> int:
        return int(self._client.zcard(key))

    def has_key(self, key: str) -> bool:
        return bool(self._client.exists(key) > 0)

    def _connect(self) -> None:
        """
        Connect to the Redis host with properly configured host, port, and database
        """
        if settings.ENVIRONMENT == "local":
            self._client = fakeredis.FakeRedis(db=0)
        else:
            host_with_port = settings.DJ_RATELIMIT_REDIS_ADDRESS
            hostname = host_with_port.split(":")[0]
            self._client = redis.Redis(host=hostname, port=settings.DJ_RATELIMIT_REDIS_PORT, db=0)


class RatelimitRedisClientFactory:
    @staticmethod
    def get_client() -> RatelimitRedisClient:
        return RatelimitRedisClient()
