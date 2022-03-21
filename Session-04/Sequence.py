from pathlib import Path
file = input("Enter the name of a file: ")

try:
    file_contents = Path(file).read_text().replace("\n", "")
    content_length = len(file_contents)
    print(f"The total number of bases in the {file} file is: {content_length}")

except FileNotFoundError:
    print(f"[ERROR]: file '{file}' not found")
except IndexError:
    print(f"[ERROR]: file '{file}' is empty")