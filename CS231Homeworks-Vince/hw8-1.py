#!/usr/bin/env python3
"""
Data Encodings Assignment 10/27-11/2
Reads data exclusively from: /users/abrick/resources/si.csv Displays the top 20 roadways by default.
"""

import sys, csv
from collections import Counter


def _normalize_street(street_name, street_type):
    """Return a cleaned and combined roadway label."""
    parts = filter(None, [(street_name or "").strip(), (street_type or "").strip()])
    return " ".join(parts)

def _generate_roadway_names(rows):
    """Yield combined roadway names from CSV rows."""
    return map(lambda csv_row: _normalize_street(csv_row.get("st_name", ""), csv_row.get("st_type", "")), rows)

def _read_csv(filepath):
    """Read a CSV file and yield rows as dictionaries."""
    with open(filepath, "r", encoding="utf-8", newline="") as f:
        yield from csv.DictReader(f)

def _compute_top_counts(filepath, top_n):
    """Compute and return the top N roadways with the greatest number of intersections."""
    roadways = _generate_roadway_names(_read_csv(filepath)) # Create an iterator of roadway names (already normalized)
    counts = Counter(filter(None, roadways)) # Filter out empty roadway names and count occurrences directly
    return counts.most_common(top_n)  # Return the top N

def _format_list(roadway_counts, title="Top 20 SF roadways by intersection count"):
    """Return a simple numbered list report as a string."""
    return ("No data found.\n" if not roadway_counts else "\n" + "\n".join([title] + list(map(
            lambda ranked_item: f"{ranked_item[0]}. {ranked_item[1][0]} — {ranked_item[1][1]}",
            enumerate(roadway_counts, start=1)))) + "\n")

def main():
    filepath = "/users/abrick/resources/si.csv"
    top_n = 20  # fixed per assignment instructions

    try:
        top_pairs = _compute_top_counts(filepath, top_n)
    except FileNotFoundError:
        sys.stderr.write(f"ERROR: File not found: {filepath}\n")
        sys.exit(2)
    except csv.Error as e:
        sys.stderr.write(f"ERROR: Problem parsing CSV: {e}\n")
        sys.exit(2)
    print(_format_list(top_pairs))

if __name__ == "__main__":
    main()
