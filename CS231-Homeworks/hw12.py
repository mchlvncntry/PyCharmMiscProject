#!/usr/bin/python3
"""Week 11/24-11/30 Containerization & Packages Assignment"""

import ansiplot, random
from collections import Counter

def generate_random_numbers(count, min_val, max_val):
    """Generate a list of random numbers"""
    return [random.randint(min_val, max_val) for _ in range(count)]


def create_bins(numbers, bin_size):
    """Functional binning of numbers into ranges."""
    bin_starts = [((n - 1) // bin_size) * bin_size + 1 for n in numbers] # Round each number to its bin start value
    frequencies = Counter(bin_starts)

    min_val, max_val = min(numbers), max(numbers) # Create labeled bins
    return {f"{start}-{start + bin_size - 1}": frequencies.get(start, 0)
        for start in range(min_val, max_val + 1, bin_size)}


def print_statistics(numbers):
    print("\nDistribution Histogram Of 1000 Random Numbers")
    print(f"Total numbers: {len(numbers):,d}")
    print(f"Minimum value: {min(numbers)},    Maximum value: {max(numbers)}")
    print(f"Average value: {sum(numbers) / len(numbers):.2f}\n")


def plot_histogram(counter_dict):
    """Plot histogram using ansiplot."""
    canvas = ansiplot.Scaled(40, 10, axis=False)

    for pos, (key, value) in enumerate(counter_dict.items(), start=1):
        # Include bin number, range, and count
        canvas.bar(pos, value, title=f"Bin {pos}: {key} ({value} numbers)")
    canvas.show()

def main():
    """Main function to run the histogram program"""
    rand_nums = generate_random_numbers(1000, 1, 100)
    counter_dict = create_bins(rand_nums, 10)  # Create bins of size 10
    print_statistics(rand_nums) # Display results
    plot_histogram(counter_dict)

if __name__ == "__main__":
    main()