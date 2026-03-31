from http.server import BaseHTTPRequestHandler, HTTPServer
import os

PORT = int(os.getenv("PORT", "8000"))

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        msg = f"Hello from Docker! PORT={PORT}\n"
        self.wfile.write(msg.encode())

if __name__ == "__main__":
    HTTPServer(("", PORT), Handler).serve_forever()