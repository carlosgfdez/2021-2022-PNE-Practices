import socket

class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def __str__(self):
        return "Connection to SERVER at "  +  str(self.ip) + " PORT:" + str(self.port)

    def ping(self):
        print("OK")

    def talk(self, msg):
        # -- Create the socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # establish the connection to the Server (IP, PORT)
        s.connect((self.ip, self.port))
        # Send data.
        s.send(str.encode(msg))
        # Receive data
        response = s.recv(2048).decode("utf-8")
        # Close the socket
        s.close()
        # Return the response
        return response

    def send_seq(self):
        new_dict = {"U5": "", "FRAT1": "", "ADA": ""}
        FOLDER = "../Session-04/"
        for e in new_dict:
            f = open(FOLDER + e + ".txt", "r")
            sequence = f.read()
            full_seq = sequence[sequence.find("\n"):].replace("\n", "")
            for element in full_seq:
                new_dict[e] += element
        return new_dict

    def seq_frag(self):
        seq_info = ""
        FOLDER = "../Session-04/"
        f = open(FOLDER + "FRAT1.txt", "r")
        sequence = f.read()
        full_seq = sequence[sequence.find("\n"):].replace("\n", "")
        for element in full_seq:
            seq_info += element
        return seq_info
