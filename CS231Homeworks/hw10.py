'''
Write an HTTP service that chooses an available high port number and serves a single
copy of a memorable text to the first request that comes in. Because of firewall rules,
requests to services running on hills have to come from within the college network
'''

import http.server


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write('Hello!\n'.encode())


if __name__ == '__main__':
    server = ('', 8118)
    httpd = http.server.HTTPServer(server, Handler)
    httpd.serve_forever()


