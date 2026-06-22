"""phase 0b . Lab 4.1 persisting kv store.
Run::
    poetry run python foundations/phase_0b/lab_4_2_kv_persistent.py
"""

import json
import pathlib


class KV:
    def __init__(self, path: str):
        self.path = pathlib.Path(path)
        if self.path.exists():
            self.data = json.loads(self.path.read_text())
        else:
            self.data = {}

    def _flush(self):
        self.path.write_text(json.dumps(self.data, indent=2))

    def put(self, k, v):
        self.data[k] = v
        self._flush()

    def get(self, k):
        return self.data.get(k)

    def delete(self, k):
        self.data.pop(k, None)
        self._flush()

    def scan(self, prefix):
        return {k: v for k, v in self.data.items() if k.startswith(prefix)}


kv = KV("/tmp/lab_4_2.json")
kv.put("/users/alice/name", "Alice")
print(kv.scan("/users/"))
