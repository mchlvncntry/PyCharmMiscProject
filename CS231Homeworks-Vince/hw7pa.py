import sys
from collections import Counter


def analyze_file(filename):
    try:
        # Read the file with UTF-8 encoding
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()

        # Count occurrences of each character
        char_counts = Counter(content)
        total_chars = sum(char_counts.values())

        # Categorize characters by byte length
        one_byte = set()
        two_bytes = set()
        three_bytes = set()
        four_bytes = set()

        for char in char_counts:
            byte_length = len(char.encode('utf-8'))
            if byte_length == 1:
                one_byte.add(char)
            elif byte_length == 2:
                two_bytes.add(char)
            elif byte_length == 3:
                three_bytes.add(char)
            elif byte_length == 4:
                four_bytes.add(char)

        # Calculate percentages
        one_byte_count = sum(char_counts[char] for char in one_byte)
        two_byte_count = sum(char_counts[char] for char in two_bytes)
        three_byte_count = sum(char_counts[char] for char in three_bytes)
        four_byte_count = sum(char_counts[char] for char in four_bytes)

        print(f"Total characters: {total_chars}")
        print(f"1-byte characters: {len(one_byte)} unique, {one_byte_count / total_chars * 100:.2f}%")
        print(f"2-byte characters: {len(two_bytes)} unique, {two_byte_count / total_chars * 100:.2f}%")
        print(f"3-byte characters: {len(three_bytes)} unique, {three_byte_count / total_chars * 100:.2f}%")
        print(f"4-byte characters: {len(four_bytes)} unique, {four_byte_count / total_chars * 100:.2f}%")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except UnicodeDecodeError:
        print(f"Error: File '{filename}' contains invalid UTF-8 characters.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
    else:
        analyze_file(sys.argv[1])

'''
Sample outpout 
echo "Hello world! こんにちは ¡Hola! 😊 你今天过得怎么样" > hw77.txt
python3 hw7.py hw77.txt
Total characters: 37
1-byte characters: 11 unique, 59.46%
2-byte characters: 1 unique, 2.70%
3-byte characters: 13 unique, 35.14%
4-byte characters: 1 unique, 2.70%
'''

'''
I have try to make a file (hw77.txt) by myself, this file including Chinese, Japanese, English and emoji. That will be shows different byte(1,2,3,4,bytes), use this file to test if my program is run correctly or not.
all English is 1 bytes, and other languages will be 2 or 3 bytes, and emoji will shows 4 bytes.
My terminal editor didn't accpet unicode characters correctly, so it will shows like ^a^s, so I change to use the echo command instead.
'''