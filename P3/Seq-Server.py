import socket
import termcolor
import os #Operative System
from Sequence import Seq

IP = "127.0.0.1" # "127.0.0.1"  o "localhost"
# para la máquina en la que se ejecuta, si se intenta desde otra hace falta poner el de dicha maquina (192....)
PORT = 8080
GENES = ["ADA", "FRAT1", "FXN", "RNU6_29P", "U5"]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    server_socket.bind((IP, PORT))
    server_socket.listen()

    print("SEQ Server configured!")

    while True:
        print(f"Waiting for Clients...")
        (client_socket, client_address) = server_socket.accept()
        request_bytes = client_socket.recv(2048)
        request = request_bytes.decode("utf-8")
        slices = request.split(" ")
        command = slices[0]
        termcolor.cprint(f"{command}", 'green')
        if command == "PING":
            response = f"OK!\n"

        elif command == "GET":
            genes_number = int(slices[1])
            gene = GENES[genes_number]
            seq = Seq()
            file_name = os.path.join("..", "Genes", f"{gene}.txt")
            seq.read_fasta(file_name)

            response = f"{seq}\n"

        elif command == "INFO":
            bases = slices [1]
            seq = Seq(bases)

            response = f"{seq.count()}"

        elif command == "COMP":
            bases = slices[1]
            seq = Seq(bases)

            response = f"{seq.complement()}\n"

        elif command == "REV":
            bases = slices[1]
            seq = Seq(bases)

            response = f"{seq.reverse()}\n"

        elif command == "GENE":
            gene = slices[1]
            seq = Seq()
            file_name = os.path.join("..", "Genes", f"{gene}.txt")
            seq.read_fasta(file_name)

            response = f"{seq}\n"

        print(response)
        response_bytes = str.encode(response)
        client_socket.send(response_bytes)


        client_socket.close()

except socket.error:
    print(f"Problems using port {PORT}. Do you have permission?")
except KeyboardInterrupt:
    print("Server stopped by the admin")
    server_socket.close()
