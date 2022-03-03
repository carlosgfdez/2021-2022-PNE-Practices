from Seq1 import Seq
print("-----| Practice 1, Exercise 5 |------")

s1 = Seq()
s2 = Seq("ACTGA")
s3 = Seq("Invalid sequence")

print(f"Sequence 1: (length: {s1.len()}) {s1} \n (A: {s1.seq_count_base()[0]}, T: {s1.seq_count_base()[1]}, C: {s1.seq_count_base()[2]}, G: {s1.seq_count_base()[3]})")
print(f"Sequence 2: (length: {s2.len()}) {s2} \n (A: {s2.seq_count_base()[0]}, T: {s2.seq_count_base()[1]}, C: {s2.seq_count_base()[2]}, G: {s2.seq_count_base()[3]})")
print(f"Sequence 3: (length: {s3.len()}) {s3} \n (A: {s3.seq_count_base()[0]}, T: {s3.seq_count_base()[1]}, C: {s3.seq_count_base()[2]}, G: {s3.seq_count_base()[3]})")