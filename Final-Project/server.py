import http.server
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from Sequence import Seq
import jinja2 as j

PORT = 8080

def read_html_file(filename):  # filename = "get.html"
    contents = Path("./html/" + filename).read_text()  # "./html/get.html"
    contents = j.Template(contents)
    return contents

socketserver.TCPServer.allow_reuse_address = True



class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')
        parsed_url = urlparse(self.path)  # path = url
        path = parsed_url.path
        params = parse_qs(parsed_url.query)
        print(path, params)

        if path == "/":
            contents = Path("html/Index.html").read_text()
            self.send_response(200)
        elif path == "/listSpecies":
            try:
                limit_number = int(params['limit'][0])  # 2
                contents = read_html_file(path[1:] + ".html").\
                    render(context={'limit': limit_number})
                self.send_response(200)
            except (KeyError, IndexError, ValueError):
                contents = Path(HTML_FOLDER + "error.html").read_text()
                self.send_response(404)
        elif path == "/karyotype":
            try:
                sequence_number = int(params['sequence_number'][0])  # 2
                sequence = Seq(SEQUENCES[sequence_number])  # "ATCG"
                contents = read_html_file(path[1:] + ".html").\
                    render(context={'The total number of species in ensemble is': sequence_number,
                                    'The limit you have selected is': sequence,
                                    'The names of the species are': sequence})
                self.send_response(200)
            except (KeyError, IndexError, ValueError):
                contents = Path(HTML_FOLDER + "error.html").read_text()
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