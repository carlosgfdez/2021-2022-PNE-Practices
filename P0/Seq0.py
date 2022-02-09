def seq_ping():
    print("Ok")



def valid_filename():
    condition = True
    while condition:
        try:
            gene = input("What file do you want to open? ")
            FOLDER = "./Sequences/"
            f = open(FOLDER + gene + ".txt", "r")
            condition = False
            return f.read()
        except FileNotFoundError:
            print("That file couldn't be found")


def seq_read_fasta(gene):
    text = open(gene, "r").read()
    seq = seq[seq.find("\n"):].replace("\n", "")
    return full_seq