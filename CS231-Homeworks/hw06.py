#!/usr/bin/env python3

"""
Testing Assignment 10/13-10/19
Use unittest.TestCase methods to check that adding and subtracting
date and timedelta objects gives the correct results.
"""

import unittest
from datetime import date, timedelta


# ------------------------------------------
# Part 1: Testing (timedelta +/- timedelta)
# ------------------------------------------

class TestTimedeltaAddition(unittest.TestCase):
    """Tests for adding two timedelta objects."""

    def test_add_days(self):
        # 360 days + 5 days should give 365 days
        result = timedelta(days=360) + timedelta(days=5)
        self.assertEqual(result, timedelta(days=365))

    def test_add_hours_days_rollover(self):
        # 2 days 6 hours + 1 day 20 hours = 3 days 26 hours
        # Python automatically turns that into 4 days 2 hours
        result = timedelta(days=2, hours=6) + timedelta(days=1, hours=20)
        self.assertEqual(result, timedelta(days=4, hours=2))

    def test_add_minutes_seconds_microseconds_rollover(self):
        # Adding times with minutes, seconds, and microseconds
        # extra values are carried over to the next bigger unit (like seconds to minutes)
        left = timedelta(days=2, hours=4, minutes=10, seconds=10, microseconds=10)
        right = timedelta(days=1, hours=23, minutes=55, seconds=55, microseconds=55)
        result = left + right
        self.assertEqual(result, timedelta(days=4, hours=4, minutes=6, seconds=5, microseconds=65))

    def test_add_negative_timedelta_rollover(self):
        # Adding a negative timedelta moves the total backwards in time
        left = timedelta(days=-3, hours=-14, minutes=-16, seconds=-18, microseconds=-10)
        right = timedelta(days=2, hours=4, minutes=6, seconds=8, microseconds=1)
        result = left + right
        self.assertEqual(result, timedelta(days=-2, hours=13, minutes=49, seconds=49, microseconds=999_991))

    def test_add_zero_timedelta(self):
        # Adding zero should not change the timedelta
        td = timedelta(days=5, hours=3, minutes=30)
        result = td + timedelta(0)
        self.assertEqual(result, td)

    def test_add_large_timedeltas(self):
        # Large timedelta values should still add correctly
        result = timedelta(days=1000) + timedelta(days=365)
        self.assertEqual(result, timedelta(days=1365))

    def test_commutativity_of_addition(self):
        # Adding a + b should give the same as b + a
        a = timedelta(days=3, hours=12)
        b = timedelta(days=1, hours=6)
        self.assertEqual(a + b, b + a)


class TestTimedeltaSubtraction(unittest.TestCase):
    """Tests for subtracting one timedelta from another."""

    def test_subtract_days(self):
        # 365 days - 5 days = 360 days
        result = timedelta(days=365) - timedelta(days=5)
        self.assertEqual(result, timedelta(days=360))

    def test_subtract_hours_negative_result_rollover(self):
        # 1 day 6 hours - 2 days 20 hours = a negative time
        # Python turns it into -2 days + 10 hours
        result = timedelta(days=1, hours=6) - timedelta(days=2, hours=20)
        self.assertEqual(result, timedelta(days=-2, hours=10))

    def test_subtract_minutes_seconds_microseconds_rollover(self):
        # Subtracting with small time units, borrow happens across units
        left = timedelta(days=2, hours=4, minutes=10, seconds=10, microseconds=10)
        right = timedelta(days=1, hours=23, minutes=55, seconds=55, microseconds=55)
        result = left - right
        self.assertEqual(result, timedelta(hours=4, minutes=14, seconds=14, microseconds=999_955))

    def test_subtract_negative_timedelta_rollover(self):
        # Subtracting from a negative timedelta gives a more negative result
        left = timedelta(days=-3, hours=-4, minutes=-6, seconds=-8, microseconds=-1)
        right = timedelta(days=2, hours=4, minutes=6, seconds=8, microseconds=1)
        result = left - right
        self.assertEqual(result, timedelta(days=-6, hours=15, minutes=47, seconds=43, microseconds=999_998))

    def test_subtract_zero_timedelta(self):
        # Subtracting zero doesn’t change anything
        td = timedelta(days=7, hours=12, minutes=45)
        result = td - timedelta(0)
        self.assertEqual(result, td)

    def test_subtract_same_timedelta_yields_zero(self):
        # Subtracting the same timedelta gives zero
        td = timedelta(days=5, hours=3, minutes=30, seconds=15)
        result = td - td
        self.assertEqual(result, timedelta(0))


# ----------------------------------------------------------------------
# Part 2: Testing (date + timedelta), (date - timedelta), (date - date)
# ----------------------------------------------------------------------

class TestDateArithmetic(unittest.TestCase):
    """Tests for date math using timedelta and other dates."""

    def test_date_plus_timedelta(self):
        # Adding 10 days to Oct 14, 2025 should give Oct 24, 2025
        d = date(2025, 10, 14)
        self.assertEqual(d + timedelta(days=10), date(2025, 10, 24))

    def test_timedelta_plus_date_commutativity(self):
        # date + timedelta gives same result as timedelta + date
        d = date(2025, 3, 15)
        td = timedelta(days=7)
        self.assertEqual(d + td, td + d)

    def test_date_minus_timedelta(self):
        # Subtracting 10 days from Oct 14, 2025 gives Oct 4, 2025
        d = date(2025, 10, 14)
        self.assertEqual(d - timedelta(days=10), date(2025, 10, 4))

    def test_date_plus_zero_timedelta(self):
        # Adding zero days returns the same date
        d = date(2025, 6, 20)
        self.assertEqual(d + timedelta(0), d)

    def test_date_minus_date_returns_timedelta(self):
        # Subtracting one date from another date returns a timedelta
        d1, d2 = date(2025, 10, 24), date(2025, 10, 14)
        diff = d1 - d2
        self.assertIsInstance(diff, timedelta)
        self.assertEqual(diff, timedelta(days=10))

    def test_date_minus_itself_yields_zero(self):
        # Subtracting the same date should give a timedelta of zero
        d = date(2025, 7, 4)
        diff = d - d
        self.assertEqual(diff, timedelta(0))

    def test_leap_year_rollover(self):
        # 2024 is a leap year, so Feb 28 + 1 day = Feb 29
        self.assertEqual(date(2024, 2, 28) + timedelta(days=1), date(2024, 2, 29))
        # Adding 2 days moves into March 1
        self.assertEqual(date(2024, 2, 28) + timedelta(days=2), date(2024, 3, 1))

    def test_non_leap_year_rollover(self):
        # 2025 is not a leap year, so Feb 28 + 1 day = Mar 1
        self.assertEqual(date(2025, 2, 28) + timedelta(days=1), date(2025, 3, 1))

    def test_year_boundary_forward(self):
        # Adding days that cross from one year to the next
        d = date(2025, 12, 31)
        self.assertEqual(d + timedelta(days=1), date(2026, 1, 1))
        self.assertEqual(d + timedelta(days=5), date(2026, 1, 5))

    def test_year_boundary_backward(self):
        # Subtracting days that go back into the previous year
        d = date(2026, 1, 1)
        self.assertEqual(d - timedelta(days=1), date(2025, 12, 31))
        self.assertEqual(d - timedelta(days=10), date(2025, 12, 22))

    def test_month_boundary_various_months(self):
        # Make sure date math handles different month lengths
        # April to May below
        self.assertEqual(date(2025, 4, 30) + timedelta(days=1), date(2025, 5, 1))
        # January to February below
        self.assertEqual(date(2025, 1, 31) + timedelta(days=1), date(2025, 2, 1))
        # June to July below
        self.assertEqual(date(2025, 6, 30) + timedelta(days=1), date(2025, 7, 1))

    def test_large_timedelta_addition(self):
        # Add 1,000 days to Jan 1, 2025
        d = date(2025, 1, 1)
        result = d + timedelta(days=1000)
        self.assertEqual(result, date(2027, 9, 28))

    def test_large_timedelta_subtraction(self):
        # Subtract 1,000 days from Dec 31, 2025
        d = date(2025, 12, 31)
        result = d - timedelta(days=1000)
        self.assertEqual(result, date(2023, 4, 6))


if __name__ == "__main__":
    # verbosity=2 means you’ll see each test name and "ok" when it passes
    unittest.main(verbosity=2)
