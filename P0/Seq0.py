def seq_ping():
    print("Ok")



def valid_filename():
    condition = True
    while condition:
        try:
            gene = input("What gene information do you want to open? ")
            FOLDER = "/Users/carlosgfdez/PycharmProjects/2021-2022-PNE-Practices/Session-04/"
            f = open(FOLDER + gene + ".txt", "r")
            condition = False
            return f.read()
        except FileNotFoundError:
            print("That file couldn't be found")


def seq_read_fasta(gene):
    new_seq = gene[gene.find("\n"):].replace("\n", "")
    return new_seq