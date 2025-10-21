#!/usr/bin/env python3

"""
Character Encodings Assignment 10/20-10/26
Write a program that expects a filename as argument, and indicates the percentages
of characters in it spanning one, two, three, and four bytes, along with the number
of unique characters occurring in each of those classes.

** I decided to also print the unique chars per byte class. **
"""

from collections import Counter
import sys

BYTE_CLASSES = (1, 2, 3, 4)
CHARS_PER_LINE = 5  # makes the output more readable by preventing very long horizontal lines of chars
MAX_CHARS_TO_DISPLAY = 100  # prevents huge, unreadable character dumps in the command line shell

def usage_and_exit():
    print("\nNo file arg entered.\nPlease run:\npython3 <py file during peer review> <file arg here>\n")
    sys.exit(1)

def read_text(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: file \'{file_path}\' not found.\n")
        sys.exit(2)
    except PermissionError:
        print(f"Error: permission denied to file \'{file_path}\'\n")
        sys.exit(3)
    except UnicodeDecodeError as e:
        print(f"Error: could not decode file \'{file_path}\' as UTF-8.\n{e}\n")
        sys.exit(4)

def classify_pairs(text):
    """Return a tuple of (byte_length, character) for each character (immutable)."""
    return tuple(map(lambda ch: (len(ch.encode("utf-8")), ch), text))

def counts_from_pairs(pairs):
    """Functional count per byte-length."""
    return Counter(map(lambda p: p[0], pairs))

def uniques_from_pairs(pairs):
    """
    Returns dictionary mapping byte_length -> frozenset of unique characters.
    Makes 4 passes over pairs (one per byte class in BYTE_CLASSES).
    Time: O(n) where n=len(pairs). Space: O(n).
    No in-place mutation; returns immutable frozensets.
    """
    return {
        n: frozenset(charac for byte_len, charac in pairs if byte_len == n)
        for n in BYTE_CLASSES
    }


def _format_one_class_block(args):
    """Return formatted block for one byte-length class with wrapped character lines."""
    byte_len, count, total, uniq = args
    percent = (count / total * 100) if total > 0 else 0.0
    header = f"{byte_len}-byte characters: {percent:6.2f}% ({count:,} out of {total:,})"
    uniq_line = f"  Count of unique {byte_len}-byte characters: {len(uniq)}"

    characs_block = ""
    if 0 < len(uniq) <= MAX_CHARS_TO_DISPLAY:
        sorted_characs = sorted(uniq)
        groups = [
            ", ".join(repr(c) for c in sorted_characs[i:i + CHARS_PER_LINE])
            for i in range(0, len(sorted_characs), CHARS_PER_LINE)
        ]
        # Align all lines at the same indentation level
        label = "  Unique Characters: "
        indent = " " * len(label)
        wrapped = ("\n" + indent).join(groups)
        characs_block = f"{label}{wrapped}"

    parts = [header, uniq_line]
    if characs_block:
        parts.append(characs_block)
    return "\n".join(parts) + "\n\n"

def render_report(filename, total_characs, counts, uniques):
    """Format and return complete analysis report showing character distribution by byte length."""
    header = f"\n\nTotal count of characters in '{filename}': {total_characs:,}\n\n"

    class_args_iterable = map(
        lambda n: (n, counts.get(n, 0), total_characs, uniques.get(n, frozenset())),
        BYTE_CLASSES
    )
    class_blocks = "".join(map(_format_one_class_block, class_args_iterable))

    total_unique = sum(len(uniques.get(n, frozenset())) for n in BYTE_CLASSES)
    footer = "-" * 45 + f"\nTotal count of unique characters: {total_unique}\n\n"
    return header + class_blocks + footer

def analyze(filename):
    """Analyze text file and return formatted report of character byte-length distribution."""
    text = read_text(filename)
    if text == "":
        return f"Analysis of '{filename}':\n\nFile is empty."
    pairs = classify_pairs(text)
    counts = counts_from_pairs(pairs)
    uniques = uniques_from_pairs(pairs)
    total_characs = sum(counts.values())
    return render_report(filename, total_characs, counts, uniques)

def main():
    if len(sys.argv) != 2: # self-explanatory, no need to comment here
        usage_and_exit()
    print(analyze(sys.argv[1])) # self-explanatory, no need to comment here

if __name__ == "__main__":
    main()
