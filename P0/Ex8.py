import Seq0
print("----| Exercise 8 |----")
count_dict_2 = Seq0.frequent_base()
for d in count_dict_2:
    print("Gene", d, "most frequent base:", count_dict_2[d][1])
