#!/usr/bin/env python3
""" Data Encodings Assignment 10/27-11/2 """
import csv
from collections import Counter

# Return a cleaned and combined roadway label.
normalize = lambda r: " ".join(filter(None, map(str.strip, [r.get("st_name", ""), r.get("st_type", "")])))

# Generator that yields combined roadway names from CSV rows.
generate_names = lambda rows: map(normalize, rows)

# Read a CSV file and yield each row as a dictionary
def read_csv(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        yield from csv.DictReader(f)

# Create an iterator of normalized roadway names, filter out blanks and count roadway occurrences
# Sort by intersection count (highest first), then alphabetically by roadway name
# to ensure a deterministic tie-break. Roads with the same count always appear in the same order.
compute_top_counts = lambda path, n=20: sorted(
    Counter(filter(None, generate_names(read_csv(path)))).items(), key=lambda item: (-item[1], item[0].casefold()))[:n]

# produce a "report" as required by the assignment
format_report = lambda rows: "\n".join(
    ["Rank  Roadway Name      Intersections",
     "----  ----------------  -------------"] +
    [f"{i:>2}.    {name:<18}  {cnt:>7}" for i, (name, cnt) in enumerate(rows, 1)])

if __name__ == "__main__":
    # no error handling since filepath is fixed & guaranteed
    filepath = "/users/abrick/resources/si.csv"
    print("\nTop 20 SF Roadways with the Most Intersections\n")
    print(format_report(compute_top_counts(filepath)) + "\n")
