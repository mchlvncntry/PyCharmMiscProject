#!/usr/bin/env python3

# Logs & Time assignment

import sys
from datetime import datetime


def parse_timestamp(line):
    # sample acces log entry:
    # 134.209.238.29 - - [09/Oct/2025:14:49:19 -0700] "GET / HTTP/1.0" 302 207 "-" "-"

    access_log_timefmt = "%d/%b/%Y:%H:%M:%S %z"
    left_bracket = line.find("[")
    right_bracket = line.find("]", left_bracket + 1)

    if left_bracket < 0 or right_bracket < 0:
        return None
    date_str = line[left_bracket + 1 : right_bracket]
    try:
        return datetime.strptime(date_str, access_log_timefmt)
    except ValueError:
        return None


def access_counts_by_hour(my_lines):
    """Lazy and pure generator only"""
    current_hour = None
    current_count = 0

    for line in my_lines:
        time_stamp = parse_timestamp(line)
        if time_stamp is None:
            continue
        hour = time_stamp.replace(minute=0, second=0, microsecond=0)

        if current_hour is None:
            current_hour = hour
            current_count = 1
        elif hour == current_hour:
            current_count += 1
        else:
            yield current_hour, current_count
            current_hour, current_count = hour, 1

    # flush last partial hour
    if current_hour is not None:
        yield current_hour, current_count


def main():
    file_path = sys.argv[1] if len(sys.argv) > 1 else "/var/www/logs/access_log"
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as my_file:
            previous_date = None
            for hour, count in access_counts_by_hour(my_file):
                # print a blank line to make it clear we've transitioned to a new day
                if previous_date and hour.date() != previous_date:
                    print()
                print(
                    f"{hour:%Y-%m-%d %H:%M:%S %z} {count:4d} "
                    f"access{'es' if count != 1 else ''}",
                    flush=True,
                )
                previous_date = hour.date()
        print(f'Name of file read: "{file_path}"\n')

    except (FileNotFoundError, PermissionError) as err:

        err_type = (
            "File not found"
            if isinstance(err, FileNotFoundError)
            else "no read permission for"
        )
        print(f"Error: {err_type}: \"{file_path}\". Goodbye!")


if __name__ == "__main__":
    main()
