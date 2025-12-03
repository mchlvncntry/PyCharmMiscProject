#!/usr/bin/env python3
"""Serve the output of `date -R` over HTTP on a dynamically assigned high port."""

import http.server
import subprocess
import socket

class DateHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            text = subprocess.check_output(["date", "-R"], text=True).strip()
        except Exception as e:
            # Minimal, user-friendly fallback; assignment doesn't require full error handling.
            text = f"Error running `date -R`: {e}"

        body = (text + "\n").encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

def main():
    # Bind to all interfaces on an OS-assigned free high port.
    server = http.server.HTTPServer(("", 0), DateHandler)
    host, port = server.server_address  # host may be '' (0.0.0.0)
    hostname = socket.gethostname()

    print(f"Server listening on port {port}")
    print(f"Local access:   http://localhost:{port}/")
    print(f"Network access: http://{hostname}:{port}/")
    # Handle exactly one request, then exit. Use serve_forever() for a long-running server.
    server.handle_request()

if __name__ == "__main__":
    main()
