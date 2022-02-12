from pathlib import Path
file = "ADA.txt"
text = Path(file).read_text()

full_seq = text[text.find("\n"):].replace("\n", "")
print("The total number of bases in ADA.txt is", len(full_seq))