from Seq1 import Seq
print("-----| Practice 1, Exercise 8 |------")

seqs_list = [Seq(), Seq("ACTGA"), Seq("Invalid sequence")]
for index, seq in enumerate(seqs_list):
    print(f"Sequence {index}: (Length: {seq.len()}) {seq}")
    print(f"\tBases: {seq.count()}")
    print(f"\tRev: {seq.reverse()}")
    print(f"\tComp: {seq.complement()}")

