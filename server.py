import http.server
import urllib.request
import urllib.error
import json
import os

CLAUDE_BACKEND_URL = 'https://script.google.com/macros/s/AKfycbygP5mGHqEprhWDEVhEYahonPnPhZLSpwLoGo5n39-RttowqSp_qKAs1MEYERrZ0kaz/exec'

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/claude':
            try:
                length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(length)

                req = urllib.request.Request(
                    CLAUDE_BACKEND_URL,
                    data=body,
                    headers={'Content-Type': 'text/plain;charset=utf-8'},
                    method='POST'
                )

                with urllib.request.urlopen(req, timeout=30) as resp:
                    response_body = resp.read()

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(response_body)

            except Exception as e:
                error = json.dumps({'success': False, 'error': str(e)}).encode()
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(error)
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        print(f'{self.address_string()} - {format % args}')

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = http.server.HTTPServer(('0.0.0.0', 5000), Handler)
    print('Serving on http://0.0.0.0:5000')
    server.serve_forever()
