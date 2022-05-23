import os
import http.server
import socketserver
import termcolor
from pathlib import Path
from Sequence import Seq


PORT = 8080

socketserver.TCPServer.allow_reuse_address = True

genes = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]

class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        if self.path == "/":
            contents = Path("form-4.html").read_text()
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
        elif self.path.startswith("/get?"):
            content_1 = self.path.split("?")[1]
            content_2 = content_1.split("=")[1]
            try:
                sequence_number = int(content_2)
                sequence = Seq()
                file_name = os.path.join("..", "Genes", f"{genes[sequence_number]}.txt")
                sequence.read_fasta(file_name)
                contents = f"""
                    <!DOCTYPE html>
                    <html lang="en">
                        <head>
                            <meta charset="utf-8">
                            <title>GET</title>
                        </head>
                        <body>
                            <h1>Sequence number {sequence_number}:</h1>
                            <p>{sequence}</p>
                            <a href="/">Main page</a>
                        </body>
                    </html>"""
                self.send_response(200)
            except (IndexError, ValueError):
                contents = Path(f"Error.html").read_text()
                self.send_response(404)


        elif  self.path.startswith("/gene?"):
            content_1 = self.path.split("?")[1]
            content_2 = content_1.split("=")[1]
            try:
                sequence = Seq()
                sequence_gene = content_2
                file_name = os.path.join("..", "Genes", f"{sequence_gene}.txt")
                sequence.read_fasta(file_name)
                contents = f"""
                    <!DOCTYPE html>
                    <html lang="en">
                        <head>
                            <meta charset="utf-8">
                            <title>GET</title>
                        </head>
                        <body>
                            <h1>Sequence gene {sequence_gene}:</h1>
                            <p>{sequence}</p>
                            <a href="/">Main page</a>
                        </body>
                    </html>"""
                self.send_response(200)
            except (IndexError, ValueError):
                contents = Path(f"Error.html").read_text()
                self.send_response(404)


        elif self.path.startswith("/operate?"):
            content_1 = self.path.split("?")[1]
            content_2 = content_1.split("=")[1]
            sequence_gene = content_2.split("&")[0]


            try:
                sequence = Seq(sequence_gene)
                if 'info' in self.path:
                    task = 'info'
                    text = f"<p>{sequence.info()}</p>"
                elif 'comp' in self.path:
                    task = 'complement'
                    text = f"<p>{sequence.complement()}</p>"
                elif 'reverse' in self.path:
                    task = 'rev'
                    text = f"<p>{sequence.reverse()}</p>"

                contents = f"""
                    <!DOCTYPE html>
                    <html lang="en">
                        <head>
                            <meta charset="utf-8">
                            <title>GET</title>
                        </head>
                        <body>
                            <h1>Sequence:</h1>
                            <p>{sequence_gene}</p>
                            <h1>Operation:</h1>
                            <p>{task}</p>
                            <h1>Result</h1>
                            {text} 
                            <a href="/">Main page</a>
                        </body>
                    </html>"""
                
                self.send_response(200)
            except (IndexError, ValueError):
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