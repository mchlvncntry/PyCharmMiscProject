import sys
from collections import Counter, defaultdict

def analyze_characters(filename):
    #try to open and read file
    try:
        #open the file using UTF-8 encoding
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        #handle file not found
        print(f"Error: File '{filename}' not found.")
        return
    except UnicodeDecodeError:
        #handle files that aren't UTF-8
        print(f"Error: File '{filename}' is not UTF-8.")
        return

    #handle empty file
    if not text:
        print("File is empty.")
        return

    #create counter to store the different types of byte characters
    byte_lengths = Counter(len(ch.encode("utf-8")) for ch in text)

    #counts unique characters per byte length, ignoring duplicates
    unique_chars = defaultdict(set)
    for ch in set(text):
        unique_chars[len(ch.encode("utf-8"))].add(ch)

    #totals for percentage
    total = sum(byte_lengths.values())

    for n in range(1, 5):
        count = byte_lengths.get(n, 0)
        percent = (count / total * 100) if total else 0
        uniq = len(unique_chars[n])
        print(f"{n}-byte characters: {percent:6.2f}% ({count} total, {uniq} unique)")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <filename>")
    else:
        analyze_characters(sys.argv[1])
