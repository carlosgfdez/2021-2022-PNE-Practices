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
            contents = Path("form-EX02.html").read_text()
            self.send_response(200)
        elif self.path.startswith("/echo?"):
            content_1 = self.path.split("?")[1]
            content_2 = content_1.split("=")[1]
            try:
                contents = f"""
                    <!DOCTYPE html>
                    <html lang="en">
                        <head>
                            <meta charset="utf-8">
                            <title>Result</title>
                        </head>
                        <body>
                            <h1>Received message:</h1>
                            """
                if 'capital_letters' in self.path:
                    content_3 = content_2.split("&")[0]
                    contents += f"<p>{content_3.upper()}</p>"
                else:
                    contents += f"<p>{content_2}</p>"
                contents += """
                            <a href="/">Main page</a>
                        </body>
                    </html>"""
                self.send_response(200)
            except (KeyError, IndexError):
                contents = Path(f"Error.html").read_text()
                self.send_response(404)
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