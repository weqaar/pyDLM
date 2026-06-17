"""Phase 0b · Lab 2.2 — fixing a race condition with a lock.

Run::

    poetry run python foundations/phase_0b/lab_2_2_race_fixed.py
"""

import threading

counter = 0
N = 1_000_000
lock = threading.Lock()


def bump() -> None:
    global counter

    for _ in range(N):
        with lock:
            counter = counter + 1


t1 = threading.Thread(target=bump)
t2 = threading.Thread(target=bump)
t3 = threading.Thread(target=bump)
t4 = threading.Thread(target=bump)

t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()

print(f"final counter = {counter} (expected {4 * N})")
