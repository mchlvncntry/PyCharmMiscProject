import sys

CLASSES = (1, 2, 3, 4)


# percent helper
def pct(n: int, d: int) -> float:
    return (n / d * 100.0) if d else 0.0


def main() -> None:
    # Validate argument passed.
    if len(sys.argv) != 2:
        print("No filename argument")
        sys.exit(1)
    path = sys.argv[1]

    # total counts per-byte-length and uniques.
    counts = {k: 0 for k in CLASSES}
    uniques = {k: set() for k in CLASSES}
    total = 0

    # Stream the file; classify each character by its UTF-8 byte length.
    try:
        with open(path, "r", encoding="utf-8", errors="strict") as f:
            for line in f:
                for ch in line:
                    total += 1
                    blen = len(ch.encode("utf-8"))
                    if blen in counts:
                        counts[blen] += 1
                        uniques[blen].add(ch)
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}")
        sys.exit(2)
    except UnicodeDecodeError as e:
        print(f"Error: failed to decode '{path}' as UTF-8: {e}")
        sys.exit(3)

    # Print counts.
    print(f"File: {path}")
    print(f"Total characters: {total}")
    for k in CLASSES:
        print(f"{k}-byte: {pct(counts[k], total):.2f}% (unique={len(uniques[k])})")


if __name__ == "__main__":
    main()