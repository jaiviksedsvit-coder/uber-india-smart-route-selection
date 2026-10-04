import http.server
import socketserver
import os
import sys

PORT = 3000
WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PROTOTYPE_DIR = os.path.join(WORKSPACE_DIR, 'prototype')
DOCS_DIR = os.path.join(WORKSPACE_DIR, 'docs')

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        clean_path = path.split('?')[0].split('#')[0]
        if clean_path.startswith('/docs/'):
            rel = clean_path[len('/docs/'):]
            return os.path.join(DOCS_DIR, rel)
        else:
            if clean_path == '/' or clean_path == '':
                clean_path = '/index.html'
            rel = clean_path.lstrip('/')
            return os.path.join(PROTOTYPE_DIR, rel)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

def run():
    ThreadingHTTPServer.allow_reuse_address = True
    with ThreadingHTTPServer(("", PORT), CustomHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}/ (multi-threaded, no-cache)...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    run()
