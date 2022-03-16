class Client:
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT

    def __str__(self):
        return f"Connection to server at ({self.IP}:{self.PORT})"

    def ping(self):
        print("OK")
