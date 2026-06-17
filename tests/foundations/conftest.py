"""Shared pytest configuration for foundation tests."""

from __future__ import annotations

import pytest  # pyright: ignore[reportMissingImports]
import redis  # pyright: ignore[reportMissingModuleSource]
import redis.exceptions  # pyright: ignore[reportMissingModuleSource]


def pytest_collection_modifyitems(
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    """Skip Phase 0a tests when Redis is not reachable."""
    try:
        redis.Redis(host="127.0.0.1", port=6379, decode_responses=True).ping()
        return
    except ConnectionError:
        skip = pytest.mark.skip(reason="Redis not reachable on localhost:6379")
        for item in items:
            if "phase_0a" in str(item.fspath):
                item.add_marker(skip)
