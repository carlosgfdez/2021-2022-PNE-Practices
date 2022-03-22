from Seq0 import *
print("----| Practice 0, Exercise 2 |----")
FOLDER = "../Session-04/"

filename = input("File's name: ")

print(f"DNA file: {filename}")
sequence = seq_read_fasta(FOLDER + filename)
print("The first 20 bases are:")
print(sequence[:20])

