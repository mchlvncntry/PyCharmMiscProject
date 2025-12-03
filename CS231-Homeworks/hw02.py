# Assignment: Functional Model
# /etc/passwd  - every line is colon-separated into seven fields

with open("/etc/passwd") as my_file:
    # line.strip() to strip all leading and trailing whitespace
    # the reason for the str.strip is to guarantee
    # that each line is clean at the beginning
    # before extracting the shell info
    # formatted the one-liner code into multiple lines for readability
    lines = filter(lambda line: line and not line.startswith("#"), map(str.strip, my_file))

    # rsplit to obtain the last field in the line
    # no need to use strip() here since the lines were all cleaned earlier
    shells = map(lambda sh: sh.rsplit(":", 1)[-1], lines)

    # count the total number of /bin/drop or /sbin/nologin
    #drop_nologin_count = sum(1 for sh in shells if sh in ("/bin/drop", "/sbin/nologin"))
    drop_nologin_count = sum(map(lambda item: item in ("/bin/drop", "/sbin/nologin"), shells))

# I used f-string here for readability in the command-line interface
print(f'\nCount of users with either "/bin/drop" or "/sbin/nologin" ---> {drop_nologin_count}\n')