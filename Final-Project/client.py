# -- Example of a client that uses the HTTP.client library
# -- for requesting the main page from the server
import http.client

PORT = 8080
SERVER = 'localhost'

print(f"\nConnecting to server: {SERVER}:{PORT}")
conn = http.client.HTTPConnection(SERVER, PORT)

# -- Send the request message, using the GET method. We are
# -- requesting the main page (/)


def connect_server(ENDPOINT, PARAMETER):
    try:
        conn.request("GET", ENDPOINT + PARAMETER)
    except ConnectionRefusedError:
        print("ERROR! Cannot connect to the Server")
        exit()
    r1 = conn.getresponse()

    print(f"Response received!: {r1.status} {r1.reason}\n")

    data1 = r1.read().decode("utf-8")
    return data1


data_species = connect_server("/listSpecies", "?limit=10&json=1")
print(data_species)

data_karyotype = connect_server("/karyotype", "?specie=mouse&json=1")
print(data_karyotype)

data_chromosome_length = connect_server("/chromosomeLength", "?specie=mouse&chromo=9&json=1")
print(data_chromosome_length)

data_gene_sequence = connect_server("/geneSeq", "?gene=FRAT1&json=1")
print(data_gene_sequence)

data_gene_information = connect_server("/geneInfo", "?gene=FRAT1&json=1")
print(data_gene_information)

data_gene_calculation = connect_server("/geneCalc", "?gene=FRAT1&json=1")
print(data_gene_calculation)

data_gene_list = connect_server("/geneList", "?chromo=18&start=22125500&end=22136000&json=1")
print(data_gene_list)