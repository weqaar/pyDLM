"""Phase 0b · Lab 6.1 — race condition on a KV store.

Run::

    poetry run python foundations/phase_0b/lab_6_1_kv_race.py
"""

import threading

kv = {"counter": 0}
N = 100_000


def bump() -> None:
    for _ in range(N):
        v = kv["counter"]
        kv["counter"] = v + 1


threads = [threading.Thread(target=bump) for _ in range(4)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
print("counter =", kv["counter"], "expected", 4 * N)
