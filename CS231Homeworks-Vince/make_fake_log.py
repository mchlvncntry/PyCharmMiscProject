#!/usr/bin/env python3
# make_fake_log.py
# Generates a realistic fake Apache access_log file in the current directory.

import random
from datetime import datetime, timedelta

# Config: change these if you want more/less data
output_path = "my_fake_access_log_sample"   # file created in current folder
num_lines = 60000                    # number of log lines to generate
start_time = datetime(2024, 10, 6, 8, 0, 0)
time_step_range = (10, 40)           # seconds between requests (random)

paths = [
    "/index.html", "/about.html", "/contact.html", "/login", "/logout",
    "/home", "/search", "/products", "/api/data", "/images/logo.png",
    "/js/app.js", "/style.css", "/blog", "/faq", "/dashboard"
]
statuses = [200, 200, 200, 404, 500, 301, 302]
methods = ["GET", "POST"]

with open(output_path, "w", encoding="utf-8") as f:
    current = start_time
    for i in range(num_lines):
        ip = f"192.168.1.{random.randint(1, 254)}"
        user = random.choice(["-", "admin", "guest", "user"])
        path = random.choice(paths)
        method = random.choice(methods)
        status = random.choice(statuses)
        size = random.randint(100, 5000)
        ts = current.strftime("%d/%b/%Y:%H:%M:%S -0700")
        line = f'{ip} - {user} [{ts}] "{method} {path} HTTP/1.1" {status} {size}\n'
        f.write(line)
        current += timedelta(seconds=random.randint(*time_step_range))

print(f"Wrote {num_lines} fake log lines to {output_path}")
