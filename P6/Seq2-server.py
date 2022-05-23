import http.server
import socketserver
import termcolor
from pathlib import Path


PORT = 8080

socketserver.TCPServer.allow_reuse_address = True


class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        if self.path == "/":
            contents = Path("Form-1.html").read_text()
            self.send_response(200)
        elif self.path == "/ping?":
            contents = f"""
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="utf-8">
                    <title>PING</title>
                </head>
                <body>
                    <h1>PING OK!</h1>
                    <p>The SEQ2 server is running...</p>
                    <a href="/">Main page</a>
                </body>
            </html>"""
            self.send_response(200)

        else:
            contents = Path(f"Error.html").read_text()
            self.send_response(404)

        contents_bytes = contents.encode()
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(contents_bytes)))
        self.end_headers()

        self.wfile.write(contents_bytes)

        return


with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
    print("Serving at PORT...", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Stopped by the user")
        httpd.server_close()