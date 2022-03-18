from Client0 import Client

ip = "127.0.0.1"
port = 8083

c = Client(ip, port)
print(c)

# -- Send a message to the server
print("Sending a message to the server...")
i = 0
while i <= 4:
    response = c.talk(f"Message {i}")
    print(f"To Server: Message {i}")
    print(f"From Server: {response}")
    i += 1