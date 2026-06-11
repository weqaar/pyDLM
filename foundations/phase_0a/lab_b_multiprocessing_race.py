"""Phase 0a · Lab B — race condition with multiprocessing + Redis.

Run::

    poetry run python foundations/phase_0a/lab_b_multiprocessing_race.py
"""

from __future__ import annotations

import multiprocessing as mp
from typing import Final

import redis

NUM_PROCS: Final = 8
INCREMENTS: Final = 10_000
KEY: Final = "labB:counter"


def bump() -> None:
    """Increment a Redis counter from one OS process using unsafe GET/SET."""
    client = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

    for _ in range(INCREMENTS):
        current = int(client.get(KEY) or 0)
        client.set(KEY, current + 1)


def main() -> None:
    """Run the multiprocessing Redis race-condition demo."""
    redis.Redis(host="127.0.0.1", port=6379, decode_responses=True).set(KEY, 0)

    processes = [mp.Process(target=bump) for _ in range(NUM_PROCS)]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    client = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
    final = int(client.get(KEY) or 0)
    expected = NUM_PROCS * INCREMENTS
    lost = expected - final

    print(f"final = {final:>7}    expected = {expected:>7}    lost = {lost:>7}")


if __name__ == "__main__":
    main()
