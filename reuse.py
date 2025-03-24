"""Find old calendars with the same configuration as the given year."""

import datetime
import unittest

YEAR_LIMIT = 2000

def find_year(target):
    """Return a datetime.date object with the same day of the week as target.

    Args:
        target: datetime.date object to match.
    Returns:
        datetime.date object with the same day of the week as target.
    """
    if not isinstance(target, datetime.date):
        raise TypeError('target must be a datetime.date.')

    year = target.year - 1
    while year > YEAR_LIMIT:
        date = datetime.date(year, target.month, target.day)
        if date.weekday() == target.weekday():
            return date
        year -= 1

    return None

class _UnitTest(unittest.TestCase):
    def test_find_year(self):
        """Test finding a date with the same day of the week."""
        for value in [None, 42, '', []]:
            self.assertRaises(TypeError, find_year, value)
        self.assertEqual(find_year(datetime.date(2025, 1, 1)),
                         datetime.date(2020, 1, 1))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'year', type=int, default=datetime.date.today().year,
        help='integer target year (defaults to %(default)s)')
    args = parser.parse_args()

    if args.year > YEAR_LIMIT:
        for target in [datetime.date(args.year, 1, 1),
                       datetime.date(args.year, 3, 1)]:
            match = find_year(target)
            if isinstance(match, datetime.date):
                print('{} matched {}'.format(target.isoformat(), match.isoformat()))
    else:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(_UnitTest)
        unittest.TextTestRunner(verbosity=2).run(suite)
