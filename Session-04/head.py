f = open("RNU6_269P.txt", "r")
file = f.read()
print(file[:file.find("\n")])