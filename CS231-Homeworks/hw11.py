#!/usr/bin/env python3
"""HW 11 Translation, Week 11/17-11/23"""
import sys, re, textwrap
from collections import Counter


def read_pgm(filename):
    """from abrick's notes"""
    with open(filename) as f:
        parts = re.split(r'\s+', re.sub(r'#.*', '\n', f.read()))
    x, y, depth = int(parts[1]), int(parts[2]), int(parts[3])
    pixels = [int(n) for n in parts[4:] if n]
    assert len(pixels) == x * y
    return pixels, depth


def create_histogram(pixels, depth, bins=16):
    """Take pixel values and group them into buckets. Return a list of counts for each bucket."""
    bucket_size = (depth + 1) / bins
    counts = Counter(min(int(p / bucket_size), bins - 1) for p in pixels)
    return [counts[i] for i in range(bins)], bucket_size


def adjust_contrast(pixels, depth):
    """Increase contrast using percentile stretch (2%–98%)."""
    n = len(pixels)
    if n == 0: return pixels[:]
    sorted_pixels = sorted(pixels)
    low_idx, hi_idx = sorted_pixels[int(0.02 * (n-1))], sorted_pixels[int(0.98 * (n-1))] # 2nd,98th percentile
    if hi_idx <= low_idx: return pixels[:]
    return [0 if p <= low_idx else depth if p >= hi_idx else int((p-low_idx) / (hi_idx-low_idx) * depth)
            for p in pixels]


def compute_tick_interval(max_val, ticks=10):
    """Compute spacing between y-axis tick marks using a tick interval given a maximum value."""
    if max_val <= 0: return 1
    raw_interval = max_val / (ticks - 1)
    return max(1, int(round(raw_interval / 1000) * 1000)) # round to nearest 1,000 to keep labels nice


def tick_values_and_levels(max_count, height, ticks=10, tick_interval=None):
    """Return y-axis tick labels and vertical positions."""
    if max_count <= 0:
        return [0] * ticks, [0] * ticks # tick values, tick levels
    interval = tick_interval or compute_tick_interval(max_count, ticks)
    tick_vals = list(reversed([i * interval for i in range(ticks)]))
    tick_lvls = [int((v/max_count) * height) for v in tick_vals]
    return tick_vals, tick_lvls


def plot_histogram(buckets, bucket_size, depth, *, title, caption=None, y_max, tick_interval,height=30):
    """Plot the vertical bar histogram."""
    print(f"\n\n {title}\n")
    CELL, LEFT = 4, "       "
    max_count = max(buckets) if y_max is None else y_max
    norm = [int(c / max_count * height) if max_count > 0 else 0 for c in buckets]

    tick_vals, tick_lvls = tick_values_and_levels(max_count, height, tick_interval=tick_interval)

    # Bars
    for h in range(height, 0, -1):
        label = f"{tick_vals[tick_lvls.index(h)]:6d} ┤ " if h in tick_lvls else "       │ "
        line = "".join("█".center(CELL) if bh >= h else " ".center(CELL) for bh in norm)
        print(label + line)

    # X-axis
    print(LEFT + "┼" + "━"*(CELL*len(buckets)))
    print(LEFT + " " + "".join(f"{i+1:>2}".center(CELL) for i in range(len(buckets))))

    # Caption (default = BEFORE caption)
    if caption is None:
        caption = ("Sixteen-bucket histogram before contrast adjustment using linear scaling. "
            "Some smaller bars may not be visible because Bucket 10 dominates, "
            "but the linear scaling preserves the true proportion of pixel counts.")
    for ln in textwrap.wrap(caption, width=len(buckets)*CELL): print(LEFT + " " + ln)
    print(f"\n{LEFT} Data source: {sys.argv[1]}")
    for i, count in enumerate(buckets):
        start = int(i * bucket_size)
        end = depth if i == len(buckets) - 1 else int((i+1) * bucket_size - 1)
        print(f"{LEFT} Bin {i+1:2d}: [{start:3d}-{end:3d}] = {count:,} pixels")
    print(f"{LEFT} Total pixels: {sum(buckets):,}\n")


def main():
    if len(sys.argv) != 2:
        print(f"\nMissing filepath arg, enter: python3 {sys.argv[0]} <path_to_pgm_file>\n",
              file=sys.stderr)
        sys.exit(1)

    filename = sys.argv[1]
    try:
        pixels, depth = read_pgm(filename)

        # BEFORE + AFTER histograms
        before, bsize = create_histogram(pixels, depth)
        enhanced = adjust_contrast(pixels, depth)
        after, asize = create_histogram(enhanced, depth)

        # Shared Y-axis scale
        global_max = max(max(before), max(after))
        tick_interval = compute_tick_interval(global_max, 10)

        # BEFORE
        plot_histogram(before, bsize, depth,title="Histogram Before Contrast Adjustment",
                       y_max=global_max,tick_interval=tick_interval)

        # AFTER
        after_caption = ("Sixteen-bucket histogram of the contrast-adjusted image using linear scaling."
            " The 2% to 98% percentile adjustment remaps the pixel intensities "
            "by pushing darker values toward 0 and brighter values toward maximum depth, "
            "widening the spread across buckets.")
        plot_histogram(after, asize, depth,title="Histogram After Contrast Adjustment",
                       caption=after_caption, y_max=global_max,tick_interval=tick_interval)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
