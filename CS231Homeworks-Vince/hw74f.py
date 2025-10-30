import sys


def check(file):
    # Determine whether the file passed is encoded as UTF-8
    with open(file) as handle:
        try:
            handle.read()
            return True
        except UnicodeDecodeError:
            return False


def num_utf8_bytes(char):
    return len(char.encode('utf-8'))


def file_analysis(filename):
    with open(filename, encoding='utf-8') as f:
        text = f.read()

    # first keep all non whitespace characters
    # by filtering the chars in the large string 'text'
    non_whitespace_chars = [c for c in text if not c.isspace()]
    num_chars = len(non_whitespace_chars)

    # use set function to remove duplicate chars
    unique_chars = set(non_whitespace_chars)

    # create dictionaries to store counts of each size class
    byte_counts = {1: 0, 2: 0, 3: 0, 4: 0}
    unique_byte_counts = {1: 0, 2: 0, 3: 0, 4: 0}

    # iterate through all chars to update byte counts to find percentage
    for c in non_whitespace_chars:
        num_bytes = num_utf8_bytes(c)
        if num_bytes in byte_counts:
            byte_counts[num_bytes] += 1

    # iterate through all chars to update unique byte counts to find counts
    for c in unique_chars:
        num_bytes = num_utf8_bytes(c)
        if num_bytes in unique_byte_counts:
            unique_byte_counts[num_bytes] += 1

    print(f"Total non-whitespace characters: {num_chars}")
    print("Percentages and uniqueness counts by byte length: ")
    for byte_len in range(1, 5):
        percentage = (byte_counts[byte_len] / num_chars * 100) if num_chars > 0 else 0
        print(f"{byte_len} byte(s):")
        print(f"   Percentage of all non whitespace chars: {percentage:.2f}%")
        print(f"   Number of unique byte counts: {unique_byte_counts[byte_len]}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No filename argument entered.")
        sys.exit(1)

    filename = sys.argv[1]

    if not check(filename):
        print(f"File is not valid UTF-8")
        sys.exit(1)

    print("File was successfully opened")
    file_analysis(filename)