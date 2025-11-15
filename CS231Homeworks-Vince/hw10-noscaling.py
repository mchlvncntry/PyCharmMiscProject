#!/usr/bin/env python3
""" HW 10: Feature Extraction, Week 11/10-11/16"""
import sys, re


def read_pgm(filename):
    # Process and input the integer elements of the ASCII PGM file.
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

    for pixel in pixels:
        bucket_idx = min(int(pixel / bucket_size), num_buckets - 1)
        buckets[bucket_idx] += 1

    return buckets

def plot_histogram(buckets, max_val, height=30):
    """Plot vertical histogram using text characters."""
    max_count = max(buckets)
    bucket_size = (max_val + 1) / len(buckets)

    print("\nSixteen-bucket Histogram, no logarithmic scaling, only true linear scaling\n")

    # Convert the raw pixel counts into proportional bar heights that fit nicely on the screen
    normalized = []
    for count in buckets:
        if max_count > 0:
            bar_height = int((count / max_count) * height)
        else:
            bar_height = 0
        normalized.append(bar_height)

    # Y-axis ticks using nice rounded values
    ticks = 10
    raw_interval = max_count / (ticks - 1) # Pick a nice interval like 1000, 2000, 5000, 10000, etc.
    tick_interval = max(1, int(round(raw_interval / 1000) * 1000))
    tick_values = [i * tick_interval for i in range(ticks)] # Build tick values (rounded)
    tick_values.reverse()  # biggest at the top

    # Convert tick values to chart row positions
    tick_levels = [int((val / max_count) * height) if max_count > 0 else 0 for val in tick_values]

    # Draw chart
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
                line += "  █ "
            else:
                line += "    "

        print(tick_label + line)

    print("       ┼" + "━" * (len(buckets) * 4 - 1)) # print x-axis
    # print bucket lines
    print("".join(f" {i:2d} " for i in range(len(buckets))))

    # Print bucket ranges
    print("\nData used:")
    for i in range(len(buckets)):
        start = int(i * bucket_size)
        end = int((i + 1) * bucket_size - 1)
        if i == len(buckets) - 1:
            end = max_val
        print(f"Bucket {i:2d}: [{start:3d}-{end:3d}] = {buckets[i]:7,d} pixels")

    print(f"\nTotal pixels: {sum(buckets):,}")
    print(f"Max bucket count: {max_count:,}\n")


def main():
    if len(sys.argv) != 2:
        print(f"\nMissing filepath arg, enter: python3 {sys.argv[0]} <path_to_pgm_file>\n", file=sys.stderr)
        sys.exit(1)

    filename = sys.argv[1]

    try:
        pixels, max_val = read_pgm(filename)
        buckets = create_histogram(pixels, max_val)
        plot_histogram(buckets, max_val)
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
