import http.server
import urllib.request
import urllib.error
import json
import os
import re
import threading

CLAUDE_BACKEND_URL = 'https://script.google.com/macros/s/AKfycbygP5mGHqEprhWDEVhEYahonPnPhZLSpwLoGo5n39-RttowqSp_qKAs1MEYERrZ0kaz/exec'
AIRTABLE_BASE = 'appEUXFXlnxrxY4OG'
AIRTABLE_TABLE = 'Activities'
HTML_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')


def fetch_airtable_images():
    token = os.environ.get('AIRTABLE_PAT', '')
    if not token or not token.startswith('pat'):
        print('[Airtable] No valid PAT found, skipping image refresh')
        return

    print('[Airtable] Refreshing activity images...')
    try:
        records = []
        offset = None
        while True:
            url = f'https://api.airtable.com/v0/{AIRTABLE_BASE}/{AIRTABLE_TABLE}?fields[]=Name&fields[]=Gallery+Image'
            if offset:
                url += f'&offset={offset}'
            req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.load(r)
            records.extend(data.get('records', []))
            offset = data.get('offset')
            if not offset:
                break

        img_map = {}
        for rec in records:
            name = rec['fields'].get('Name', '').strip()
            imgs = rec['fields'].get('Gallery Image', [])
            if imgs and name:
                img_map[name] = imgs[0].get('url', '')

        if not img_map:
            print('[Airtable] No images found')
            return

        with open(HTML_FILE, 'r', encoding='utf-8') as f:
            html = f.read()

        replacements = 0
        for name, new_url in img_map.items():
            escaped = re.escape(name)
            pattern = rf'(name:\s*"{escaped}"(?:(?!name:).)*?image:\s*)"https://[^"]*"'
            new_html, count = re.subn(pattern, rf'\g<1>"{new_url}"', html, flags=re.DOTALL)
            if count > 0:
                html = new_html
                replacements += count

        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f'[Airtable] Updated {replacements} image URLs from {len(img_map)} records')
    except Exception as e:
        print(f'[Airtable] Image refresh failed: {e}')


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
    # Refresh images in background so startup isn't delayed
    threading.Thread(target=fetch_airtable_images, daemon=True).start()
    server = http.server.HTTPServer(('0.0.0.0', 5000), Handler)
    print('Serving on http://0.0.0.0:5000')
    server.serve_forever()
