import socket

ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

PORT = 8080
IP = "127.0.0.1"

# -- Step 1: create the socket
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# -- Optional: This is for avoiding the problem of Port already in use
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# -- Step 2: Bind the socket to html's IP and PORT
ls.bind((IP, PORT))

ls.listen()

print("The html is configured!")

while True:
    print("Waiting for Clients to connect")

    try:
        (cs, client_ip_port) = ls.accept()
    # -- Server stopped manually
    except KeyboardInterrupt:
        print("Server stopped by the user")
        # -- Close the listenning socket
        ls.close()

        # -- Exit!
        exit()

    # -- Execute this part if there are no errors
    else:
        print("A client has connected to the html!")
        msg_raw = cs.recv(2048)
        msg = msg_raw.decode().replace("\n", "").strip()
        splitted_cmd = msg.split(" ")
        cmd = splitted_cmd[0]   #cmd = msg.split(' ')[0]
        if cmd != "PING":
            arg = splitted_cmd[1]   #arg = msg.split(' ')[1]
        print(cmd)
        print(f"Message received: {msg}")
        #print(msg == "PING")
        #print(len(msg))
        if cmd == "PING":
            response = "OK!\n"
        else:
            response = "HELLO. I am the Happy Server :-)\n"
        cs.send(response.encode())
        cs.close()