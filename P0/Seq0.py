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


def seq_len():
    new_dict = {"U5": 0, "ADA": 0, "FRAT1": 0, "FXN": 0, "RNU6_269P": 0}
    FOLDER = "/Users/carlosgfdez/PycharmProjects/2021-2022-PNE-Practices/Session-04/"
    for e in new_dict:
        f = open(FOLDER + e + ".txt", "r")
        sequence = f.read()
        full_seq = sequence[sequence.find("\n"):].replace("\n", "")
        for element in full_seq:
            new_dict[e] += len(element)
    return new_dict
