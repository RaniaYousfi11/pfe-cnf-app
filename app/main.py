from flask import Flask
import os
import socket
import time

app = Flask(__name__)

PRODUCT = os.getenv("PRODUCT", "CNF")
SITE = os.getenv("SITE", "unknown-site")
CNF_NAME = os.getenv("CNF_NAME", "unknown-cnf")
START_TIME = time.time()

@app.route("/")
def home():
    return {
        "status": "running",
        "product": PRODUCT,
        "site": SITE,
        "cnf": CNF_NAME,
        "pod": socket.gethostname(),
        "uptime_seconds": int(time.time() - START_TIME)
    }

@app.route("/health")
def health():
    return {"status": "healthy"}

@app.route("/metrics")
def metrics():
    return (
        "cnf_up 1\n"
        "cnf_requests_total 1\n"
    ), 200, {"Content-Type": "text/plain; charset=utf-8"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
