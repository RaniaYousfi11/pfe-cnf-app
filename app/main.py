import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

PRODUCT = os.getenv("PRODUCT", "CNF")
SITE = os.getenv("SITE", "unknown-site")
CNF_NAME = os.getenv("CNF_NAME", "unknown-cnf")
STATUS = os.getenv("STATUS", "running-from-github-actions")
PORT = int(os.getenv("PORT", "8080"))

class Handler(BaseHTTPRequestHandler):
    def _send_json(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        if self.path in ["/", "/health"]:
            self._send_json(200, {
                "status": STATUS,
                "product": PRODUCT,
                "site": SITE,
                "cnf_name": CNF_NAME,
                "port": PORT
            })
        elif self.path == "/metrics":
            metrics = (
                f'cnf_status{{product="{PRODUCT}",site="{SITE}",cnf="{CNF_NAME}"}} 1\n'
            )
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(metrics.encode("utf-8"))
        else:
            self._send_json(404, {"error": "not found"})

    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"CNF app started on 0.0.0.0:{PORT}")
    server.serve_forever()
