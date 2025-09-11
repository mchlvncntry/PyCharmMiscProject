# HW3
# Write a generator that yields one filename at a time from /etc/httpd/logs/access_log

# In the result, home directory (i.e. /) is counted as filename
# because that is where a user accessed.
# If we do not count home directory as filename, then we just add
# “and parts[6] != '/' “  into filter and exclude home directory from the result.
# Other than that, generator is pretty straight forward.

def file_name():
    log_file = open('/etc/httpd/logs/access_log', 'r').readlines()
    for line in log_file:
        parts = line.split()
        if parts[6] is not None:
            yield parts[6]