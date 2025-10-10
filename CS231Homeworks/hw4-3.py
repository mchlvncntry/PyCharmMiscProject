from pathlib import Path

def lazy_rewrapper(file_name, width=80):
    """
    Lazily rewrap text from a file so each yielded line is <= width chars
    (unless a single word is longer than width), without breaking words.
    Preserves blank lines as paragraph breaks.
    """
    p = Path(file_name).expanduser()

    current = []
    current_len = 0

    with p.open('r', encoding='utf-8') as f:
        for raw in f:
            words = raw.split()  # split on any whitespace; no empty tokens

            # blank line → paragraph break
            if not words:
                if current:
                    yield " ".join(current)
                    current, current_len = [], 0
                yield ""  # preserve the blank line
                continue

            for w in words:
                w_len = len(w)
                if current_len == 0:
                    # start a new line with w (even if > width; don't break words)
                    current = [w]
                    current_len = w_len
                elif current_len + 1 + w_len <= width:
                    current.append(w)
                    current_len += 1 + w_len  # +1 for the space
                else:
                    yield " ".join(current)
                    current = [w]
                    current_len = w_len

        # flush remaining words at EOF
        if current:
            yield " ".join(current)

# Example usage:
if __name__ == "__main__":
    wrapped_text = lazy_rewrapper("/Users/mvrayo-mini/Downloads/text.txt", width=80)
    for line in wrapped_text:
        print(line)
