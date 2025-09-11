'''
Use unittest.TestCase methods to confirm that the addition and subtraction of date and
timedelta objects produce correct results

'''

from datetime import timedelta
import unittest


class TestAdd(unittest.TestCase):
    """
    Test the addition of date and timedelta objects
    """

    def test_add_days(self):
        """
        Test that the addition of days
        """
        result = timedelta(days=360) + timedelta(days=5)
        self.assertEqual(result, timedelta(days=365))

    def test_add_hours_days_rollover(self):
        """
        Test that the addition of days and hours
        """
        result = timedelta(days=2, hours=6) + timedelta(days=1, hours=20)
        self.assertEqual(result, timedelta(days=4, hours=2))

    def test_add_minutes_seconds_microseconds_rollover(self):
        """
        Test the addition of days, hours, minutes, seconds and microseconds
        """
        result = timedelta(days=2, hours=4, minutes=10, seconds=10, microseconds=10) + timedelta(days=1, hours=23,
                                                                                                 minutes=55, seconds=55,
                                                                                                 microseconds=55)
        self.assertEqual(result, timedelta(days=4, hours=4, minutes=6, seconds=5, microseconds=65))

    def test_add_negative_timedelta_rollover(self):
        """
        Test the addition of negative timedelta
        """
        result = timedelta(days=-3, hours=-14, minutes=-16, seconds=-18, microseconds=-10) + timedelta(days=2, hours=4,
                                                                                                       minutes=6,
                                                                                                       seconds=8,
                                                                                                       microseconds=1)
        self.assertEqual(result, timedelta(days=-2, hours=13, minutes=49, seconds=49, microseconds=999991))


class TestSubstract(unittest.TestCase):
    """
    Test the  subtractions of date and timedelta objects
    """

    def test_substract_days(self):
        """
        Test that the substraction of days
        """
        result = timedelta(days=365) - timedelta(days=5)
        self.assertEqual(result, timedelta(days=360))

    def test_substract_hours_negative_result_rollover(self):
        """
        Test that the substraction of days and hours with roll-over and negative result
        """
        result = timedelta(days=1, hours=6) - timedelta(days=2, hours=20)
        self.assertEqual(result, timedelta(days=-2, hours=10))

    def test_substract_minutes_seconds_microseconds_rollover(self):
        """
        Test the substraction of days, hours, minutes, seconds and microseconds with rollover
        """
        result = timedelta(days=2, hours=4, minutes=10, seconds=10, microseconds=10) - timedelta(days=1, hours=23,
                                                                                                 minutes=55, seconds=55,
                                                                                                 microseconds=55)
        self.assertEqual(result, timedelta(days=0, hours=4, minutes=14, seconds=14, microseconds=999955))

    def test_substract_negative_timedelta_rollover(self):
        """
        Test the addition of negative timedelta
        """
        result = timedelta(days=-3, hours=-4, minutes=-6, seconds=-8, microseconds=-1) - timedelta(days=2, hours=4,
                                                                                                   minutes=6, seconds=8,
                                                                                                   microseconds=1)
        self.assertEqual(result, timedelta(days=-6, hours=15, minutes=47, seconds=43, microseconds=999998))


if __name__ == '__main__':
    unittest.main()