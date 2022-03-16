from Client0 import Client

PRACTICE = 2
EXERCISE = 2

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "127.0.0.1"
PORT = 9000

c = Client(IP, PORT)
c.ping()

print(c)
