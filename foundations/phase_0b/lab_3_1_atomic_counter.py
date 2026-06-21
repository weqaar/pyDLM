"""Phase 0b . Lab 2.1 - demonstrating of atomic operations at the silicon level.

Run::
    poetry run python foundations/phase_0b/lab_3_1_atomic_counter.py
"""

import threading
from itertools import count

counter = count()  # thread-safe-by-implementation
N = 1_000_000


def bump():
    for _ in range(N):
        next(counter)


ts = [threading.Thread(target=bump) for _ in range(4)]
for t in ts:
    t.start()
for t in ts:
    t.join()
# count() doest't expose its current value directly; one more next() gives us the count of next()s so far (off by one)
print("approximate total =", next(counter) - 1, "expected", 4 * N)
