#!/usr/bin/env python3
""" HW 10: Feature Extraction, Week 11/10-11/16 — Now shows BEFORE and AFTER contrast histograms """
import sys, re, textwrap
from collections import Counter

# -----------------------------
# READ PGM
# -----------------------------
def read_pgm(filename):
    with open(filename) as content:
        parts = re.split(r'\s+', re.sub(r'#.*', r'\n', content.read()))
        x_dim, y_dim, depth = int(parts[1]), int(parts[2]), int(parts[3])
        pixels = [int(n) for n in parts[4:] if n]
        assert len(pixels) == x_dim * y_dim
    return pixels, depth


# -----------------------------
# HISTOGRAM
# -----------------------------
def create_histogram(pixels, max_val, num_buckets=16):
    bucket_size = (max_val + 1) / num_buckets
    counts = Counter(min(int(p / bucket_size), num_buckets - 1) for p in pixels)
    buckets = [counts[i] for i in range(num_buckets)]
    return buckets, bucket_size


# -----------------------------
# CONTRAST ENHANCEMENT (added)
# -----------------------------
def contrast_stretch(pixels, depth):
    """Increase contrast using percentile stretch (2%–98%)."""
    n = len(pixels)
    if n == 0:
        return pixels[:]

    # Sort a copy to find percentiles
    sorted_pixels = sorted(pixels)
    low_index  = int(0.02 * (n - 1))  # 2nd percentile
    high_index = int(0.98 * (n - 1))  # 98th percentile

    low  = sorted_pixels[low_index]
    high = sorted_pixels[high_index]

    # Avoid divide-by-zero
    if high <= low:
        return pixels[:]

    stretched = []
    for p in pixels:
        if p <= low:
            stretched.append(0)
        elif p >= high:
            stretched.append(depth)
        else:
            # Linearly map [low, high] -> [0, depth]
            val = (p - low) / (high - low) * depth
            stretched.append(int(val))

    return stretched


# -----------------------------
# VERTICAL HISTOGRAM (unchanged)
# -----------------------------
def plot_histogram(buckets, bucket_size, max_val, height=30, title="Histogram"):
    max_count = max(buckets)
    num_buckets = len(buckets)
    print("\n\n")
    print(f"=== {title} ===\n")

    normalized = [int((count / max_count) * height) if max_count > 0 else 0
                  for count in buckets]

    ticks = 10
    raw_interval = max_count / (ticks - 1)
    tick_interval = max(1, int(round(raw_interval / 1000) * 1000))
    tick_values = [i * tick_interval for i in range(ticks)]
    tick_values.reverse()
    tick_levels = [int((val / max_count) * height) for val in tick_values]

    CELL = 4
    LEFT = "       "

    for level in range(height, 0, -1):
        if level in tick_levels:
            idx = tick_levels.index(level)
            tick_label = f"{tick_values[idx]:6d} ┤ "
        else:
            tick_label = "       │ "

        line = ""
        for bar_height in normalized:
            line += ("█".center(CELL) if bar_height >= level else " ".center(CELL))

        print(tick_label + line)

    print(LEFT + "┼" + "━" * (num_buckets * CELL))
    print(LEFT + " " + "".join(f"{i+1:^{CELL}}" for i in range(num_buckets)))

    caption_width = num_buckets * CELL

    caption_text = (
        "Sixteen-bucket Histogram using true linear scaling. "
        "Some smaller bars may not be visible when one bucket dominates, "
        "but linear scale preserves the true proportion of pixel counts."
    )

    wrapped = textwrap.fill(caption_text, width=caption_width)
    for line in wrapped.split('\n'):
        print(LEFT + " " + line)

    print()
    print(f"{LEFT} Bin ranges (0–{max_val}):")
    for i, count in enumerate(buckets):
        start = int(i * bucket_size)
        end   = max_val if i == num_buckets - 1 else int((i + 1) * bucket_size - 1)
        print(f"{LEFT} Bin {i+1:2d}: [{start:3d}-{end:3d}] = {count:,} pixels")


# -----------------------------
# MAIN
# -----------------------------
def main():
    if len(sys.argv) != 2:
        print(f"\nMissing filepath arg, enter: python3 {sys.argv[0]} <path_to_pgm_file>\n", file=sys.stderr)
        sys.exit(1)

    filename = sys.argv[1]

    try:
        # Load original
        pixels, max_val = read_pgm(filename)

        # BEFORE histogram
        before_buckets, before_bucket_size = create_histogram(pixels, max_val)
        plot_histogram(before_buckets, before_bucket_size, max_val,
                       title="BEFORE CONTRAST ADJUSTMENT")

        # CONTRAST ENHANCEMENT
        enhanced_pixels = contrast_stretch(pixels, max_val)

        # AFTER histogram
        after_buckets, after_bucket_size = create_histogram(enhanced_pixels, max_val)
        plot_histogram(after_buckets, after_bucket_size, max_val,
                       title="AFTER CONTRAST ADJUSTMENT")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found\n", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}\n", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}\n", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
