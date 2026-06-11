"""Phase 0a · Lab C — race condition with asyncio + Redis.

Run::

    poetry run python foundations/phase_0a/lab_c_asyncio_race.py
"""

from __future__ import annotations

import asyncio
from typing import Final

import redis.asyncio as aioredis

NUM_TASKS: Final = 8
INCREMENTS: Final = 10_000
KEY: Final = "labC:counter"


async def bump(client: aioredis.Redis) -> None:
    """Increment a Redis counter from one coroutine using unsafe GET/SET."""
    for _ in range(INCREMENTS):
        current = int(await client.get(KEY) or 0)
        await client.set(KEY, current + 1)


async def main() -> None:
    """Run the asyncio Redis race-condition demo."""
    client = aioredis.from_url("redis://127.0.0.1:6379", decode_responses=True)
    await client.set(KEY, 0)

    await asyncio.gather(*(bump(client) for _ in range(NUM_TASKS)))

    final = int(await client.get(KEY) or 0)
    expected = NUM_TASKS * INCREMENTS
    lost = expected - final

    print(f"final = {final:>7}    expected = {expected:>7}    lost = {lost:>7}")

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
