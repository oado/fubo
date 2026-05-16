"""Quick deploy: start local HTTP server + create public tunnel."""
import http.server
import socketserver
import threading
import subprocess
import sys
import os
import time
import json
import urllib.request

PORT = 8765
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # Serve daily-checklist.html as root
        if self.path == '/' or self.path == '':
            self.path = '/daily-checklist.html'
        return super().do_GET()

    def log_message(self, format, *args):
        pass  # Suppress logs

def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Local server running on http://localhost:{PORT}")
        httpd.serve_forever()

def create_tunnel():
    """Create a localtunnel using Node.js."""
    node_path = r"C:\Users\Administrator\.workbuddy\binaries\node\versions\22.12.0\node.exe"
    script = r"C:\Users\Administrator\WorkBuddy\2026-05-15-task-1\node_modules\localtunnel\bin\lt.js"

    # Start tunnel
    proc = subprocess.Popen(
        [node_path, script, "--port", str(PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Wait for tunnel URL
    for _ in range(30):
        line = proc.stdout.readline().strip()
        if line:
            print(f"Tunnel URL: {line}")
            return line, proc
        time.sleep(1)

    print("Timeout waiting for tunnel URL")
    err = proc.stderr.read()
    if err:
        print(f"Error: {err}")
    return None, proc

if __name__ == "__main__":
    # Start server in background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Create tunnel
    url, proc = create_tunnel()

    if url:
        # Save URL for reference
        with open(os.path.join(DIRECTORY, "tunnel_url.txt"), "w") as f:
            f.write(url)
        print(f"\n{'='*50}")
        print(f"Public URL: {url}")
        print(f"{'='*50}")
        print("Press Ctrl+C to stop the server and tunnel.")

        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")
            proc.terminate()
