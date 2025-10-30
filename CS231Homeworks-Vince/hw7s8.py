'''
Analyze UTF-8 encoded file to show percentage and unique count
of characters by byte length (1, 2, 3, or 4 bytes).
'''
import sys

def analyze_utf8(filename):
    # Open in binary mode to work with raw bytes, then decode to UTF-8
    try:
        with open(filename, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    # Decode bytes to Unicode string, handling invalid UTF-8
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        print(f"Error: File '{filename}' is not valid UTF-8.")
        sys.exit(1)

    # Check for empty file
    if not text:
        print(f"File '{filename}' is empty.")
        return

    # Track counts and unique characters for each byte-length class
    byte_classes = {1: 0, 2: 0, 3: 0, 4: 0}
    unique_chars = {1: set(), 2: set(), 3: set(), 4: set()}

    # Single pass through all characters
    for ch in text:
        # Determine byte length when encoded as UTF-8
        byte_length = len(ch.encode('utf-8'))
        byte_classes[byte_length] += 1
        unique_chars[byte_length].add(ch)

    total_chars = len(text)

    # Display results
    print(f'UTF-8 Analysis: {filename}')
    print(f'Total characters: {total_chars}')
    print('=' * 60)

    for n in (1, 2, 3, 4):
        count = byte_classes[n]
        percent = (count / total_chars * 100)
        unique_count = len(unique_chars[n])
        print(f'{n}-byte characters: {percent:6.2f}% ({count:,}/{total_chars:,}) | Unique: {unique_count:,}')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} <filename>')
        sys.exit(1)

    analyze_utf8(sys.argv[1])