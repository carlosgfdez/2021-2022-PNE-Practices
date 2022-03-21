from pathlib import Path
file = input("Enter the name of a file: ")

try:
    file_contents = Path(file).read_text()
    lines = file_contents.splitlines()
    body = lines[1:]
    print(f"Body of the filename {file} file:")
    for line in body:
        print(line)

except FileNotFoundError:
    print(f"[ERROR]: file '{file}' not found")
except IndexError:
    print(f"[ERROR]: file '{file}' is empty")
