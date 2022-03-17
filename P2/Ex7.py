from Client0 import Client

PRACTICE = 2
EXERCISE = 7
print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

ip = "127.0.0.1"
port = 9000
port2 = 9002

c = Client(ip, port)
c2 = Client(ip, port2)
print(c)
print(c2)

print("Null Seq created")
print("Sending FRAT1 gene to the server...")

sequence = Client.seq_frag("self")
i = 0
d = 1
while i < 100:
    if d % 2 == 0:
        response = c2.talk(f"Fragment {d}: {sequence[i:10 + i]}")
    else:
        response = c.talk(f"Fragment {d}: {sequence[i:10 + i]}")
    i += 10
    d += 1

    print(f"Response: {response}")