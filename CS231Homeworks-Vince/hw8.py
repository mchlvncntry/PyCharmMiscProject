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
    return map(lambda csv_row: _normalize_street(csv_row.get("st_name", ""),
                                                 csv_row.get("st_type", "")), rows)

def _read_csv(filepath):
    """Read a CSV file and yield rows as dictionaries."""
    with open(filepath, "r", encoding="utf-8", newline="") as f:
        yield from csv.DictReader(f)


def _compute_top_counts(filepath, top_n):
    """Compute and return the top N roadways with the greatest number of intersections."""
    roadways = _generate_roadway_names(_read_csv(filepath)) # Create an iterator of normalized roadway names
    counts = Counter(filter(None, roadways)) # Filter out empty roadway names and count occurrences
    return counts.most_common(top_n)  # Return the top N

def _format_report(roadway_counts, title="Top 20 SF Roadways with the most intersections"):
    """Return a formatted rank table as a string."""
    if not roadway_counts:
        return "No data found.\n"

    rank_col_width = max(len("Rank"), len(str(len(roadway_counts))))
    name_col_width = max(len("Roadway"), max(len(name) for name, _ in roadway_counts))
    count_col_width = max(len("Intersection Count"), max(len(str(c)) for _, c in roadway_counts))

    header = (f"{'Rank':<{rank_col_width}}  {'Roadway':<{name_col_width}}  "
              f"{'Intersection Count':>{count_col_width}}")
    rule = "-" * len(header)

    lines = [f"{i:<{rank_col_width}}  {name:<{name_col_width}}  {cnt:>{count_col_width}}"
             for i, (name, cnt) in enumerate(roadway_counts, start=1)]

    return "\n" + "\n".join([title, header, rule, *lines]) + "\n"

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
    print(_format_report(top_pairs))

if __name__ == "__main__":
    main()
