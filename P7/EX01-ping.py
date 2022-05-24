import http.client
from http import HTTPStatus
import json
import termcolor

SERVER = 'rest.ensembl.org'
ENDPOINT = '/info/ping'
RESOURCE = '?content-type=application/json'
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

