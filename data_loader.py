import csv

def read_file(file_path):
    """
    Reads the content of a file and returns it as a string.

    Args:
        file_path (str): Path to the file to be read.

    Returns:
        str: Content of the file as a string.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def read_csv(file_path):
    """
    Reads a CSV file and returns the header and rows.

    Args:
        file_path (str): Path to the CSV file to be read.

    Returns:
        tuple: A tuple containing:
            - header (list of str): List of column names from the CSV file.
            - rows (list of list of str): List of rows, where each row is a list of column values.
    """
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        rows = list(reader)
    return header, rows

def chunk_data(header, rows, chunk_size):
    """
    Splits the data into chunks of a defined size.

    Args:
        header (list of str): List of column names from the CSV file.
        rows (list of list of str): List of rows, where each row is a list of column values.
        chunk_size (int): Number of rows per chunk.

    Returns:
        list of str: List of chunks, where each chunk is a string containing the header and rows.
    """
    header_str = ", ".join(header)
    chunks = []
    for i in range(0, len(rows), chunk_size):
        chunk = [header_str] + [", ".join(row) for row in rows[i:i+chunk_size]]
        chunks.append("\n".join(chunk))
    return chunks
