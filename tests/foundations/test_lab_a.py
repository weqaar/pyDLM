"""Phase 0a · test that the threading race actually races."""

from __future__ import annotations

import pytest  # pyright: ignore[reportMissingImports]
import redis  # pyright: ignore[reportMissingModuleSource]

from foundations.phase_0a import lab_a_threading_race as lab


@pytest.fixture
def client() -> redis.Redis:
    """Return a clean Redis client."""
    c = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
    c.flushdb()
    return c


def test_race_loses_updates(client: redis.Redis) -> None:
    """The naive code is supposed to be wrong. Prove it."""
    lab.main()
    final = int(client.get(lab.KEY) or 0)
    expected = lab.NUM_THREADS * lab.INCREMENTS
    assert final < expected, "expected a race, but the counter was exact"
