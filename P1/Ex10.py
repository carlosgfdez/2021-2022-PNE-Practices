from Seq1 import Seq
list_genes = ["U5.txt", "FRAT1.txt", "ADA.txt", "FXN.txt", "RNU6_269P.txt"]
FOLDER = "../session-04/"
for f in list_genes:
    filename = FOLDER + f
    s1 = Seq()
    s1.read_fasta(filename)
    u2 = s1.frequent_base()
    print("gen", f,":", "most frequent base -->", u2[1])