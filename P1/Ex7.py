from Seq1 import Seq
print("-----| Practice 1, Exercise 7 |------")

s1 = Seq()
s2 = Seq("ACTGA")
s3 = Seq("Invalid sequence")

print(f"Sequence 1: (length: {s1.len()}) {s1} \n Bases: {s1.count()} \n Rev: {s1.reverse()}")
print(f"Sequence 2: (length: {s2.len()}) {s2} \n Bases: {s2.count()} \n Rev: {s2.reverse()}")
print(f"Sequence 3: (length: {s3.len()}) {s3} \n Bases: {s3.count()} \n Rev: {s3.reverse()}")