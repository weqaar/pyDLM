"""Phase 0a · Lab E — fencing token defends against expired-lease writes.

Run::

    poetry run python foundations/phase_0a/lab_e_fencing.py
"""

from __future__ import annotations

import threading
import time
from typing import Final

import redis
from redis.exceptions import LockError
from redis.lock import Lock

NUM_THREADS: Final = 4
ROUNDS: Final = 1_000
KEY: Final = "labE:counter"
LOCK_KEY: Final = "labE:lock"
EPOCH_KEY: Final = "labE:epoch"
HOLDER_KEY: Final = "labE:current_epoch_in_state"


def critical_section(client: redis.Redis, my_epoch: int) -> bool:
    """Return True if our write was accepted, False if we were fenced out."""
    current = int(client.get(HOLDER_KEY) or 0)

    if my_epoch < current:
        return False

    pipe = client.pipeline()
    pipe.set(HOLDER_KEY, my_epoch)
    pipe.incr(KEY)
    pipe.execute()

    return True


def worker(client: redis.Redis) -> None:
    """Acquire a Redis lock, mint a fencing token, and attempt a safe write."""
    for _ in range(ROUNDS):
        lock = Lock(client, LOCK_KEY, timeout=2, blocking=True, blocking_timeout=5)

        if not lock.acquire():
            continue

        try:
            my_epoch = int(client.incr(EPOCH_KEY))
            time.sleep(0.0001)
            critical_section(client, my_epoch)
        finally:
            try:
                lock.release()
            except LockError:
                pass


def main() -> None:
    """Run the fencing-token demo."""
    client = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

    for key in (KEY, LOCK_KEY, EPOCH_KEY, HOLDER_KEY):
        client.delete(key)

    threads = [
        threading.Thread(target=worker, args=(client,)) for _ in range(NUM_THREADS)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(f"final counter = {client.get(KEY)}    final epoch = {client.get(EPOCH_KEY)}")


if __name__ == "__main__":
    main()
