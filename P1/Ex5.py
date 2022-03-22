from Seq1 import Seq
print("-----| Practice 1, Exercise 5 |------")

seqs_list = [Seq(), Seq("ACTGA"), Seq("Invalid sequence")]
for index, seq in enumerate(seqs_list):
    print(f"Sequence {index}: (Length: {seq.len()}) {seq}")
    for base in Seq.BASES_ALLOWED:
        print(f"{base}: {seq.count_base(base)}", end=" ")
    print()