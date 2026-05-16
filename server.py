import http.server, socketserver, os
DIRECTORY = r"C:\Users\Administrator\WorkBuddy\2026-05-15-task-1"
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s, *a, **k):
        super().__init__(*a, directory=DIRECTORY, **k)
    def do_GET(s):
        if s.path in ('/', ''): s.path = '/index.html'
        return super().do_GET()
    def log_message(s, *a): pass
with socketserver.TCPServer(("", 8765), H) as h: h.serve_forever()
