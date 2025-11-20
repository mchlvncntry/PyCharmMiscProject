#!/usr/bin/env python3
import sys
import re, math

def read_pgm(filepath):
    """Read a grayscale ASCII PGM file using the robust regex tokenizer approach."""

    with open(filepath, 'r') as f:
        content = f.read()

    content_no_comments = re.sub(r'#.*', '', content)
    parts = re.split(r'\s+', content_no_comments.strip())

    if parts[0] != 'P2':
        raise ValueError(f"Not an ASCII PGM file (expected P2, got {parts[0]})")

    try:
        width  = int(parts[1])
        height = int(parts[2])
        max_val = int(parts[3])
    except Exception:
        raise ValueError("Invalid PGM header")

    expected = width * height
    pixel_strings = parts[4:]

    if len(pixel_strings) < expected:
        raise ValueError(f"Expected {expected} pixels, got {len(pixel_strings)}")

    pixels = [int(px) for px in pixel_strings[:expected]]
    return pixels, max_val


def create_histogram(pixels, max_val, num_buckets=16):
    """Create a histogram with the specified number of buckets."""
    buckets = [0] * num_buckets
    bucket_size = (max_val + 1) / num_buckets

    for pixel in pixels:
        b = min(int(pixel / bucket_size), num_buckets - 1)
        buckets[b] += 1

    return buckets


# -------------------------------
# TRUE LINEAR SCALING (no log)
# -------------------------------
def scale_linear(buckets, max_height):
    """
    True proportional linear scaling:
    height = (count / max_count) * max_height
    """
    max_count = max(buckets)
    if max_count == 0:
        return [0] * len(buckets)

    scaled = []
    for c in buckets:
        h = int((c / max_count) * max_height)
        if c > 0 and h == 0:
            h = 1
        scaled.append(h)

    return scaled


def print_vertical_histogram(buckets, max_val):
    """
    TRUE LINEAR vertical histogram:
    - bar height is directly proportional to count
    - bar width = label width
    - no logarithmic scaling
    """

    num_buckets = len(buckets)
    max_height = 15

    # TRUE proportional heights
    heights = scale_linear(buckets, max_height)

    # Build labels like [  0- 15]
    bucket_size = (max_val + 1) / num_buckets
    labels = []
    for i in range(num_buckets):
        start = int(i * bucket_size)
        end   = int((i + 1) * bucket_size - 1)
        if i == num_buckets - 1:
            end = max_val
        labels.append(f"[{start:3d}-{end:3d}]")

    col_width = len(labels[0])
    gap = 2

    # Draw top → bottom
    for row in range(max_height, 0, -1):
        line = ""
        for h in heights:
            if h >= row:
                line += "█" * col_width + " " * gap
            else:
                line += " " * col_width + " " * gap
        print(line.rstrip())

    axis = (("─" * col_width) + (" " * gap)) * num_buckets
    print(axis.rstrip())

    label_line = ""
    for label in labels:
        label_line += label + " " * gap
    print(label_line.rstrip())


# --------------------------------
# SIDEWAYS HISTOGRAM STILL LOG-SCALED
# --------------------------------

def scaled_lengths_log(buckets, max_size):
    """(unchanged)"""
    max_count = max(buckets)
    if max_count <= 0:
        return [0] * len(buckets)

    log_max = math.log(max_count + 1)
    lengths = []
    for c in buckets:
        if c <= 0:
            lengths.append(0)
        else:
            raw = (math.log(c + 1) / log_max) * max_size
            length = int(raw)
            if length == 0:
                length = 1
            lengths.append(length)
    return lengths


def print_histogram_sideways(buckets, max_val):
    print("\nHorizontal Histogram (sideways)\n")

    num_buckets = len(buckets)
    max_width = 50

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


def main():
    if len(sys.argv) != 2:
        print("Usage: python pgm_histogram.py <pgm-file>")
        sys.exit(1)

    filepath = sys.argv[1]

    try:
        pixels, max_val = read_pgm(filepath)
        buckets = create_histogram(pixels, max_val, num_buckets=16)
        print_vertical_histogram(buckets, max_val)
        print_histogram_sideways(buckets, max_val)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
