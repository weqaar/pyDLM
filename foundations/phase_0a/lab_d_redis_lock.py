"""Phase 0a · Lab D — fix the race with a Redis distributed lock.

Run::

    poetry run python foundations/phase_0a/lab_d_redis_lock.py
"""

from __future__ import annotations

import threading
from typing import Final

import redis
from redis.lock import Lock

NUM_THREADS: Final = 8
INCREMENTS: Final = 10_000
KEY: Final = "labD:counter"
LOCK_KEY: Final = "labD:lock"


def bump(client: redis.Redis) -> None:
    """Increment a Redis counter while holding a Redis distributed lock."""
    for _ in range(INCREMENTS):
        lock = Lock(client, LOCK_KEY, timeout=5, blocking=True, blocking_timeout=10)

        if not lock.acquire():
            raise RuntimeError("could not acquire lock")

        try:
            current = int(client.get(KEY) or 0)
            client.set(KEY, current + 1)
        finally:
            lock.release()


def main() -> None:
    """Run the Redis lock demo and show that no increments are lost."""
    client = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
    client.set(KEY, 0)
    client.delete(LOCK_KEY)

    threads = [
        threading.Thread(target=bump, args=(client,)) for _ in range(NUM_THREADS)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    final = int(client.get(KEY) or 0)
    expected = NUM_THREADS * INCREMENTS
    lost = expected - final

    print(f"final = {final:>7}    expected = {expected:>7}    lost = {lost:>7}")


if __name__ == "__main__":
    main()
