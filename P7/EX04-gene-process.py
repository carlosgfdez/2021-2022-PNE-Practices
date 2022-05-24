from Seq1 import Seq
import http.client
from http import HTTPStatus
import json
import termcolor

gene_1 = input("Write the gene name: ")

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

if gene_1 in GENES:
    SERVER = 'rest.ensembl.org'
    ENDPOINT = '/sequence/id'
    RESOURCE = f'/{GENES[gene_1]}?content-type=application/json'
    URL = SERVER + ENDPOINT + RESOURCE
    CONTENT = ENDPOINT + RESOURCE
    PORT = 80

    conn = http.client.HTTPConnection(SERVER)

    print(f"Server: {SERVER}")
    print(f"URL: {URL}")

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

    print(f"Gene: {gene_1}")
    print(f"Description: {data['desc']}")
    sequence = Seq(data['seq'])
    print(sequence.info())
    print(sequence.frequent_base())

else:
    print("Choose a correct gene")


