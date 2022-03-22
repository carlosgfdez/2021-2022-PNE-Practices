BASES = ["A", "C", "T", "G"]
COMPLEMENTS = {"A": "T", "T": "A", "C": "G", "G": "C"}


def seq_ping():
    print("OK")


def seq_read_fasta(filename):
    from pathlib import Path

    file_contents = Path(filename).read_text()
    lines = file_contents.splitlines()
    body = lines[1:]  # list[str]
    sequence = ""
    for line in body:
        sequence += line
    return sequence


def seq_len(seq):
    return len(seq)


def seq_count_base(seq, base):
    # total = 0
    # for b in seq:
    #    if b == base:
    #        total += 1
    # return total
    return seq.count(base)


def seq_count(seq):
    result = {}
    for base in BASES:  # base = "A"
        result[base] = seq_count_base(seq, base)
    return result


def seq_reverse(seq):
    return seq[::-1]


def seq_complement(seq):  # seq = "ATTCG"
    result = ""
    for base in seq:  # base = "G"
        result += COMPLEMENTS[base]  # result = "TAAGC"
    return result


def most_frequent_base(seq):  # seq = "ATTCG"
    max_base = None  # "T"
    max_count = 0  # 2
    for base, count in seq_count(seq).items():  # {"A": 1, "C": 1, "G": 1, "T": 2}
        if count >= max_count:
            max_base = base
            max_count = count
    return max_base

