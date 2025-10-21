#!/usr/bin/env python3
"""
Character Encodings Assignment 10/20-10/26
Write a program that expects a filename as argument, and indicates the percentages
of characters in it spanning one, two, three, and four bytes, along with the number
of unique characters occurring in each of those classes.
"""

from collections import Counter
from typing import Dict, FrozenSet, Tuple
import sys

BYTE_CLASSES = (1, 2, 3, 4)
CHARS_PER_LINE = 5
MAX_CHARS_TO_DISPLAY = 100

def usage_and_exit() -> None:
    print("This program analyzes UTF-8 characters by byte length. Run: python3 hw7.py <filename>")
    sys.exit(1)

def read_utf8_stream(path: str):
    """Yield the file content line by line as UTF-8 text."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                yield line
    except FileNotFoundError:
        print(f"Error: file not found: {path}")
        sys.exit(2)
    except PermissionError:
        print(f"Error: permission denied: {path}")
        sys.exit(3)
    except UnicodeDecodeError as e:
        print(f"Error: could not decode file as UTF-8: {e}")
        sys.exit(4)

def aggregate_streaming(filename: str) -> Tuple[int, Counter, Dict[int, FrozenSet[str]]]:
    """
    Single-pass streaming aggregation:
      - counts[byte_len] = total count
      - uniques[byte_len] = frozenset of unique characters (kept immutable)
    """
    counts: Counter = Counter({1: 0, 2: 0, 3: 0, 4: 0})
    uniques: Dict[int, FrozenSet[str]] = {1: frozenset(), 2: frozenset(), 3: frozenset(), 4: frozenset()}
    total_chars = 0

    for line in read_utf8_stream(filename):
        for character in line:
            byte_len = len(character.encode("utf-8"))
            # UTF-8 characters are always 1–4 bytes; ignore anything else defensively
            if byte_len in counts:
                counts[byte_len] += 1
                # union with a single-element frozenset keeps immutability
                uniques[byte_len] = uniques[byte_len] | frozenset([character])
                total_chars += 1

    return total_chars, counts, uniques

def _format_one_class_block(byte_length: int, count: int, total_chars: int, unique_set: FrozenSet[str]) -> str:
    """Return formatted block for one byte-length class with wrapped character lines."""
    percent = (count / total_chars * 100) if total_chars > 0 else 0.0

    header = f"{byte_length}-byte characters: {percent:6.2f}% ({count:,} out of {total_chars:,})"
    uniq_line = f"  Count of unique {byte_length}-byte characters: {len(unique_set)}"

    # Format characters, CHARS_PER_LINE per line, with aligned indentation
    chars_block = ""
    if 0 < len(unique_set) <= MAX_CHARS_TO_DISPLAY:
        sorted_chars = sorted(unique_set)
        groups = [
            ", ".join(repr(c) for c in sorted_chars[i:i+CHARS_PER_LINE])
            for i in range(0, len(sorted_chars), CHARS_PER_LINE)
        ]
        indent = " " * len("  Characters: ")
        # First line has the label; subsequent lines align under it
        if groups:
            first = f"  Characters: {groups[0]}"
            rest = ("\n" + indent).join(groups[1:])
            chars_block = first if len(groups) == 1 else first + "\n" + rest

    parts = [header, uniq_line]
    if chars_block:
        parts.append(chars_block)
    return "\n".join(parts) + "\n\n"

def render_report(filename: str, total_chars: int, counts: Counter, uniques: Dict[int, FrozenSet[str]]) -> str:
    header = f"Total count of characters in '{filename}': {total_chars:,}\n\n"

    class_blocks = "".join(
        _format_one_class_block(
            n,
            counts.get(n, 0),
            total_chars,
            uniques.get(n, frozenset())
        )
        for n in BYTE_CLASSES
    )

    total_unique = sum(len(uniques.get(n, frozenset())) for n in BYTE_CLASSES)
    footer = "-" * 37 + f"\nTotal unique characters: {total_unique}\n\n"

    return header + class_blocks + footer

def analyze(filename: str) -> str:
    total_chars, counts, uniques = aggregate_streaming(filename)
    if total_chars == 0:
        return f"Analysis of '{filename}':\n\nFile is empty."
    return render_report(filename, total_chars, counts, uniques)

def main() -> None:
    if len(sys.argv) != 2:
        usage_and_exit()
    print(analyze(sys.argv[1]))

if __name__ == "__main__":
    main()
