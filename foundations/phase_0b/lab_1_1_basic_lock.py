"""Phase 0b · Lab 1.1 — basic threading.Lock example.

Run::

    poetry run python foundations/phase_0b/lab_1_1_basic_lock.py
"""

import threading
import time

lock = threading.Lock()


def critical_section(name: str) -> None:
    print(f"{name}: waiting for the lock")

    with lock:
        print(f"{name}: got the lock")
        time.sleep(1)
        print(f"{name}: releasing the lock")


threads = [threading.Thread(target=critical_section, args=(f"t{i}",)) for i in range(3)]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
