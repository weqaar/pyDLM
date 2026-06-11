"""Phase 0a · Lab F.1 — racing CI jobs corrupt host reservations.

Run::

    poetry run python foundations/phase_0a/lab_f1_provision_race.py
"""

from __future__ import annotations

import json
import random
import threading
from collections import Counter
from typing import Final

import redis

NUM_HOSTS: Final = 50
NUM_JOBS: Final = 200
HOST_KEY: Final = "labF:host:{i}"


def seed(client: redis.Redis) -> None:
    """Seed Redis with a fresh pool of free hosts."""
    for index in range(NUM_HOSTS):
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
    """Try to reserve one free host using unsafe GET/SET."""
    for _ in range(20):
        index = random.randrange(NUM_HOSTS)
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


def main() -> None:
    """Run the broken CI host reservation demo."""
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

    for host, count in sorted(double_booked.items()):
        owners = [job_id for job_id, claimed_host in results if claimed_host == host]
        print(f"  {host}: {count} owners → {owners}")


if __name__ == "__main__":
    main()
