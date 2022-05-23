content_1 = self.path.split("?")[1]
content_2 = content_1.split("=")[1]
try:
    sequence_number = int(content_2)
    sequence = Seq()
    file_name = os.path.join("..", "Genes", f"{genes[sequence_number]}.txt")
    sequence.read_fasta(file_name)
    contents = f"""
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="utf-8">
                <title>GET</title>
            </head>
            <body>
                <h1>Sequence number {sequence_number}:</h1>
                <p>{sequence}</p>
                <a href="/">Main page</a>
            </body>
        </html>"""
    self.send_response(200)
except (IndexError, ValueError):
    contents = Path(f"Error.html").read_text()
    self.send_response(404)