"""Phase 0b · Lab 3.1 try-this — multiprocessing.Value with and without lock.
Run::
    poetry run python foundations/phase_0b/lab_3_1_try_multiprocessing_value.py
"""

from multiprocessing import Process, Value

N = 100_000
NUM_PROCESSES = 4


def bump_without_lock(counter) -> None:
    for _ in range(N):
        counter.value = counter.value + 1


def bump_with_lock(counter) -> None:
    for _ in range(N):
        with counter.get_lock():
            counter.value = counter.value + 1


def run_without_lock() -> None:
    counter = Value("i", 0)

    processes = [
        Process(target=bump_without_lock, args=(counter,)) for _ in range(NUM_PROCESSES)
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    print("without lock =", counter.value, "expected", NUM_PROCESSES * N)


def run_with_lock() -> None:
    counter = Value("i", 0)

    processes = [
        Process(target=bump_with_lock, args=(counter,)) for _ in range(NUM_PROCESSES)
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    print("with lock    =", counter.value, "expected", NUM_PROCESSES * N)


if __name__ == "__main__":
    run_without_lock()
    run_with_lock()
