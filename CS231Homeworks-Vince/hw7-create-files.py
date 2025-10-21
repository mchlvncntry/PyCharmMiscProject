# Create a Latin-1 (ISO-8859-1) encoded file
text = "Hello! This file contains special characters: café, naïve, résumé, ñ, ü"
with open('latin1_sample.txt', 'w', encoding='latin-1') as f:
    f.write(text)

# Create a Windows-1252 encoded file
text = "Windows-1252 special chars: €, †, ‡, •, ™"
with open('windows1252_sample.txt', 'w', encoding='windows-1252') as f:
    f.write(text)

# Create a UTF-16 encoded file
text = "UTF-16 encoding: Hello 世界 🌍"
with open('utf16_sample.txt', 'w', encoding='utf-16') as f:
    f.write(text)

# Create a file with mixed/invalid UTF-8 bytes
with open('invalid_utf8.txt', 'wb') as f:
    f.write(b'Valid ASCII text\n')
    f.write(b'\xff\xfe Invalid UTF-8 bytes\n')
    f.write(b'More text\n')