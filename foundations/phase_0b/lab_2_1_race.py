"""Phase 0b · Lab 2.1 — demonstrating a race condition.

Run::

    poetry run python foundations/phase_0b/lab_2_1_race.py
"""

import threading

counter = 0
N = 1_000_000


def bump() -> None:
    global counter

    for _ in range(N):
        counter = counter + 1


t1 = threading.Thread(target=bump)
t2 = threading.Thread(target=bump)

t1.start()
t2.start()

t1.join()
t2.join()

print(f"final counter = {counter} (expected {2 * N})")
