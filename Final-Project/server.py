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
import os


SERVER = "rest.ensembl.org"
PORT = 8080

GENES = {"FRAT1": "ENSG00000165879",
         "ADA": "ENSG00000196839",
         "FXN": "ENSG00000165060",
         "RNU6_269P": "ENSG00000212379",
         "MIR633": "ENSG00000207552",
         "TTTY4C": "ENSG00000228296",
         "RBMY2YP": "ENSG00000227633",
         "FGFR3": "ENSG00000068078",
         "KDR": "ENSG00000128052",
         "ANK2": "ENSG00000145362"}


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
    CONTENT = URL + ENDPOINT + PARAMETER
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
        print(data)
    return data

def genes_information(gene_1):
    if gene_1 in GENES:
        SERVER = 'rest.ensembl.org'
        ENDPOINT = '/sequence/id'
        RESOURCE = f'/{GENES[gene_1]}?content-type=application/json'
        URL = SERVER + ENDPOINT + RESOURCE
        CONTENT = ENDPOINT + RESOURCE

        conn = http.client.HTTPConnection(SERVER)

        try:
            conn.request("GET", CONTENT)
        except ConnectionRefusedError:
            print("ERROR! Cannot connect to the Server")
            exit()
        response = conn.getresponse()

        if response.status == HTTPStatus.OK:
            print(f"Response received: {response.status} {response.reason}")
            print()

            data_1 = response.read().decode("utf-8")
            data = json.loads(data_1)
            return data


    else:
        print("Choose a correct gene")


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

            species_dict_1 = connect_web("/info/species", "")
            species_dict_2 = species_dict_1["species"]
            total_number = len(species_dict_2)

            if len(params) == 1:
                limit_number = int(params['limit'][0])
            elif len(params) == 0:
                limit_number = total_number
            else:
                contents = Path("./html/" + "error.html").read_text()
                self.send_response(404)

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


        elif path == "/karyotype":
            if len(params) == 1:
                specie_name = params['specie'][0]
                karyotype_dict_1 = connect_web("info/assembly/", specie_name)
                karyotype_dict_2 = karyotype_dict_1["karyotype"]
                karyo = ""
                for element in karyotype_dict_2:
                    karyo += f"·{element}<br>"
                print(karyo)
                contents = read_html_file(path[1:] + ".html").\
                    render(context={'karyotype': karyo})
                self.send_response(200)

            else:
                contents = Path("./html/" + "error.html").read_text()
                self.send_response(404)

        elif path == "/chromosomeLength":
            if len(params) == 2:
                specie_name = params['specie'][0]
                chromosome_number = params['chromo'][0]
                chromo_dict_1 = connect_web("info/assembly/", specie_name)
                chromo_dict_2 = chromo_dict_1["top_level_region"]
                chromo_length = 0

                for e in range(0,len(chromo_dict_2)):
                    chromo_length += int(chromo_dict_2[e]["length"])

                contents = read_html_file(path[1:] + ".html"). \
                    render(context={'length': chromo_length})
                self.send_response(200)

            else:
                contents = Path("./html/" + "error.html").read_text()
                self.send_response(404)

        elif path == "/geneSeq":
            if len(params) == 1:
                user_gene = params['gene'][0]
                info_dict = genes_information(user_gene)
                sequence = info_dict['seq']


                contents = read_html_file(path[1:] + ".html"). \
                    render(context={"gene": user_gene,
                                    "sequence": sequence})
                self.send_response(200)
            else:
                contents = Path(f"Error.html").read_text()
                self.send_response(404)

        elif path == "/geneInfo":
            if len(params) == 1:
                user_gene = params['gene'][0]
                info_dict = genes_information(user_gene)
                sequence = info_dict['seq']
                id_info = info_dict['id']
                sequence_length = len(sequence)
                chromosome_info_1 = info_dict['desc']
                chromosome_info_2 = chromosome_info_1.split(":")
                chromosome_name = chromosome_info_2[1]
                chromosome_start = chromosome_info_2[3]
                chromosome_end = chromosome_info_2[4]


                contents = read_html_file(path[1:] + ".html"). \
                    render(context={"gene": user_gene,
                                    "start": chromosome_start,
                                    "end": chromosome_end,
                                    "id": id_info,
                                    "length": sequence_length,
                                    "name": chromosome_name})
                self.send_response(200)
            else:
                contents = Path(f"Error.html").read_text()
                self.send_response(404)

        elif path == "/geneCalc":
            if len(params) == 1:
                user_gene = params['gene'][0]
                info_dict = genes_information(user_gene)
                sequence = info_dict['seq']
                length = Seq(sequence).len()
                bases = Seq(sequence).frequent_base()[1]
                percentage_bases = Seq(sequence).info()


                contents = read_html_file(path[1:] + ".html"). \
                    render(context={"gene": user_gene,
                                    "length": length,
                                    "bases": bases,
                                    "percentage": percentage_bases})
                self.send_response(200)
            else:
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