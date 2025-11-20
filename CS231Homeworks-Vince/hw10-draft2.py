#!/usr/bin/env python3
""" HW 10: Feature Extraction, Week 11/10-11/16"""
import sys, re
from collections import Counter

def read_pgm(filename):
    # Using abrick's code found in his notes
    with open(filename) as content:
        parts = re.split(r'\s+', re.sub(r'#.*', r'\n', content.read()))
        x_dim, y_dim, depth = int(parts[1]), int(parts[2]), int(parts[3])
        pixels = [int(n) for n in parts[4:] if n]
        assert len(pixels) == x_dim * y_dim

    return pixels, depth


def create_histogram(pixels, max_val, num_buckets=16):
    """Create histogram with specified number of buckets."""
    buckets = [0] * num_buckets
    bucket_size = (max_val + 1) / num_buckets
    counts = Counter(min(int(p / bucket_size), num_buckets-1) for p in pixels)
    buckets = [counts[i] for i in range(num_buckets)]
    return buckets, bucket_size


def plot_histogram(buckets, bucket_size, max_val, height=30):
    """Plot vertical histogram using block characters."""
    max_count = max(buckets)
    num_buckets = len(buckets)
    print("\n\n")

    # Normalize/convert each raw bucket counts into scaled bar height that fit terminal window
    normalized = [int((count/max_count) * height) if max_count > 0 else 0 for count in buckets]

    # Y-axis ticks (rounded thousands)
    ticks = 10
    raw_interval = max_count / (ticks - 1)
    tick_interval = max(1, int(round(raw_interval / 1000) * 1000))
    tick_values = [i * tick_interval for i in range(ticks)]
    tick_values.reverse()  # biggest at top

    tick_levels = [int((val / max_count) * height) for val in tick_values]

    # --- FIXED SPACING CONSTANTS ---
    CELL = 4               # width of each bar column ("  █ ")
    LEFT = "       "       # same margin as y-axis labels (7 spaces)

    # Draw histogram rows from top to bottom
    for level in range(height, 0, -1):
        if level in tick_levels:
            idx = tick_levels.index(level)
            tick_label = f"{tick_values[idx]:6d} ┤ "
        else:
            tick_label = "       │ "

        # Bars
        line = ""
        for bar_height in normalized:
            if bar_height >= level:
                line += "█".center(CELL)
            else:
                line += " ".center(CELL)

        print(tick_label + line)

    # --- X-AXIS BELOW BARS ---
    print(LEFT + "┼" + "━" * (num_buckets * CELL))

    # centered bin labels 0 1 2 ... 15
    label_row = "".join(f"{i+1:^{CELL}}" for i in range(num_buckets))
    print(LEFT + " " + label_row)

    print("\nSixteen-bucket Histogram, no logarithmic scaling, only true linear scaling\n"
          "Because the value of the highest bar is so big, some of the bars with really small values may not be visible.\n"
          "I chose not to use log scaling because I did not want the resulting histogram to distort the actual data.")

    print(f"\nData source: {sys.argv[1]}")
    for i in range(num_buckets):
        start = int(i * bucket_size)
        end = int((i + 1) * bucket_size - 1)
        if i == num_buckets - 1:
            end = max_val
        print(f"Bin {i+1:2d}: [{start:3d}-{end:3d}] = {buckets[i]:3,d} pixels")

    #print(f"\nTotal pixels: {sum(buckets):,}")
    #print(f"Max bin count: {max_count:,}\n")


def main():
    if len(sys.argv) != 2:
        print(f"\nMissing filepath arg, enter: python3 {sys.argv[0]} <path_to_pgm_file>\n", file=sys.stderr)
        sys.exit(1)

    filename = sys.argv[1]

    try:
        pixels, max_val = read_pgm(filename)
        buckets, bucket_size = create_histogram(pixels, max_val)
        plot_histogram(buckets,bucket_size,  max_val)
    except FileNotFoundError:
        print(f"\nError: File '{filename}' not found\n", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"\nError: {e}\n", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}\n", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
