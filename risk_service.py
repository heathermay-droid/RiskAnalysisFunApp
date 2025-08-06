"""
Risk Analysis microservice for Along Came Polly.

This module provides a WSGI-based microservice that exposes API
endpoints to compute risk scores and serves a React front‑end. The
server does not depend on external frameworks and uses only the
standard library plus Jinja2 for HTML templating. However, the
frontend is served as a static file located in the ``frontend``
directory and uses React loaded via CDN.

Endpoints:

* ``/api/risks`` – Returns JSON with total and per-factor weighted
  risks for all persons defined in ``risk_logic``.
* ``/api/risk/<person>`` – Returns JSON with total and per-factor
  weighted risks for a single person ("Polly" or "Lisa").
* ``/`` or ``/index.html`` – Serves the React front‑end.

Run this script directly to start the service on http://localhost:8001.
"""
import json
import os
from typing import Callable, Iterable
from wsgiref.simple_server import make_server

from risk_logic import compute_weighted_risk, compute_all_risks


FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")


def read_frontend_file() -> bytes:
    """Read the front-end HTML file from disk."""
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    with open(index_path, "rb") as f:
        return f.read()


def build_table_data() -> list:
    """Builds full risk table including weighted values for API."""
    from risk_logic import RISK_TABLE  # import here to avoid circular import
    rows = []
    for row in RISK_TABLE:
        severity = float(row["severity"])
        polly_score = float(row["Polly"])
        lisa_score = float(row["Lisa"])
        polly_weighted = severity * polly_score
        lisa_weighted = severity * lisa_score
        rows.append(
            {
                "factor": row["factor"],
                "severity": severity,
                "Polly": polly_score,
                "Lisa": lisa_score,
                "polly_weighted": polly_weighted,
                "lisa_weighted": lisa_weighted,
            }
        )
    return rows


def application(environ: dict, start_response: Callable) -> Iterable[bytes]:
    """
    WSGI application serving API endpoints and static front-end.

    Parameters
    ----------
    environ : dict
        The WSGI environment dictionary.
    start_response : callable
        Callable for starting the HTTP response.
    """
    path = environ.get("PATH_INFO", "/")
    method = environ.get("REQUEST_METHOD", "GET").upper()
    # Handle API endpoints
    if path.startswith("/api/risks") and method == "GET":
        # Return complete table and totals
        total_data = compute_all_risks()
        table_rows = build_table_data()
        response = {
            "rows": table_rows,
            "totals": {person: total_data[person]["total"] for person in total_data},
        }
        body = json.dumps(response).encode("utf-8")
        headers = [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(body))),
            ("Access-Control-Allow-Origin", "*"),
        ]
        start_response("200 OK", headers)
        return [body]
    elif path.startswith("/api/risk/") and method == "GET":
        # Return risk for a single person
        person = path.split("/", 3)[-1]
        try:
            total, details = compute_weighted_risk(person)
            data = {"person": person, "total": total, "details": details}
            body = json.dumps(data).encode("utf-8")
            headers = [
                ("Content-Type", "application/json"),
                ("Content-Length", str(len(body))),
                ("Access-Control-Allow-Origin", "*"),
            ]
            start_response("200 OK", headers)
            return [body]
        except Exception as ex:
            error = {"error": str(ex)}
            body = json.dumps(error).encode("utf-8")
            start_response("404 Not Found", [("Content-Type", "application/json"), ("Content-Length", str(len(body)))])
            return [body]
    # Serve front-end for root or index
    elif path in ("/", "/index", "/index.html") and method == "GET":
        body = read_frontend_file()
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8"), ("Content-Length", str(len(body)))])
        return [body]
    else:
        # Not found
        body = b"Not Found"
        start_response("404 Not Found", [("Content-Type", "text/plain"), ("Content-Length", str(len(body)))])
        return [body]


def run(host: str = "127.0.0.1", port: int = 8001) -> None:
    """Run the risk analysis microservice server."""
    with make_server(host, port, application) as httpd:
        print(f"Risk microservice running at http://{host}:{port}")
        httpd.serve_forever()


if __name__ == "__main__":
    run()