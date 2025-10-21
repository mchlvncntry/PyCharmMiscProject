import unittest
from datetime import date, timedelta

td = timedelta(days=-2, hours=10)
print(td)
print(td.days, td.seconds)

print()

result = timedelta(days=1, hours=6) - timedelta(days=2, hours=20)
print(f"Days: {result.days}")
print(f"Seconds: {result.seconds}")
print(f"Total seconds: {result.total_seconds()}")

print()

result = timedelta(days=1, hours=6) - timedelta(days=2, hours=20)
expected = timedelta(days=-2, hours=10)
print(f"Result: {result}")
print(f"Expected: {expected}")
print(f"Are they equal? {result == expected}")

print()

d = date(2025, 1, 1)
result = d + timedelta(days=1000)
print(result)

print()

d = date(2025, 12, 31)
result = d - timedelta(days=1000)
print(result)