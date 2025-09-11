# # highest ranked
# # //////////// 1st ////////////////

# import re
# import os

# def filename_gen(f_handler):
# 	while True:
# 		pattern_match = re.search('(?:POST|GET|HEAD)(.+?)HTTP',
# 			f_handler.readline())
# 		if pattern_match:
# 			filepath = pattern_match.group(1)
# 			filename = os.path.basename(filepath)
# 			if filename == ' ':
# 				filename = '/'
# 			yield filename

# with open("/etc/httpd/logs/access_log", 'r') as f:
# 	for i in range(10):
# 		print(next(filename_gen(f)))


# //////////// 2nd ////////////////

# #!/usr/bin/env python3
# from os import path

# # this generator function will generate filenames with
# # os.path.basename using the nth column from the input
# def generate_filenames(x, n) :
#     for i in x :
#         # prepare nth column to pass to path.basename()
#         i = i.strip().split() # split using whitespace to count columns
#         if len(i) >= n :
#             if len(path.basename(i[n])) > 0 :
#                 yield path.basename(i[n])
#             else :
#                 continue

# def _main() :
#     print('this program prints filenames from the access_log file on hills...')
#     print('....here are the first 20 examples of output via the generator....')
#     f = open('/etc/httpd/logs/access_log')
#     filename_generator = generate_filenames(f, 6)
#     for i in range(20):
#         print(next(filename_generator))

# if __name__ == '__main__' :
#     _main()


# # //////////// 3rd ////////////////
# #!/usr/local/bin/python3
# """Write a generator that yields one filename at a time from /etc/httpd/logs/access_log"""
# import re

# """One-liner for funsies"""
# # print(*(match.group() for match
# #         in (re.search(r"\S*\.\w*",
# #                       line.split(' ')[6].split('/')[-1])
# #             for line in open("/etc/httpd/logs/access_log").readlines()[:100]
# #             if re.search(r"GET|POST|HEAD", line))
# #         if match is not None), sep='\n')


# def filename_gen(regex, log):
#     """Yields one filename at a time"""
#     for line in log:
#         if re.search(r"GET|POST|HEAD", line):
#             match = re.search(regex, line.split(' ')[6].split('/')[-1])
#             if match is not None:
#                 yield match.group()


# def main():
#     """Prints the first 100 filenames to the terminal"""
#     regex = re.compile(r"\S*\.\w*")
#     with open("/etc/httpd/logs/access_log") as log:
#         for _ in range(100):
#             print(next(filename_gen(regex, log)))


# if __name__ == "__main__":
#     main()


# Homework 5
# Write a generator that calculates the number of seconds since
# midnight for events in access_log, and show the first ten when
# the program is run

import re
from datetime import datetime
from datetime import timedelta

def seconds_since_midnight(file_used):
    while True:
        match = re.search("\[.*\]", file_used.readline())
        if match is not None:
            # print(match.group(0))
            date = datetime.strptime(match.group(0), '[%d/%b/%Y:%H:%M:%S %z]')
            # print(date)
            midnight = date.replace(hour=00, minute =0, second=0)
            yield((date-midnight).total_seconds())

with open("/etc/httpd/logs/access_log", 'r') as f:
	for i in range(10):
		print(next(seconds_since_midnight(f)))



# import re
# import os

# def filename_gen(f_handler):
# 	while True:
# 		pattern_match = re.search('(?:POST|GET|HEAD)(.+?)HTTP',
# 			f_handler.readline())
# 		if pattern_match:
# 			filepath = pattern_match.group(1)
# 			filename = os.path.basename(filepath)
# 			if filename == ' ':
# 				filename = '/'
# 			yield filename

# with open("/etc/httpd/logs/access_log", 'r') as f:
# 	for i in range(10):
# 		print(next(filename_gen(f)))

# import re
# import datetime

# def seconds_since_midnight(f_used):
#     while True:
#         # match the pattern
#         # Pattern: between [], exclude UTC
#         # strip access_time only, not the date
#         # count the seconds with timedelta.total_seconds()¶
#         # yield the total second

# with open("/etc/httpd/logs/access_log", 'r') as f:
# 	for i in range(10):
# 		print(next(seconds_since_midnight(f)))


# match_record = re.compile(r"^[^ ]+ - (C[^ ]*) \[([^ ]+)").match
# strptime = datetime.datetime.strptime

# f = open("very/big/log", "rb")

# for line in f:
#     match = match_record(line)
#     if match is not None:
#         user, str_time = match.groups()
#         time = strptime(str_time, "%d/%b/%Y:%H:%M:%S")
#         print user, repr(time)