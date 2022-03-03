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
