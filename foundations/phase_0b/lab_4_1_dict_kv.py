"""Phase 0b · Lab 4.1 — dict as a key-value store."""

kv: dict[str, bytes] = {}
vr: dict[str, int] = {}


def put(k: str, v: str | bytes) -> None:
    kv[k] = v.encode() if isinstance(v, str) else v
    vr[k] = vr.get(k, 0) + 1


def get(k: str) -> tuple[bytes | None, int]:
    return kv.get(k), vr.get(k, 0)


def delete(k: str) -> bool:
    return kv.pop(k, None) is not None


def scan(prefix: str) -> dict[str, bytes]:
    return {k: v for k, v in kv.items() if k.startswith(prefix)}


def cas(
    k: str, expected: str | bytes, desired: str | bytes
) -> tuple[bool, bytes | None]:
    current = kv.get(k)
    if current == expected:
        put(k, desired)
        return True, kv.get(k)
    return False, current


put("/users/alice/name", "Alice")
put("/users/alice/age", "32")
put("/users/bob/name", "Bob")

print(get("/users/alice/name"))
print(scan("/users/alice/"))

delete("/users/bob/name")

print(scan("/users/"))
print(cas("/users/alice/name", b"Alice", "sara"))
print(get("/users/alice/name"))
print(scan("/users/alice/"))

print(cas("users/alice/name", b"Alice", "Jhon"))
print(get("users/alice/name"))
