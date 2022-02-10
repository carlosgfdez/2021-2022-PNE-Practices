import Seq0
count_dict = Seq0.seq_count_base()
print("----| Exercise 4 |----")
for d in count_dict:
    print("Gene", d, ":")
    for e in count_dict[d]:
        print(e, ":", count_dict[d][e])
    print("\n")
