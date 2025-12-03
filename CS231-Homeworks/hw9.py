#!/usr/bin/env python3
"""Web Service Assignment 11/3–11/9"""

import http.server, subprocess


class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Run the system command "date -R"
        date_text = subprocess.check_output(["date", "-R"], text=True).strip()
        body = (date_text + "\n").encode("utf-8")

        # Send HTTP response
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    # (Optional) silence log messages:
    # def log_message(self, *args):
    #     return


def main():
        # Let HTTPServer bind directly to port 0 (safer & simpler), OS chooses a free port
        server = http.server.HTTPServer(("", 0), MyHandler)

        # After binding, retrieve the actual port
        port = server.server_address[1]

        print(f"Server listening on port: {port}")
        print(f"Local access at: http://localhost:{port}/")

        # Handle exactly one request, then exit
        server.handle_request()


if __name__ == "__main__":
    main()
