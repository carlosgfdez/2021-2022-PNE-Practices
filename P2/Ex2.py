from Client0 import Client

PRACTICE = 2
EXERCISE = 2

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

ip = "127.0.0.1"
port = 9000

c = Client(ip, port)

print(c)
