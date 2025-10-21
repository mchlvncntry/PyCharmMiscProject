# Determine whether the file passed is encoded as UTF-8:
import sys
def check(file):
    with open(file) as handle:
        try:
            handle.read()
            return True
        except UnicodeDecodeError:
            return False
print(check(sys.argv[1]))