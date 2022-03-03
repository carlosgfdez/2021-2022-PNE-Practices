class Seq:
    """A class for representing sequences"""
    def __init__(self, strbases="NULL"):
        self.strbases = strbases
        if strbases == "NULL":
            print("NULL sequence created")
            self.strbases = "NULL"
        elif not self.valid_sequence():
            print("INVALID Seq!")
            self.strbases = "ERROR"
        else:
            print("New sequence created!")
            self.strbases = strbases

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

    def seq_count_base(self):
        count_A = 0
        count_T = 0
        count_C = 0
        count_G = 0
        if self.strbases == "NULL" or self.strbases == "ERROR":
            pass
        else:
            for e in self.strbases:
                if e == "A":
                    count_A += 1
                elif e == "T":
                    count_T += 1
                elif e == "C":
                    count_C += 1
                else:
                    count_G += 1
        return count_A, count_T, count_C, count_G

    def count(self):
        bases_dict = {"A": 0, "T": 0, "C": 0, "G": 0}
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return bases_dict
        else:
            for e in self.strbases:
                bases_dict[e] += 1
            return bases_dict
