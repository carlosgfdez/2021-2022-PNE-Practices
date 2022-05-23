import os
import http.server
import socketserver
import termcolor
from pathlib import Path
import jinja2 as j
from urllib.parse import urlparse, parse_qs
from Sequence import Seq

HTML_FOLDER = "./html/"
PORT = 8080
SEQUENCES = ["ACGTCCAGTAAA", "ACGTAGTTTTTAAACCC", "GGGTAAACTACG", "CGTAGTACGTA", "TGCATGCCGAT", "ATATATATATATATATATA"]
GENES = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]


def read_html_file(filename):  # filename = "get.html"
    contents = Path(HTML_FOLDER + filename).read_text()  # "./html/get.html"
    contents = j.Template(contents)
    return contents


socketserver.TCPServer.allow_reuse_address = True


class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        parsed_url = urlparse(self.path)  # path = url
        path = parsed_url.path
        params = parse_qs(parsed_url.query)
        print(path, params)

        if path == "/":
            context = {'n_sequences': len(SEQUENCES), 'genes': GENES}
            contents = read_html_file("index.html").render(context=context)
            self.send_response(200)  # Comment
        elif path == "/ping":
            contents = read_html_file(path[1:] + ".html").render()
            self.send_response(200)
        elif path == "/get":
            try:
                sequence_number = int(params['sequence_number'][0])  # 2
                sequence = Seq(SEQUENCES[sequence_number])  # "ATCG"
                contents = read_html_file(path[1:] + ".html").\
                    render(context={'sequence_number': sequence_number, 'sequence': sequence})
                self.send_response(200)
            except (KeyError, IndexError, ValueError):
                contents = Path(HTML_FOLDER + "error.html").read_text()
                self.send_response(404)
        elif path == "/gene":
            try:
                gene_name = params['gene_name'][0]
                sequence = Seq()
                file_name = os.path.join("../..", "Genes", f"{gene_name}.txt")
                sequence.read_fasta(file_name)
                contents = read_html_file(path[1:] + ".html"). \
                    render(context={'gene_name': gene_name, 'sequence': sequence})
                self.send_response(200)
            except IndexError:
                contents = Path(HTML_FOLDER + "error.html").read_text()
                self.send_response(404)
        elif path == "/operation":
            try:
                bases = params['bases'][0]  # bases = "ATCG"
                op = params['op'][0]  # op = "comp"
                if op in ["info", "comp", "rev"]:
                    sequence = Seq(bases)

                    if op == "info":
                        contents = read_html_file(parsed_url.path[1:] + ".html"). \
                            render(context={'sequence': sequence, 'op': op, 'result': sequence.info()})
                    elif op == "comp":
                        contents = read_html_file(parsed_url.path[1:] + ".html"). \
                            render(context={'sequence': sequence, 'op': op, 'result': sequence.complement()})
                    else:  # elif op == "rev":
                        contents = read_html_file(parsed_url.path[1:] + ".html"). \
                            render(context={'sequence': sequence, 'op': op, 'result': sequence.reverse()})
                    self.send_response(200)
                else:
                    contents = Path(HTML_FOLDER + "error.html").read_text()
                    self.send_response(404)
            except IndexError:
                contents = Path(HTML_FOLDER + "error.html").read_text()
                self.send_response(404)
        else:
            contents = Path(HTML_FOLDER + "error.html").read_text()
            self.send_response(404)

        contents_bytes = contents.encode()
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(contents_bytes)))
        self.end_headers()

        self.wfile.write(contents_bytes)

        return


with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print("Serving at PORT...", PORT)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Stopped by the user")
        httpd.server_close()

