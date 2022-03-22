from Seq0 import *

print("----| Practice 0, Exercise 6 |----")

FOLDER = "../Session-04/"
GENES = ["ADA", "FRAT1", "FXN", "RNU6_269P", "U5"]

for gene in GENES:  # gene = "ADA"
    filename = gene + ".txt"  # filename = "ADA.txt"
    sequence = seq_read_fasta(FOLDER + filename)  # "../Session-04/ADA.txt"
    print(f"Gene {gene}:")
    print(f"Frag: {sequence[:20]}")
    print(f"Rev:  {seq_reverse(sequence[:20])}\n")