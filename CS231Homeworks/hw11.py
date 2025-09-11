'''
Write a universal wrapper program that expects its command line arguments to contain
the absolute path to any program, followed by its arguments. The wrapper should run
that program and report its exit value
'''

from sys import argv
from os.path import exists
from subprocess import call

# Checking whether there is file path provided
if len(argv) < 2:
    print("Error: must provide path to file. Exiting")
    exit(1)

target = argv[1]

# Checking whether file path is valid and exist
if not exists(target):
    print(f"Error: file {target} invalid or does not exist")
    exit(1)

args = argv[2:]

exit_code = call(["python3", target, *args])

print(f"Program {target} exited with code {exit_code}")