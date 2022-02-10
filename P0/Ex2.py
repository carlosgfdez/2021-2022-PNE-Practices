import Seq0
gene = Seq0.valid_filename()
sequence = Seq0.seq_read_fasta(gene)
print(sequence[0:20])