#!/usr/bin/env python3
"""
This program is a command line tool and
takes a file as a commandline argument,
reads a UTF-8 text file and prints the
percentage of characters that use 1-4 bytes,
and counts and categorizes the amount of
UTF-8 characters with 1-4 bytes
"""

import sys

def analyze_file(path: str):
    """
    This counts and categorizes unique characters
    # by 1-4 bytes encoded in UTF-8.
    """

    # Initialized counter and uniques
    counts = {1: 0, 2: 0, 3: 0, 4: 0}
    uniques = {1: set(), 2: set(), 3: set(), 4: set()}

    # Opens file to read as UTF-8 text
    with open(path, "r", encoding="utf-8") as file:
        text = file.read()

    # Number of characters in text
    total = len(text)

    for char in text:
        # Encode each character back to UTF-8 bytes
        b = char.encode("utf-8")
        n = len(b)  # 1–4 bytes
        counts[n] += 1
        uniques[n].add(char)

    # Prints name of file and number of characters
    print(f"File: {path}")
    print(f"Total characters: {total}\n")

    # Calculates percentage
    for n in range(1, 5):
        if total:
            pct = 100 * counts[n] / total
        else:
            pct = 0
        print(f"{n}-byte chars: {counts[n]:6d}  "
              f"{pct:6.2f}%  Unique: {len(uniques[n])}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("You probably forgot to include the filename: python3 charByte_eg4.py <filename>")
        sys.exit(1)
    analyze_file(sys.argv[1])