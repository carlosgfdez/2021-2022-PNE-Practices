import http.server
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from Sequence import Seq
import jinja2 as j
import http.client
import json
from Sequence import Seq
from http import HTTPStatus


SERVER = "rest.ensembl.org"
PORT = 8080
def read_html_file(filename):
    contents = Path("./html/" + filename).read_text()
    contents = j.Template(contents)
    return contents

def read_template_html_file(filename):
    import jinja2
    from pathlib import Path
    content = jinja2.Template(Path(filename).read_text())
    return content


def connect_web(URL, ENDPOINT):
    conn = http.client.HTTPConnection(SERVER)
    PARAMETER = "?content-type=application/json"
    CONTENT = URL + PARAMETER + ENDPOINT
    try:
        conn.request("GET", CONTENT)
    except ConnectionRefusedError:
        print("ERROR! Cannot connect to the Server")
        exit()

    response = conn.getresponse()
    if response.status == HTTPStatus.OK:
        print(f"Response received: {response.status} {response.reason}\n")

        data_1 = response.read().decode("utf-8")
        data = json.loads(data_1)
    return data



socketserver.TCPServer.allow_reuse_address = True



class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')
        parsed_url = urlparse(self.path)  # path = url
        path = parsed_url.path
        params = parse_qs(parsed_url.query)
        print(f"Endpoints: {path}, Parameters: {params}")

        if path == "/":
            contents = Path("html/Index.html").read_text()
            self.send_response(200)
        elif path == "/listSpecies":
            try:
                species_dict_1 = connect_web("/info/species", "")
                limit_number = int(params['limit'][0])
                species_dict_2 = species_dict_1["species"]
                total_number = len(species_dict_2)
                species_list = []
                for element in range(0, limit_number):
                    species_list.append(species_dict_2[element]["common_name"])
                species = ""
                for element in species_list:
                    species += f"·{element.capitalize()}<br>"

                contents = read_html_file(path[1:] + ".html").\
                    render(context={"species": species,
                                    "total": total_number,
                                    "limit": limit_number})
                self.send_response(200)
            except (KeyError, IndexError, ValueError):
                contents = Path("./html/" + "error.html").read_text()
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