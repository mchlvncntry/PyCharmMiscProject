'''
Write a program that creates a pool of workers to all at once check whether or
not the files whose pathnames are passed in are encoded in UTF-8
'''

import concurrent.futures
import sys
import codecs


def utf8Checker(pathnameToFile):
    try:
        codecs.open(pathnameToFile, encoding='utf-8', errors='strict')
        print(pathnameToFile + ": Valid utf-8")
    except UnicodeDecodeError:
        print(pathnameToFile + ": invalid utf-8")


filename = sys.argv[1:]
pool = concurrent.futures.ThreadPoolExecutor()

if len(sys.argv) < 2:
    print('Error: please provide pathnames to files')
else:
    pool.map(utf8Checker,filename)