"""Phase 0b · Lab 6.2 — fix KV race with compare-and-swap.

Run::

    poetry run python foundations/phase_0b/lab_6_2_kv_cas.py
"""

import threading

kv = {"counter": 0}
kv_lock = threading.Lock()
N = 100_000


def cas(key, expected, desired):
    with kv_lock:
        if kv.get(key) == expected:
            kv[key] = desired
            return True, desired
        return False, kv.get(key)


def bump() -> None:
    for _ in range(N):
        while True:
            current = kv["counter"]
            ok, _ = cas("counter", current, current + 1)
            if ok:
                break


ts = [threading.Thread(target=bump) for _ in range(4)]

for t in ts:
    t.start()

for t in ts:
    t.join()

print("counter =", kv["counter"], "expected", 4 * N)
