import socket

# SERVER IP, PORT
PORT = 21000
IP = "localhost"

while True:
    # -- Ask the user for the message
    message = input("Enter a message: ")
    # -- Create the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # -- Establish the connection to the Server
    s.connect((IP, PORT))
    # -- Send the user message
    s.send(str.encode(message))
    # -- Close the socket
    s.close()