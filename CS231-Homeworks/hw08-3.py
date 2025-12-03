#!/usr/bin/env python3
"""CS 231 — Data Encodings HW9
This program finds which San Francisco streets have the most intersections.
It reads the SF roadway dataset, groups streets by their shared intersection
points, counts how many distinct intersections each street has, and prints the
top twenty roadways with the highest counts.
"""

import csv
from collections import defaultdict, Counter

def join_name_type(name, typ):
    name = (name or "").strip()
    typ = (typ or "").strip()
    if name and typ:
        return f"{name} {typ}"
    return name or typ  # whichever exists

def read_points(path):
    """Read the CSV and group streets by their shared geometric point."""
    by_point = defaultdict(set)
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            point = (row.get("the_geom") or "").strip()
            if not point:
                continue
            street = join_name_type(row.get("st_name"), row.get("st_type"))
            if street:
                by_point[point].add(street)
    return by_point

def count_intersections(by_point, mode="k_minus_1"):
    """
    Count how many intersections each street has.
    Determine first how intersections are counted:
    "k_minus_1"  (measures how many *other streets* a road intersects)
    "one_per_point" (measures how many distinct intersection locations a road has)
    """
    counts = Counter()
    for streets in by_point.values():
        k = len(streets)
        if k < 2:
            continue
        inc = (k - 1) if mode == "k_minus_1" else 1
        for s in streets:
            counts[s] += inc
    return counts

def main():
    path = "/Users/mvrayo-mini/Downloads/sfroadways.csv"
    by_point = read_points(path)
    counts = count_intersections(by_point, mode="k_minus_1")

    # Sort by count (descending), then by name (alphabetically)
    top20 = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0].casefold()))[:20]

    # Print formatted table
    print("\nTop 20 San Francisco Roadways with the Most Intersections\n")
    print("Rank  Roadway Name                         Intersections")
    print("----  -----------------------------------  -------------")
    for i, (name, cnt) in enumerate(top20, 1):
        print(f"{i:>2}.   {name:<35}  {cnt:>7}")
    print()

    # -----------------------------------------------------------
    # Extra section: list all streets that intersect with Mission Street
    # -----------------------------------------------------------
    """target = "MISSION ST"
    intersects = set()

    for streets in by_point.values():
        if target in streets:
            intersects.update(streets - {target})  # add all other streets at that point

    print(f"\nStreets that intersect with {target} ({len(intersects)} total):\n")
    for name in sorted(intersects, key=str.casefold):
        print(name)
    """
    # --- All occurrences: print every street that meets MISSION ST, once per point ---
    target = "MISSION ST"

    print(f"\nEvery occurrence of streets intersecting {target}:\n")

    # Collect (name, point) pairs so we can sort for a stable, readable list
    occurrences = []
    for point, streets in by_point.items():
        if target in streets:
            for s in streets:
                if s != target:
                    occurrences.append((s, point))

    # Sort by street name (case-insensitive), then by point string
    occurrences.sort(key=lambda t: (t[0].casefold(), t[1]))

    # Print one line per occurrence (so if VALENCIA ST meets twice, it prints twice)
    for name, point in occurrences:
        print(f"{name}  @  {point}")

    # Optional: show a small summary so you can see duplicates per street name
    # from collections import Counter  # already imported above
    summary = Counter(name for name, _ in occurrences)
    print(f"\nTotal occurrences: {len(occurrences)}")
    print("Occurrences per street (duplicates reflect multiple distinct points):")
    for name, c in sorted(summary.items(), key=lambda kv: (-kv[1], kv[0].casefold())):
        print(f"  {name}: {c}")



if __name__ == "__main__":
    main()
