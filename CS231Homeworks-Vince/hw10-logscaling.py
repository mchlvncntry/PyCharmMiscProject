#!/usr/bin/env python3
import sys

import re, math

def read_pgm(filepath):
    """Read a grayscale ASCII PGM file using the robust regex tokenizer approach."""

    with open(filepath, 'r') as f:
        # read entire file
        content = f.read()

    # 1. Remove comments anywhere
    content_no_comments = re.sub(r'#.*', '', content)

    # 2. Split on ANY whitespace (spaces, tabs, newlines)
    parts = re.split(r'\s+', content_no_comments.strip())

    if parts[0] != 'P2':
        raise ValueError(f"Not an ASCII PGM file (expected P2, got {parts[0]})")

    # 3. Parse header integers
    try:
        width  = int(parts[1])
        height = int(parts[2])
        max_val = int(parts[3])
    except Exception:
        raise ValueError("Invalid PGM header: width, height, maxval missing or not integers")

    # 4. Collect pixel data
    expected = width * height
    pixel_strings = parts[4:]

    if len(pixel_strings) < expected:
        raise ValueError(f"Expected {expected} pixels, got {len(pixel_strings)}")

    # Convert to integers
    pixels = [int(px) for px in pixel_strings[:expected]]

    return pixels, max_val



def create_histogram(pixels, max_val, num_buckets=16):
    """Create a histogram with the specified number of buckets."""
    buckets = [0] * num_buckets
    bucket_size = (max_val + 1) / num_buckets

    for pixel in pixels:
        bucket_index = min(int(pixel / bucket_size), num_buckets - 1)
        buckets[bucket_index] += 1

    return buckets


def scaled_lengths_log(buckets, max_size):
    """
    Logarithmic scaling of bucket counts into bar lengths 0..max_size.
    - 0 stays 0
    - any positive count gets at least length 1
    - relative order is preserved, but big values are compressed
    """
    max_count = max(buckets)
    if max_count <= 0:
        return [0] * len(buckets)

    log_max = math.log(max_count + 1)

    lengths = []
    for c in buckets:
        if c <= 0:
            lengths.append(0)
        else:
            # log-scale into [0, max_size]
            raw = (math.log(c + 1) / log_max) * max_size
            length = int(raw)
            if length == 0:
                length = 1      # show at least something for any positive count
            lengths.append(length)

    return lengths

def print_vertical_histogram(buckets, max_val):
    """
    Vertical histogram:
    - One bar per bucket.
    - Bar width = width of the bucket label.
    - Small horizontal gap between buckets so bars don't merge.
    - Heights are log-scaled to match the sideways histogram.
    """

    num_buckets = len(buckets)
    max_height = 15  # tallest bar in terminal rows

    # Use the same log-scaling helper as for the sideways plot
    heights = scaled_lengths_log(buckets, max_height)

    # Build bucket labels like [  0- 15], [ 16- 31], ...
    bucket_size = (max_val + 1) / num_buckets
    labels = []
    for i in range(num_buckets):
        start = int(i * bucket_size)
        end   = int((i + 1) * bucket_size - 1)
        if i == num_buckets - 1:
            end = max_val
        labels.append(f"[{start:3d}-{end:3d}]")

    col_width = len(labels[0])   # width of the label = bar width
    gap = 2                      # horizontal space between buckets

    # Draw bars from top to bottom
    for row in range(max_height, 0, -1):
        line = ""
        for h in heights:
            if h >= row:
                line += "█" * col_width + " " * gap
            else:
                line += " " * col_width + " " * gap
        print(line.rstrip())

    # X-axis
    axis = (("─" * col_width) + (" " * gap)) * num_buckets
    print(axis.rstrip())

    # Labels under each bar with the same gap
    label_line = ""
    for label in labels:
        label_line += label + " " * gap
    print(label_line.rstrip())

def print_histogram_sideways(buckets, max_val):
    print("\nHorizontal Histogram (sideways)\n")

    num_buckets = len(buckets)
    max_width = 50  # longest bar length in characters

    lengths = scaled_lengths_log(buckets, max_width)

    bucket_size = (max_val + 1) / num_buckets
    bar_char = "█"

    for i, (count, length) in enumerate(zip(buckets, lengths)):
        start = int(i * bucket_size)
        end   = int((i + 1) * bucket_size - 1)
        if i == num_buckets - 1:
            end = max_val

        label = f"{start:3d}-{end:3d}"
        bar   = bar_char * length

        print(f"{label} {count:6d} | {bar}")
        print("\u200A")  # medium spacing between bars

def main():
    if len(sys.argv) != 2:
        print("Usage: python pgm_histogram.py <path_to_pgm_file>")
        sys.exit(1)

    filepath = sys.argv[1]

    try:
        pixels, max_val = read_pgm(filepath)
        buckets = create_histogram(pixels, max_val, num_buckets=16)
        print_vertical_histogram(buckets, max_val)
        print_histogram_sideways(buckets, max_val)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
