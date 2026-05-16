"""Start local HTTP server + Cloudflare tunnel for instant public URL."""
import http.server
import socketserver
import threading
import subprocess
import sys
import os
import time
import re

PORT = 8765
DIRECTORY = r"C:\Users\Administrator\WorkBuddy\2026-05-15-task-1"
CLOUDFLARED = os.path.join(DIRECTORY, "cloudflared.exe")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    def do_GET(self):
        if self.path == '/' or self.path == '':
            self.path = '/index.html'
        return super().do_GET()
    def log_message(self, format, *args):
        pass

def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

def create_tunnel():
    proc = subprocess.Popen(
        [CLOUDFLARED, "tunnel", "--url", f"http://localhost:{PORT}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    for line in proc.stdout:
        line = line.strip()
        url_match = re.search(r'(https://[a-z0-9-]+\.trycloudflare\.com)', line)
        if url_match:
            return url_match.group(1), proc
    return None, proc

if __name__ == "__main__":
    # Start server
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    print(f"Local server started on port {PORT}")

    # Create tunnel
    print("Creating Cloudflare tunnel...")
    url, proc = create_tunnel()

    if url:
        print(f"\n{'='*60}")
        print(f"  Public URL: {url}")
        print(f"{'='*60}")
        print(f"\nAnyone can open this URL in a browser!")
        print(f"Works on mobile too!")
        print(f"URL is active while this script runs.")

        with open(os.path.join(DIRECTORY, "public_url.txt"), "w") as f:
            f.write(url)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")
            proc.terminate()
    else:
        print("Failed to create tunnel")
        proc.terminate()
