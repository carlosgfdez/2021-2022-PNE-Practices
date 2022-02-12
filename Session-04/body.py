f = open("U5.txt", "r")
file = f.read()
print("Body of the U5.txt file:")
print(file[file.find("\n"):])