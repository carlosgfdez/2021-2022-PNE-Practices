from Seq0 import *

print("----| Practice 0, Exercise 4 |----")

FOLDER = "../Session-04/"
GENES = ["ADA", "FRAT1", "FXN", "RNU6_269P", "U5"]
BASES = ["A", "C", "T", "G"]

for gene in GENES:  # gene = "ADA"
    filename = gene + ".txt"  # filename = "ADA.txt"
    sequence = seq_read_fasta(FOLDER + filename)  # "../Session-04/ADA.txt"
    print(f"Gene {gene}:")
    for base in BASES:
        print(f"  {base}: {seq_count_base(sequence, base)}")
    print()

