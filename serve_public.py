"""Start local HTTP server + create public tunnel via localtunnel."""
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
NODE_PATH = r"C:\Users\Administrator\.workbuddy\binaries\node\versions\22.12.0\node.exe"
LT_PATH = r"C:\Users\Administrator\WorkBuddy\2026-05-15-task-1\node_modules\localtunnel\bin\lt.js"

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
        [NODE_PATH, LT_PATH, "--port", str(PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    for line in proc.stdout:
        line = line.strip()
        # localtunnel outputs: your url is: https://xxx-xxx-xxx.loca.lt
        if "https://" in line and (".loca.lt" in line or ".lt" in line):
            url_match = re.search(r'(https?://[^\s]+)', line)
            if url_match:
                return url_match.group(1), proc
    return None, proc

if __name__ == "__main__":
    # Start server in background
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    print(f"Local server started on port {PORT}")

    # Create tunnel
    print("Creating public tunnel...")
    url, proc = create_tunnel()

    if url:
        print(f"\n{'='*60}")
        print(f"  Public URL: {url}")
        print(f"{'='*60}")
        print(f"\nShare this URL - anyone can open it in a browser!")
        print(f"Note: URL is active as long as this script runs.")
        print(f"Press Ctrl+C to stop.")

        # Save URL
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
