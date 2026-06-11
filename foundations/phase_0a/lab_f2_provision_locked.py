"""Phase 0a · Lab F.2 — same workload, made correct by per-host locks.

Run::

    poetry run python foundations/phase_0a/lab_f2_provision_locked.py
"""

from __future__ import annotations

import json
import random
import threading
from collections import Counter
from typing import Final

import redis
from redis.exceptions import LockError
from redis.lock import Lock

NUM_HOSTS: Final = 50
NUM_JOBS: Final = 200
HOST_KEY: Final = "labF:host:{i}"
LOCK_KEY: Final = "labF:hostlock:{i}"


def seed(client: redis.Redis) -> None:
    """Seed Redis with a fresh pool of free hosts and clear host locks."""
    for index in range(NUM_HOSTS):
        client.delete(LOCK_KEY.format(i=index))
        client.set(
            HOST_KEY.format(i=index),
            json.dumps(
                {
                    "host_id": f"node-{index}",
                    "status": "free",
                    "reserved_by": None,
                }
            ),
        )


def reserve(client: redis.Redis, job_id: str, results: list[tuple[str, str]]) -> None:
    """Reserve one free host using a per-host Redis lock."""
    for _ in range(20):
        index = random.randrange(NUM_HOSTS)
        lock = Lock(
            client,
            LOCK_KEY.format(i=index),
            timeout=10,
            blocking=True,
            blocking_timeout=2,
        )

        if not lock.acquire():
            continue

        try:
            raw = client.get(HOST_KEY.format(i=index))

            if raw is None:
                continue

            host = json.loads(raw)

            if host["status"] != "free":
                continue

            host["status"] = "reserved"
            host["reserved_by"] = job_id

            client.set(HOST_KEY.format(i=index), json.dumps(host))
            results.append((job_id, host["host_id"]))
            return
        finally:
            try:
                lock.release()
            except LockError:
                pass


def main() -> None:
    """Run the locked CI host reservation demo."""
    client = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
    seed(client)

    results: list[tuple[str, str]] = []
    threads = [
        threading.Thread(target=reserve, args=(client, f"job-{index:03d}", results))
        for index in range(NUM_JOBS)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    by_host = Counter(host for _, host in results)
    double_booked = {host: count for host, count in by_host.items() if count > 1}

    print(f"jobs that claimed a host: {len(results)}")
    print(f"distinct hosts claimed:   {len(by_host)}")
    print(f"DOUBLE-BOOKED hosts:      {len(double_booked)}")

    assert not double_booked, "lock did not protect us!"


if __name__ == "__main__":
    main()
