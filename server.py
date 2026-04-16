import urllib.request
import json
import os
import re
import threading

from flask import Flask, request, jsonify, send_from_directory

CLAUDE_BACKEND_URL = 'https://script.google.com/macros/s/AKfycbygP5mGHqEprhWDEVhEYahonPnPhZLSpwLoGo5n39-RttowqSp_qKAs1MEYERrZ0kaz/exec'
AIRTABLE_BASE = 'appEUXFXlnxrxY4OG'
AIRTABLE_TABLE = 'Activities'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(BASE_DIR, 'index.html')

app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')


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


@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')


@app.route('/sw.js')
def service_worker():
    response = send_from_directory(BASE_DIR, 'sw.js')
    response.headers['Cache-Control'] = 'no-cache'
    return response


@app.route('/api/claude', methods=['POST', 'OPTIONS'])
def claude_proxy():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    try:
        body = request.get_data()
        req = urllib.request.Request(
            CLAUDE_BACKEND_URL,
            data=body,
            headers={'Content-Type': 'text/plain;charset=utf-8'},
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            response_body = resp.read()

        response = app.response_class(
            response=response_body,
            status=200,
            mimetype='application/json'
        )
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    except Exception as e:
        response = jsonify({'success': False, 'error': str(e)})
        response.status_code = 500
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


if __name__ == '__main__':
    threading.Thread(target=fetch_airtable_images, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=False)
