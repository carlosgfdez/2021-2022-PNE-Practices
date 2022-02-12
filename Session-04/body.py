from pathlib import Path
file = "U5.txt"
text = Path(file).read_text()
print("Body of the U5.txt file:")
print(text[text.find("\n"):])
