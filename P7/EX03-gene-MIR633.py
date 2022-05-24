import http.client
from http import HTTPStatus
import json
import termcolor

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

SERVER = 'rest.ensembl.org'
ENDPOINT = '/sequence/id'
RESOURCE = f'/{GENES["MIR633"]}?content-type=application/json'
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

    raw_data = response.read().decode("utf-8")
    ping = json.loads(raw_data)['ping']
    if ping == 1:
        print("PING OK! The database is running!")

