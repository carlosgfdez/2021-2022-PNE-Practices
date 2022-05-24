import http.server
import socketserver
import termcolor
from pathlib import Path
import jinja2 as j
import http.client
from urllib.parse import parse_qs, urlparse
import json
import seq1

HTML_FOLDER = "./html/"
SERVER = 'rest.ensembl.org'
genes_dict = {"SRCAP": "ENSG00000080603",
              "FRAT1": "ENSG00000165879",
              "ADA": "ENSG00000196839",
              "FXN": "ENSG00000165060",
              "RNU6_269P": "ENSG00000212379",
              "MIR633": "ENSG00000207552",
              "TTTY4C": "ENSG00000228296",
              "RBMY2YP": "ENSG00000227633",
              "FGFR3": "ENSG00000068078",
              "KDR": "ENSG00000128052",
              "ANK2": "ENSG00000145362"}

names = genes_dict.keys()
names_list = []
for n in names:
    names_list.append(n)


def read_html_file(filename):
    contents = Path(HTML_FOLDER + filename).read_text()
    contents = j.Template(contents)
    return contents


def make_ensembl_request(url, params):
    conn = http.client.HTTPConnection(SERVER)
    parameters = '?content-type=application/json'
    try:
       conn.request("GET", url + parameters + params)

    except ConnectionRefusedError:
        print("ERROR! Cannot connect to the Server")
        exit()

    r1 = conn.getresponse()

    print(f"Response received!: {r1.status} {r1.reason} \n")
    data1 = r1.read().decode('utf-8')  #this is the dictionary

    data2 = json.loads(data1)
    return data2

def count_bases(seq):
    d = {"A": 0, "C": 0, "G": 0, "T": 0}
    for b in seq:
        d[b] += 1

    total = sum(d.values())
    for k,v in d.items():
        d[k] = [v, round((v * 100) / total,1)]
    return d


def convert_message(base_count):
    message = ""
    for k,v in base_count.items():
        message += k + ": " + str(v[0]) + " (" + str(v[1]) + "%)" + "\n"
    return message


def info_operation(arg):
    base_count = count_bases(arg)
    response = "<p> Sequence: " + arg + "</p>"
    response += "<p> Total length: " + str(len(arg)) + "</p>"
    response += convert_message(base_count)
    return response

# Define the Server's port
PORT = 8080

# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True


# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inheritates all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""
        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        url_path = urlparse(self.path)
        path = url_path.path #this is the url
        arguments = parse_qs(url_path.query)  #esto es lo que conviertes en diccionario
        print("The old path was", self.path)
        print("The new path is", url_path.path)
        print("arguments", arguments)
        # Message to send back to the client
        if self.path == "/": # son los endpoints
            contents = read_html_file("index.html") \
                .render(context={"n_names": names_list}) #poner aqui las que sean de desglosar una lista SIEMPRE

        elif path == "/listSpecies": #dos tipos de errores
            dict_answer = make_ensembl_request("/info/species", "")
            limit = int(arguments["limit"][0])  # el 0 indica un valor para una llave. es lo que te va a pedir el servidor
            species = dict_answer["species"] #queremos las especies en general
            length = len(species)
            species_2 = [] #creamos una lista a la que vamos añadiendo las especies
            for i in range(0, limit):
                species_2.append(species[i]['common_name'])
            contents = read_html_file(path[1:] + ".html")\
                .render(context = {
                "species": species_2,
                "number": length,
                "limit": limit
            })
        elif path == "/karyotype": #1 tipo de error
            speciess = arguments["speciess"][0] #speciess lo ponemos aqui y en el html y es lo que aparecerá en el web, es porque queremos una en concreto
            dict_answer = make_ensembl_request("/info/assembly/" + speciess, "") #speciess es el diccionario concreto, una key una concreta
            karyotype = dict_answer["karyotype"]
            contents = read_html_file(path[1:] + ".html") \
                .render(context={
                "karyotype": karyotype
            })
        elif path == "/chromosomeLenght": #dos tipos de errores
            specie_3 = str(arguments['specie_3'][0].strip()) #quitamos espacios para que lo lea, solo lee el espacio sino
            dict_answer = make_ensembl_request("/info/assembly/" + specie_3, "")
            chromo = int(arguments['chromosome'][0].strip())
            list = dict_answer["top_level_region"]
            line = []
            for i in range(0, len(list)):
                line.append(list[i]["name"]) #los agrupamos por especie (como en el 1)

            position = line.index(str(chromo))
            wanted_line = list[position]

            length = int(wanted_line["length"])
            print(arguments)

            contents = read_html_file(path[1:] + ".html") \
                .render(context={
                "chromo": length})

        elif path == "/geneSeq":
            seq = arguments['seq'][0]
            key = genes_dict[seq]
            dict_answer = make_ensembl_request("/sequence/id/" + str(key), "")
            info = dict_answer["seq"]
            contents = read_html_file(path[1:] + ".html") \
                .render(context={
                "sequence": info,
                "names": names
            })

        elif path == "/geneInfo":
            info = arguments["info"][0]
            key = genes_dict[info]
            dict_answer = make_ensembl_request("/sequence/id/" + str(key), "")
            gene_info = dict_answer["desc"] #usamos la descripcion para sacar la información del gen
            seq_gene = dict_answer["seq"]
            s = seq1.Seq(seq_gene)
            info_split = gene_info.split(":") #quitamos los dos puntos para así tener la distinta info y usarla
            start_gene = int(info_split[3])
            end_gene = int(info_split[4])
            chromosome = info_split[1]
            le = s.len()
            contents = read_html_file(path[1:] + ".html")\
                .render(context={
                "start": start_gene,
                "end": end_gene,
                "id": key,
                "le": le, #mirar que pasa con la lenght
                "chromosome": chromosome,
            })

        elif path == "/geneCalc":
            gene_calc = arguments["calc"][0]
            key2 = genes_dict[gene_calc]
            dict_answer = make_ensembl_request("/sequence/id/" + key2, "")
            seq_1 = dict_answer["seq"] #necesitamos la secuencia para no tener una nullsequence
            seq = seq1.Seq(seq_1) #usamos la seq de la practica 1
            percentage_bases = seq.info() #aqui tenemos la funcion hecha hace mazo de los percentages
            total_lenght = seq.len()
            contents = read_html_file(path[1:] + ".html")\
                .render(context={
                "percentages": percentage_bases,
                "t_lenght": total_lenght
            })

        elif path == "/geneList": #INTENTAR ENTENDERLO
            chromo = arguments["chromo"][0]
            start = arguments["start"][0]
            end = arguments["end"][0]
            everything = chromo + ":" + start + "-" + end
            dict_answer = ("/phenotype/region/homo_sapiens/" + everything, ";feature=gene;feature=transcript;feature=cds;feature=exon")
            print(dict_answer)
            contents = read_html_file(path[1:] + ".html")\
                .render(context={
                "gene": chromo
            })

        else:
            contents = "im the happy server"




        # Generating the response message
        self.send_response(200)  # -- Status line: OK!

        # Define the content-type header:
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(contents.encode()))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(contents.encode())

        return


# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler
Handler = TestHandler

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stoped by the user")
        httpd.server_close()