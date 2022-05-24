class Seq:
    """A class for representing sequences"""

    def __init__(self, strbases = "NULL"):   # Initialize the sequence with the value
                                            # passed as argument when creating the object
        self.strbases = strbases #aqui se crea la condicion de las bases
        if strbases == "NULL":
            print("NULL sequence created")
            self.strbases = "NULL"
        elif not self.valid_sequence():
            self.strbases = "ERROR"
            print("INVALID seq!")
        else:
            self.strbases = strbases
            print("New sequence created!")

    @staticmethod  # the function is expecting a normal argument
    def valid_sequence2(sequence):
        valid = True
        i = 0
        while i < len(sequence):
            c = sequence[i]
            if c != "A" and c != "C" and c != "G" and c != "T":
                valid = False
            i += 1
        return valid

    def valid_sequence(self):
        valid = True
        i = 0
        while i < len(self.strbases):
            c = self.strbases[i]
            if c != "A" and c != "C" and c != "G" and c != "T":
                valid = False
            i += 1
        return valid

    def __str__(self):
        """Method called when the object is being printed"""
        # -- We just return the string with the sequence
        return self.strbases

    def len(self):
        """Calculate the length of the sequence"""
        new_len = ""
        if self.strbases == "NULL" or self.strbases == "ERROR":
            new_len = 0
            return new_len
        else:
            return len(self.strbases)

    def count_base(self):
        count_A = 0
        count_C = 0
        count_G = 0
        count_T = 0
        for i in self.strbases:
            if i == "A":
                count_A += 1
            elif i == "C":
                count_C += 1
            elif i == "G":
                count_G += 1
            elif i == "T":
                count_T += 1
        return count_A, count_C, count_G, count_T

    def count(self):
        d = {"A": 0, "C": 0, "G": 0, "T": 0}
        for c in self.strbases:
            if c in d:
                d[c] += 1
        return d

    def reverse(self):
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return self.strbases
        else:
            reverse = self.strbases[::-1]  # [::-1] empieza por el final del string y va hasta la posicion -1 sin incluirlo
        return reverse

    def complement(self):
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return self.strbases
        else:
            complement = {"A": "T", "C": "G", "G": "C", "T": "A"}
        return "".join([complement[base] for base in self.strbases])  # sustituimos una base por otra (el value por el key)

    def read_fasta(self, filename):
        from pathlib import Path

        file_contents = Path(filename).read_text()
        lines = file_contents.splitlines()
        body = lines[1:]
        self.strbases = ""
        for lines in body:
            self.strbases += lines

    def most_base(self):
        bases = ["A", "C", "G", "T"]
        count_A, count_C, count_G, count_T = self.count_base()
        counts = [count_A, count_C, count_G, count_T]
        zipped = zip(counts, bases)
        u2 = max(zipped)
        return u2[1]

    def info(self): #hacerporcentajes
        print("Total lenght: ", len(self.strbases))
        d = {"A": 0, "C": 0, "G": 0, "T": 0}
        for b in self.strbases:
            d[b] += 1
        total = sum(d.values())
        for k, v in d.items():
            d[k] = [v, (v * 100) / total]
        final_dict = d
        message = ""
        for k, v in final_dict.items():
            message += k + ": " + str(v[0]) + " (" + str(round(v[1], 1)) + "%)" + "\n"
        return message