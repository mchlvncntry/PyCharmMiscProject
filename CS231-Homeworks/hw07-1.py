#!/usr/bin/env python3
"""
Character Encodings Assignment 10/20-10/26
I also chose to display the unique characters for each byte-length class
when the number of unique characters does not exceed 100
(the program’s default limit per class).
"""
import sys
from collections import Counter
from functools import reduce
from itertools import chain
import unicodedata

BYTE_CLASSES = (1, 2, 3, 4)
CHARS_PER_LINE = 5
MAX_CHARS_TO_DISPLAY = 100


def usage_and_exit():
    """Display a usage message and exit the program if no file argument is provided."""
    program_name = sys.argv[0] or "<name_of_file.py>"
    print(f"\nNo file arg entered. Please run:\npython3 {program_name} <file arg here>\n")
    sys.exit(1)


def read_chunks(path, chunk_size=8192):
    """Read a UTF-8 text file lazily and yield it in chunks of the given size.
       This helper function is designed to read a text file piece by piece (in chunks)
       instead of loading the entire file into memory at once. Allows this program to process
       very large text files efficiently.
    """
    with open(path, "r", encoding="utf-8", newline=None) as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk


def utf8_byte_length(charac_code):
    """Return the number of UTF-8 bytes required to encode a Unicode code point.
       Determines how many bytes (1–4) are needed to represent a given Unicode
       code point in UTF-8, without actually performing the encoding.
       Source: https://www.w3.org/International/articles/definitions-characters/
    """
    if charac_code <= 0x7F:
        return 1
    elif charac_code <= 0x7FF:
        return 2
    elif charac_code <= 0xFFFF:
        return 3
    else:
        return 4


def count_utf8_characters(path, normalize=None):
    """Count and classify all characters in a UTF-8 text file by byte length (1,2,3,4 bytes),
       including the number and percentage of unique characters in each class.
    """
    try:
        # Read file passed in chunks, normalizes if needed, and creates a continuous stream of characters.
        normalizer = (lambda s: unicodedata.normalize(normalize, s)) if normalize else (lambda s: s)
        char_stream = chain.from_iterable(map(normalizer, read_chunks(path)))

        # Helper function for reduce(): updates totals and unique sets for each character.
        def step(accumulator, character):
            char_total, byte_counts, unique_chars = accumulator
            char_total += 1
            byte_length = utf8_byte_length(ord(character))  # faster than len(character.encode("utf-8"))
            byte_counts[byte_length] += 1
            unique_chars[byte_length].add(character)
            return char_total, byte_counts, unique_chars

        # Initialize counters and unique sets for 1,2,3,4 byte classes
        initial_state = (0, Counter(), {n: set() for n in BYTE_CLASSES})
        total_chars, byte_length_counts, unique_char_sets = reduce(step, char_stream, initial_state)

        # Freeze unique sets for immutability
        frozen_uniques = dict(
            map(lambda k: (k, frozenset(unique_char_sets[k])), BYTE_CLASSES)
        )
        return total_chars, byte_length_counts, frozen_uniques

    except FileNotFoundError:
        print(f"Error: file '{path}' not found.")
        sys.exit(2)
    except PermissionError:
        print(f"Error: permission denied to file '{path}'.")
        sys.exit(3)
    except UnicodeDecodeError as e:
        print(f"Error: could not decode file '{path}' as UTF-8.\n{e}")
        sys.exit(4)



def _format_one_class_block(byte_len, count, total, uniq):
    """Format a readable text block showing statistics for one UTF-8 byte-length class.
       Includes the percentage of characters in this class, the number of unique characters,
       and a preview list of the unique characters (if not too many to display).
    """
    ## Calculate the percentage of characters in this byte-length class
    percent = (count / total * 100) if total else 0.0

    # Main header lines showing count and percentage
    header = f"{byte_len}-BYTE CHARACTERS: {percent:6.2f}% ({count:,} out of {total:,})"
    uniq_line = f"  Count of unique {byte_len}-byte characters: {len(uniq)}"

    # If len(uniq) is greater than MAX_CHARS_TO_DISPLAY (100 by default),
    # the program skips printing the list of unique characters to avoid flooding
    # the command shell terminal with too much output. In that case, only the total count
    # of unique characters is shown in the summary line above.
    characs_block = ""
    if 0 < len(uniq) <= MAX_CHARS_TO_DISPLAY:
        sorted_characs = sorted(uniq)
        # Group characters for cleaner multi-line display (e.g., 5 per line)
        groups = list(
            map(
                lambda i: ", ".join(map(repr, sorted_characs[i:i + CHARS_PER_LINE])),
                range(0, len(sorted_characs), CHARS_PER_LINE),
            )
        )
        # Label and indent the wrapped lines
        label = "  Unique Characters: "
        indent = " " * len(label)
        wrapped = ("\n" + indent).join(groups)
        characs_block = f"{label}{wrapped}"

    # Combine all lines into a single formatted string
    parts = [header, uniq_line]
    if characs_block:
        parts.append(characs_block)
    return "\n".join(parts) + "\n\n"


def render_report(filename, total, counts, uniques):
    """Create and return a formatted text report summarizing character statistics for a file."""

    # Handle empty files separately
    if total == 0:
        return f"Analysis of '{filename}':\n\nFile is empty."

    # Header showing the total number of characters in the file
    header = f"\n\nTotal count of characters in '{filename}': {total:,}\n\n"

    # Build the main report body by formatting each byte-length class (1–4 bytes)
    class_blocks = "".join(
        map(
            lambda n: _format_one_class_block(n, counts.get(n, 0), total, uniques.get(n, frozenset())),
            BYTE_CLASSES,
        )
    )

    # Calculate the overall number of unique characters across all byte-length classes
    total_unique = sum(map(lambda n: len(uniques.get(n, frozenset())), BYTE_CLASSES))

    # Footer showing total unique count, separated by a divider line
    footer = "-" * 45 + f"\nTotal count of unique characters: {total_unique}\n\n"

    # Combine all parts into a single formatted string
    return header + class_blocks + footer


def main():
    if len(sys.argv) != 2:
        usage_and_exit()
    filename = sys.argv[1]
    total, counts, uniques = count_utf8_characters(filename, normalize=None)
    print(render_report(filename, total, counts, uniques))


if __name__ == "__main__":
    main()
