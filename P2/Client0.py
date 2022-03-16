class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def __str__(self):
        return "Connection to SERVER at "  +  str(self.ip) + " PORT:" + str(self.port)

    def ping(self):
        print("OK")
