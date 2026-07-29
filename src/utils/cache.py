import asyncio
import time

from typing import Any, Optional


class AsyncTTLCache:
    """
    A simple asynchronous in-memory cache with TTL support.

    Intended for:

    - Embedding cache
    - Search cache
    - Router cache
    - LLM response cache

    Can later be replaced with Redis while
    preserving the same interface.
    """

    def __init__(
        self,
        ttl_seconds: int = 3600,
    ):

        self.ttl_seconds = ttl_seconds

        self._cache: dict[str, tuple[Any, float]] = {}

        self._lock = asyncio.Lock()

    async def get(
        self,
        key: str,
    ) -> Optional[Any]:

        async with self._lock:

            value = self._cache.get(key)

            if value is None:
                return None

            cached_value, expiry = value

            if expiry < time.time():

                del self._cache[key]

                return None

            return cached_value

    async def set(
        self,
        key: str,
        value: Any,
    ) -> None:

        async with self._lock:

            self._cache[key] = (
                value,
                time.time() + self.ttl_seconds,
            )

    async def delete(
        self,
        key: str,
    ) -> None:

        async with self._lock:

            self._cache.pop(key, None)

    async def clear(
        self,
    ) -> None:

        async with self._lock:

            self._cache.clear()

    async def contains(
        self,
        key: str,
    ) -> bool:

        return await self.get(key) is not None


# Shared cache instances

embedding_cache = AsyncTTLCache(
    ttl_seconds=24 * 60 * 60,
)

search_cache = AsyncTTLCache(
    ttl_seconds=30 * 60,
)

router_cache = AsyncTTLCache(
    ttl_seconds=60 * 60,
)

generation_cache = AsyncTTLCache(
    ttl_seconds=60 * 60,
)
