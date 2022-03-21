from pathlib import Path

file = input("Enter the name of a file: ")
try:
    file_contents = Path(file).read_text()
    print(file_contents)

except FileNotFoundError:
    print(f"[ERROR]: file '{file}' not found")
except IndexError:
    print(f"[ERROR]: file '{file}' is empty")
