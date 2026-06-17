"""Phase 0b · test basic threading.Lock lab."""

from __future__ import annotations

import threading

from foundations.phase_0b import lab_1_1_basic_lock as lab


def test_threads_complete_without_deadlock() -> None:
    """The lock-protected critical section should let all threads finish."""
    threads = [
        threading.Thread(target=lab.critical_section, args=(f"test-{index}",))
        for index in range(3)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join(timeout=5)

    assert all(not thread.is_alive() for thread in threads)
