import http.server
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import jinja2 as j
import http.client
import json
from Sequence import Seq
from http import HTTPStatus


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


def connect_web(ENDPOINT, PARAMS):
    conn = http.client.HTTPConnection(SERVER)
    PARAMETER = "?content-type=application/json"
    CONTENT = ENDPOINT + PARAMETER + PARAMS
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
    SERVER = "rest.ensembl.org"
    ENDPOINT = "/sequence/id"
    RESOURCE = f"/{GENES[gene_1]}?content-type=application/json"
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
                species_dict_2 = species_dict_1["species"]
                total_number = len(species_dict_2)

                if len(params) == 1 or (len(params) == 2 and "json" in params):
                    limit_number = int(params["limit"][0])
                elif len(params) == 0:
                    limit_number = total_number
                else:
                    contents = Path("./html/" + "error.html").read_text()
                    self.send_response(404)

                species_list = []
                for element in range(0, limit_number):
                    species_list.append(species_dict_2[element]["common_name"])
                species = ""

                if "json" in params:
                    contents = {"species": species_list,
                                "total": total_number,
                                "limit": limit_number}
                else:
                    for element in species_list:
                        species += f"·{element.capitalize()}<br>"
                    contents = read_html_file(path[1:] + ".html").\
                        render(context={"species": species,
                                        "total": total_number,
                                        "limit": limit_number})
            except Exception:
                if "json" in params:
                    contents = {"Error": "An error ocurred. Try again with an integer"}
                else:
                    contents = read_html_file("error.html").\
                        render()


        elif path == "/karyotype":
            try:
                if len(params) == 1 or (len(params) == 2 and "json" in params):
                    specie_name = params["specie"][0]
                    karyotype_dict_1 = connect_web("info/assembly/" + specie_name, "")
                    karyotype_dict_2 = karyotype_dict_1["karyotype"]
                    karyo = ""

                    if "json" in params:
                        contents = {"karyotype": karyotype_dict_2}
                    else:
                        for element in karyotype_dict_2:
                            karyo += f"·{element}<br>"
                        contents = read_html_file(path[1:] + ".html").\
                            render(context={"karyotype": karyo})

                else:
                    contents = Path("./html/" + "error.html").read_text()
                    self.send_response(404)
            except Exception:
                if "json" in params:
                    contents = {"Error": "An error ocurred. Try again with a valid specie."}
                else:
                    contents = read_html_file("error.html").\
                        render()

        elif path == "/chromosomeLength":
            try:
                if len(params) == 2 or (len(params) == 3 and "json" in params):
                    specie_name = params["specie"][0]
                    chromosome_number = int(params["chromo"][0])
                    chromo_dict_1 = connect_web("info/assembly/" + specie_name, "")
                    chromo_dict_2 = chromo_dict_1["top_level_region"]
                    chromo_length = 0
                    chromo_list = []

                    if chromosome_number < 0:
                        contents = Path("./html/" + "error.html").read_text()
                        self.send_response(404)
                    else:
                        for e in range(0, len(chromo_dict_2)):
                            if int(chromo_dict_2[e]["length"]) > chromosome_number:
                                chromo_list.append(chromo_dict_2[e]["name"])
                        if len(chromo_list) == 0:
                            contents = Path("./html/" + "error.html").read_text()
                            self.send_response(404)
                        else:
                            if "json" in params:
                                contents = {"names": chromo_list}

                            else:
                                contents = read_html_file(path[1:] + ".html"). \
                                    render(context={"names": chromo_list})

                else:
                    contents = Path("./html/" + "error.html").read_text()
                    self.send_response(404)
            except ValueError:
                if "json" in params:
                    contents = {"Error": "An error ocurred. Try again with a valid specie."}
                else:
                    contents = read_html_file("error.html"). \
                        render()

        elif path == "/geneSeq":
            if len(params) == 1 or (len(params) == 2 and "json" in params):
                user_gene = params["gene"][0]
                info_dict = genes_information(user_gene)
                sequence = info_dict["seq"]
                if "json" in params:
                    contents = {"gene": user_gene,
                                "sequence": sequence}
                else:
                    contents = read_html_file(path[1:] + ".html"). \
                        render(context={"gene": user_gene,
                                        "sequence": sequence})

            else:
                contents = Path("./html/" + "error.html").read_text()
                self.send_response(404)

        elif path == "/geneInfo":
            if len(params) == 1 or (len(params) == 2 and "json" in params):
                user_gene = params["gene"][0]
                info_dict = genes_information(user_gene)
                sequence = info_dict["seq"]
                id_info = info_dict["id"]
                sequence_length = len(sequence)
                chromosome_info_1 = info_dict["desc"]
                chromosome_info_2 = chromosome_info_1.split(":")
                chromosome_name = chromosome_info_2[1]
                chromosome_start = chromosome_info_2[3]
                chromosome_end = chromosome_info_2[4]
                if "json" in params:
                    contents = {"gene": user_gene,
                                "start": chromosome_start,
                                "end": chromosome_end,
                                "id": id_info,
                                "length": sequence_length,
                                "name": chromosome_name}
                else:
                    contents = read_html_file(path[1:] + ".html"). \
                        render(context={"gene": user_gene,
                                        "start": chromosome_start,
                                        "end": chromosome_end,
                                        "id": id_info,
                                        "length": sequence_length,
                                        "name": chromosome_name})
            else:
                contents = Path("./html/" + "error.html").read_text()
                self.send_response(404)

        elif path == "/geneCalc":
            if len(params) == 1 or (len(params) == 2 and "json" in params):
                user_gene = params["gene"][0]
                info_dict = genes_information(user_gene)
                sequence = info_dict["seq"]
                length = Seq(sequence).len()
                bases = Seq(sequence).frequent_base()[1]
                percentage_bases = Seq(sequence).info()
                if "json" in params:
                    percentage_bases = percentage_bases.replace("<br><br>", ", ")
                    contents = {"gene": user_gene,
                                "length": length,
                                "most_frequent_bases": bases,
                                "bases_percentage": percentage_bases}
                else:
                    contents = read_html_file(path[1:] + ".html"). \
                        render(context={"gene": user_gene,
                                        "length": length,
                                        "bases": bases,
                                        "bases_percentage": percentage_bases})
            else:
                contents = Path("./html/" + "error.html").read_text()
                self.send_response(404)


        elif path == "/geneList":
            try:
                if len(params) == 3 or (len(params) == 4 and "json" in params):
                    chromo = params["chromo"][0]
                    start = params["start"][0]
                    end = params["end"][0]
                    mixed_info = chromo + ":" + start + "-" + end
                    chromo_dict = connect_web("phenotype/region/homo_sapiens/" + mixed_info, ";feature_type=Variation")

                    list_1 = []
                    list_2 = []
                    chromo_list = []

                    for element in range(0,len(chromo_dict)):
                        list_1.append(chromo_dict[element]["phenotype_associations"])
                        for e1 in list_1:
                            for e2 in e1:
                                if "attributes" in e2:
                                    list_2.append(e2["attributes"])
                                    for i in list_2:
                                        for u1, u2 in i.items():
                                            if u1 == "associated_gene":
                                                u2 = i[u1]
                                                chromo_list.append(u2)
                    chromo_info = ""
                    if "json" in params:
                        contents = {"chromosome": chromo,"gene_names": chromo_list}
                    else:
                        for e in chromo_list:
                            chromo_info += f"- {e}<br>"
                        contents = read_html_file(path[1:] + ".html"). \
                            render(context={"chromosome": chromo,"gene_names": chromo_info})
                else:
                    contents = Path("./html/" + "error.html").read_text()
                    self.send_response(404)
            except Exception:
                if "json" in params:
                    contents = {"Error": "An error ocurred. Try again with an integer"}
                else:
                    contents = read_html_file("error.html").\
                        render()
        else:
            contents = Path("./html/" + "error.html").read_text()
            self.send_response(404)

        self.send_response(200)  # -- Status line: OK!

        if "json" in params:
            contents = json.dumps(contents)
            self.send_header("Content-Type", "application/json")

        else:
            self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", len(contents.encode()))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(contents.encode())

        return



with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
    print("Serving at PORT...", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Stopped by the user")
        httpd.server_close()