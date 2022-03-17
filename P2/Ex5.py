from Client0 import Client

PRACTICE = 2
EXERCISE = 5
print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

ip = "127.0.0.1"
port = 9000

c = Client(ip, port)
print(c)

new_dict = Client.send_seq("self")

for e in new_dict:
    print("Sending", e,"gene to the server...")
    response = c.talk(new_dict[e])
    print(f"Response: {response}")