from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

state: dict[str, str | None] = {"holder": None}
lk = threading.Lock()


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        client = self.headers.get("X-Client-ID", "anonymous")

        if self.path == "/acquire":
            with lk:
                granted = state["holder"] is None
                if granted:
                    state["holder"] = client
            self._reply(
                200 if granted else 409,
                f'{{"granted": {str(granted).lower()}, "holder": "{state["holder"]}"}}',
            )
        elif self.path == "/release":
            with lk:
                ok = state["holder"] == client
                if ok:
                    state["holder"] = None

            self._reply(200 if ok else 403, f'{{"released": {str(ok).lower()}}}')
        else:
            self._reply(404, '{"error":"unknown"}')

    def _reply(self, code, body):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body.encode())

    def log_message(self, format: str, *args: object) -> None:
        pass


HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
