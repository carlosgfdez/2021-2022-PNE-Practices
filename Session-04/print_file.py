from pathlib import Path
file = "RNU6_269P.txt"
text = Path(file).read_text()
print(text)