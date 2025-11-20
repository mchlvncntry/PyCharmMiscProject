#!/usr/bin/env python3
""" HW 11: TRANSLATION, Week 11/17-11/23 — shows BEFORE and AFTER contrast adjustment histograms """
import sys, re, textwrap
from collections import Counter


def read_pgm(filename):
    """Read an ASCII PGM file and return (pixels, depth)."""
    with open(filename) as content:
        # from abrick's notes
        parts = re.split(r'\s+', re.sub(r'#.*', r'\n', content.read()))
        x_dim, y_dim, depth = int(parts[1]), int(parts[2]), int(parts[3])
        pixels = [int(n) for n in parts[4:] if n]
        assert len(pixels) == x_dim * y_dim
    return pixels, depth


def create_histogram(pixels, max_val, num_buckets=16):
    """Return (buckets, bucket_size) for a 16-bucket histogram."""
    bucket_size = (max_val + 1) / num_buckets
    counts = Counter(min(int(p / bucket_size), num_buckets - 1) for p in pixels)
    buckets = [counts[i] for i in range(num_buckets)]
    return buckets, bucket_size


def adjust_contrast(pixels, depth):
    """Increase contrast using percentile stretch (2%–98%)."""
    n = len(pixels)
    if n == 0:
        return pixels[:]

    sorted_pixels = sorted(pixels)
    low_index  = int(0.02 * (n - 1))  # 2nd percentile
    high_index = int(0.98 * (n - 1))  # 98th percentile

    low  = sorted_pixels[low_index]
    high = sorted_pixels[high_index]

    # Avoid divide-by-zero error
    if high <= low:
        return pixels[:]

    return [
        0 if p <= low else
        depth if p >= high else
        int((p - low) / (high - low) * depth)
        for p in pixels
    ]


def compute_tick_interval(max_val, ticks=10):
    """Compute a nice tick interval given a maximum value."""
    if max_val <= 0:
        return 1
    raw_interval = max_val / (ticks - 1)
    # round to nearest 1,000 to keep labels nice
    return max(1, int(round(raw_interval / 1000) * 1000))


def tick_values_and_levels(max_count, height, ticks=10, tick_interval=None):
    """
    Given a max_count and plot height, return (tick_values, tick_levels, tick_interval_used)
    where tick_levels are the vertical positions corresponding to the tick_values.
    """
    if max_count <= 0:
        tick_values = [0] * ticks
        tick_levels = [0] * ticks
        return tick_values, tick_levels, 1

    interval_used = tick_interval or compute_tick_interval(max_count, ticks)
    tick_values = [i * interval_used for i in range(ticks)]
    tick_values.reverse()
    tick_levels = [
        int((val / max_count) * height) for val in tick_values
    ]
    return tick_values, tick_levels, interval_used


def plot_histogram(
    buckets,
    bucket_size,
    max_val,
    height=30,
    title="Histogram",
    caption_text=None,
    y_max=None,
    tick_interval=None,
):
    """Plot vertical histogram using block characters."""
    print(f"\n\n {title} \n")
    num_buckets = len(buckets)

    # Use shared y_max if provided, otherwise auto-scale from this histogram
    local_max = max(buckets) if buckets else 0
    max_count = y_max if y_max is not None else local_max

    CELL = 4
    LEFT = "       "

    # Normalize bar heights
    normalized = (
        [0 for _ in buckets]
        if max_count <= 0
        else [int((count / max_count) * height) for count in buckets]
    )

    # y-axis ticks (values + vertical levels)
    ticks = 10
    tick_values, tick_levels, _ = tick_values_and_levels(
        max_count, height, ticks=ticks, tick_interval=tick_interval
    )

    # Draw bars
    for level in range(height, 0, -1):
        if level in tick_levels:
            idx = tick_levels.index(level)
            tick_label = f"{tick_values[idx]:6d} ┤ "
        else:
            tick_label = "       │ "

        line = "".join(
            "█".center(CELL) if bar_height >= level else " ".center(CELL)
            for bar_height in normalized
        )
        print(tick_label + line)

    # x-axis
    print(LEFT + "┼" + "━" * (num_buckets * CELL))
    print(LEFT + " " + "".join(f"{i+1:>2}".center(CELL) for i in range(num_buckets)))

    # Caption (default = BEFORE caption)
    if caption_text is None:
        caption_text = (
            "Sixteen-bucket histogram using true linear scaling. "
            "Some smaller bars may not be visible because Bucket 10 dominates, "
            "but linear scaling preserves the true proportion of pixel counts."
        )

    caption_width = num_buckets * CELL
    wrapped = textwrap.fill(caption_text, width=caption_width)
    for line in wrapped.split("\n"):
        print(LEFT + " " + line)

    print(f"\n{LEFT} Data source: {sys.argv[1]}")
    print(f"{LEFT} Bin ranges [0–{max_val}]:")
    for i, count in enumerate(buckets):
        start = int(i * bucket_size)
        end = max_val if i == num_buckets - 1 else int((i + 1) * bucket_size - 1)
        print(f"{LEFT} Bin {i+1:2d}: [{start:3d}-{end:3d}] = {count:,} pixels")
    print(f"{LEFT} Total pixels: {sum(buckets):,}\n")


def main():
    if len(sys.argv) != 2:
        print(
            f"\nMissing filepath arg, enter: python3 {sys.argv[0]} <path_to_pgm_file>\n",
            file=sys.stderr,
        )
        sys.exit(1)

    filename = sys.argv[1]

    try:
        # Load original
        pixels, depth = read_pgm(filename)
        max_val = depth

        # BEFORE contrast adjustment histogram
        before_buckets, before_bucket_size = create_histogram(pixels, max_val)

        # CONTRAST adjustment
        enhanced_pixels = adjust_contrast(pixels, depth)

        # AFTER contrast adjustment histogram
        after_buckets, after_bucket_size = create_histogram(enhanced_pixels, max_val)

        # shared y-axis scale for BEFORE & AFTER
        before_max = max(before_buckets) if before_buckets else 0
        after_max  = max(after_buckets) if after_buckets else 0
        global_max = max(before_max, after_max)

        shared_tick_interval = compute_tick_interval(global_max, ticks=10)

        # BEFORE contrast adjustment histogram
        plot_histogram(
            before_buckets,
            before_bucket_size,
            max_val,
            title="Title: Histogram Before Contrast Adjustment",
            y_max=global_max,
            tick_interval=shared_tick_interval,
        )

        # AFTER contrast adjustment histogram caption
        after_caption = (
            "Sixteen-bucket histogram of the contrast-stretched image using true "
            "linear scaling. The percentile stretch (2%–98%) redistributes pixel "
            "intensities by pushing darker values toward 0 and brighter values "
            "toward the maximum depth, producing a wider spread across buckets."
        )

        # AFTER histogram
        plot_histogram(
            after_buckets,
            after_bucket_size,
            max_val,
            title="Title: Histogram After Contrast Adjustment",
            caption_text=after_caption,
            y_max=global_max,
            tick_interval=shared_tick_interval,
        )

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
