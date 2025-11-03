#!/usr/bin/env python3

import http.server, subprocess, socket

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        date_text = subprocess.check_output(["date", "-R"], text=True).strip()
        body = (date_text + "\n").encode("utf-8")
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

def main():
    # determine free, high socket number
    with socket.socket() as s:
        s.bind(("", 0))  # Ask OS for an available high-numbered port
        port = s.getsockname()[1]

    server = http.server.HTTPServer(("", port), MyHandler)
    print(f"Server listening on port: {port}")
    print(f"Local access at: http://localhost:{port}/")
    server.handle_request()

if __name__ == "__main__":
    main()

