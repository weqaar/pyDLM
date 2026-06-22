"""Phase 0b · Lab 5.1 — tiny content-addressed blob store.

Run::

    poetry run python foundations/phase_0b/lab_5_1_blob.py
"""

import hashlib
import pathlib

ROOT = pathlib.Path("/tmp/lab_5_1_blobs")
ROOT.mkdir(parents=True, exist_ok=True)


def put_blob(data: bytes) -> str:
    h = hashlib.sha256(data).hexdigest()
    target = ROOT / h[:2] / h

    target.parent.mkdir(parents=True, exist_ok=True)

    if not target.exists():
        target.write_bytes(data)

    return h


def get_blob(h: str) -> bytes:
    return (ROOT / h[:2] / h).read_bytes()


h1 = put_blob(b"hello world")
h2 = put_blob(b"hello world")

print(h1 == h2)
print(get_blob(h1))
