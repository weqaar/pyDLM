import http.client
import sys
import time
import uuid

SERVER = "localhost:8000"
ME = sys.argv[1] if len(sys.argv) > 1 else str(uuid.uuid4())


def call(path):
    conn = http.client.HTTPConnection(SERVER)
    conn.request("POST", path, headers={"X-Client-ID": ME})
    r = conn.getresponse()
    return r.status, r.read().decode()


print("acquire ->", call("/acquire"))
time.sleep(5)
print("release ->", call("/release"))
