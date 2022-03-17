from Client0 import Client

PRACTICE = 2
EXERCISE = 6
print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

ip = "127.0.0.1"
port = 9000

c = Client(ip, port)
print(c)

print("Sending FRAT1 gene to the server...")

sequence = Client.seq_frag("self")
i = 0
while i < 50:
    response = c.talk(sequence[i:10 + i])
    i += 10
    print(f"Response: {response}")