'''
Homework 5
Write a generator that calculates the number of seconds since
midnight for events in access_log, and show the first ten when
the program is run
'''

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