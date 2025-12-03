#!/usr/bin/env python3

# Logs & Time assignment

import sys
from datetime import datetime


def parse_timestamp(line, timefmt):
    # sample acces log entry:
    # 134.209.238.29 - - [09/Oct/2025:14:49:19 -0700] "GET / HTTP/1.0" 302 207 "-" "-"

    left_bracket = line.find("[")
    right_bracket = line.find("]", left_bracket + 1)

    if left_bracket < 0 or right_bracket < 0:
        return None
    date_str = line[left_bracket + 1: right_bracket]
    try:
        return datetime.strptime(date_str, timefmt)
    except ValueError:
        return None


def access_counts_by_hour(my_lines, timefmt):
    """Lazy and pure generator only"""
    current_hour = None
    current_count = 0

    for line in my_lines:
        time_stamp = parse_timestamp(line, timefmt)
        if time_stamp is None:
            continue
        hour = time_stamp.replace(minute=0, second=0, microsecond=0)

        if current_hour is None:
            current_hour = hour
            current_count = 1
            yield current_hour, current_count
            continue

        if hour == current_hour:
            current_count += 1
        else:
            # finalize previous hour
            yield current_hour, current_count
            # start new hour and emit immediately
            current_hour, current_count = hour, 1
            yield current_hour, current_count

    # flush last partial hour
    if current_hour is not None:
        yield current_hour, current_count


def main():
    file_path = sys.argv[1] if len(sys.argv) > 1 else "/var/www/logs/access_log"
    access_log_timefmt = "%d/%b/%Y:%H:%M:%S %z"

    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as my_file:
            previous_date = None
            for hour, count in access_counts_by_hour(my_file, access_log_timefmt):
                # print a blank line to make it clear we've transitioned to a new day
                if previous_date and hour.date() != previous_date:
                    print()
                print(
                    f"{hour:%Y-%m-%d %H:%M:%S %z} {count:4d} "
                    f"access{'es' if count != 1 else ''}",
                    flush=True,
                )
                previous_date = hour.date()
        print(f'\nName of file read: "{file_path}"\n')

    except (FileNotFoundError, PermissionError) as err:
        print(
            f"\nFile \"{file_path}\" not found.\n"
            if isinstance(err, FileNotFoundError)
            else f"No read permission for file \"{file_path}\"\n"
        )


if __name__ == "__main__":
    main()
