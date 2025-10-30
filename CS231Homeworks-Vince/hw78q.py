import sys
from typing import Generator, Tuple
from collections import Counter, defaultdict

def main():
    #check to ensure a file path is passed with the script
    if len(sys.argv) < 2:
        print("Usage: python3 script.py <file_path>")
        sys.exit(1)

    #store filename from passed argument and print processing message
    filename = sys.argv[1]
    print(f"Processing: {filename}")

    #counter to track per byte length numbers for percentage calc
    counts = Counter()
    #dictionary of sets to track unique characters
    unique_chars = defaultdict(set)

    #iterate through the generator and increment the index & add to set based on yield val
    for ch, byte_len in read_chars(filename):
        counts[byte_len] += 1
        unique_chars[byte_len].add(ch)
    #store total
    total = sum(counts.values())
    #empty file check
    if total == 0:
        print("The file contains no characters.")
        return
    #calculate percentages using counts & store in a dictionary with byte_len as keys
    percentages = {byte_len: round((counts[byte_len] / total) * 100, 2) for byte_len in range(1,5)}

    #Print formatted output
    print("Percentage breakdown & Unique counts")
    [print(f"\t{byte_len} byte chars: {percent}%, unique: {len(unique_chars[byte_len])}")
    for byte_len, percent in percentages.items()]

# generator to yield character & byte_len, reading in 8KB batches
def read_chars(file) -> Generator[Tuple[str, int], None, None]:
    with open(file, 'r', encoding='utf-8') as f:
        try:
            while True:
                batch = f.read(8192)
                if not batch:
                    break
                for ch in batch:
                    yield ch, len(ch.encode('utf-8'))
        except UnicodeDecodeError:
            print(f"Error: {file} is not UTF-8 encoded")
            sys.exit(1)

if __name__ == "__main__":
    main()