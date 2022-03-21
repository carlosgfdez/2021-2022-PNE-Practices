from pathlib import Path
file = input("Enter the name of a file: ")

try:
    file_contents = Path(file).read_text()
    lines = file_contents.splitlines()
    header = lines[0]
    print(f"The first line of the {file} file is:\n{header}")

except FileNotFoundError:
    print(f"[ERROR]: file '{file}' not found")
except IndexError:
    print(f"[ERROR]: file '{file}' is empty")