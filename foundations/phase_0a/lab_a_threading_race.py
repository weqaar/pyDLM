"""Phase 0a · Lab A — race condition with threading + Redis.

Run::

    poetry run python foundations/phase_0a/lab_a_threading_race.py
"""

from __future__ import annotations

import threading
from typing import Final

import redis

NUM_THREADS: Final = 8
INCREMENTS: Final = 10_000
KEY: Final = "labA:counter"


def bump(client: redis.Redis) -> None:
    """Increment a Redis counter using unsafe GET/SET read-modify-write."""
    for _ in range(INCREMENTS):
        current = int(client.get(KEY) or 0)
        client.set(KEY, current + 1)


def main() -> None:
    """Run the threaded Redis race-condition demo."""
    client = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
    client.set(KEY, 0)

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
