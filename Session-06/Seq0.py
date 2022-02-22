def seq_ping():
    print("Ok")

def valid_filename():
    condition = True
    while condition:
        try:
            gene = input("What gene information do you want to open? ")
            FOLDER = "../Session-04/"
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
    FOLDER = "../Session-04/"
    for e in new_dict:
        f = open(FOLDER + e + ".txt", "r")
        sequence = f.read()
        full_seq = sequence[sequence.find("\n"):].replace("\n", "")
        for element in full_seq:
            new_dict[e] += len(element)
    return new_dict

def seq_count_base():
    bases_dict = {"U5": "", "ADA": "", "FRAT1": "", "FXN": "", "RNU6_269P": ""}
    count_dict = {"U5": {}, "ADA": {}, "FRAT1": {}, "FXN": {}, "RNU6_269P": {}}
    FOLDER = "../Session-04/"
    for e in bases_dict:
        f = open(FOLDER + e + ".txt", "r")
        sequence = f.read()
        full_seq = sequence[sequence.find("\n"):].replace("\n", "")
        for element in full_seq:
            bases_dict[e] += element
    for d in bases_dict:
        for element in bases_dict[d]:
            if element in count_dict[d]:
                count_dict[d][element] += 1
            else:
                count_dict[d][element] = 1
    return count_dict

def seq_count(): #ex4 and ex5 are made in the same way, the only difference is the way you print it
    bases_dict = {"U5": "", "ADA": "", "FRAT1": "", "FXN": "", "RNU6_269P": ""}
    count_dict = {"U5": {}, "ADA": {}, "FRAT1": {}, "FXN": {}, "RNU6_269P": {}}
    FOLDER = "../Session-04/"
    for e in bases_dict:
        f = open(FOLDER + e + ".txt", "r")
        sequence = f.read()
        full_seq = sequence[sequence.find("\n"):].replace("\n", "")
        for element in full_seq:
            bases_dict[e] += element
    for d in bases_dict:
        for element in bases_dict[d]:
            if element in count_dict[d]:
                count_dict[d][element] += 1
            else:
                count_dict[d][element] = 1
    return count_dict

def seq_reverse(text):
    FOLDER = "../Session-04/"
    f = open(FOLDER + text + ".txt", "r")
    sequence = f.read()
    full_seq = sequence[sequence.find("\n"):].replace("\n", "")
    new_seq = full_seq[:20]
    reversed_seq = new_seq[::-1]
    return new_seq, reversed_seq


def seq_complement(text):
    FOLDER = "../Session-04/"
    f = open(FOLDER + text + ".txt", "r")
    complement_seq = ""
    sequence = f.read()
    full_seq = sequence[sequence.find("\n"):].replace("\n", "")
    new_seq = full_seq[:20]
    for e in new_seq:
        if e == "A":
            complement_seq += "T"
        elif e == "T":
            complement_seq += "A"
        elif e == "C":
            complement_seq += "G"
        else:
            complement_seq += "C"
    return new_seq, complement_seq

def frequent_base():
    bases_dict = {"U5": "", "ADA": "", "FRAT1": "", "FXN": "", "RNU6_269P": ""}
    count_dict = {"U5": {}, "ADA": {}, "FRAT1": {}, "FXN": {}, "RNU6_269P": {}}
    count_dict_2 = {"U5": [0, ""], "ADA": [0, ""], "FRAT1": [0, ""], "FXN": [0, ""], "RNU6_269P": [0, ""]}
    FOLDER = "../Session-04/"
    for e in bases_dict:
        f = open(FOLDER + e + ".txt", "r")
        sequence = f.read()
        full_seq = sequence[sequence.find("\n"):].replace("\n", "")
        for element in full_seq:
            bases_dict[e] += element
    for d in bases_dict:
        for element in bases_dict[d]:
            if element in count_dict[d]:
                count_dict[d][element] += 1
            else:
                count_dict[d][element] = 1
    for d in count_dict:
        for element in count_dict[d]:
            if count_dict[d][element] > count_dict_2[d][0]:
                count_dict_2[d][0] = count_dict[d][element]
                count_dict_2[d][1] = element
    return count_dict_2