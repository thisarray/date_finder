"""Find old calendars with the same configuration as the given year."""

import datetime
import unittest

EPOCH = 2000
"""Integer year of when to stop the search."""

def find_year(target):
    """Return a list of dates with the same day of the week as target.

    Args:
        target: datetime.date object to match.
    Returns:
        List of datetime.date objects in years less than target and greater
        than or equal to EPOCH with the same day of the week as target.
    """
    if not isinstance(target, datetime.date):
        raise TypeError('target must be a datetime.date.')

    result = []
    year = target.year - 1
    while year >= EPOCH:
        date = datetime.date(year, target.month, target.day)
        if date.weekday() == target.weekday():
            result.append(date)
        year -= 1

    return result

class _UnitTest(unittest.TestCase):
    def test_find_year(self):
        """Test finding dates with the same day of the week."""
        for value in [None, 42, '', []]:
            self.assertRaises(TypeError, find_year, value)
        self.assertEqual(find_year(datetime.date(2025, 1, 1)),
                         [datetime.date(2020, 1, 1),
                          datetime.date(2014, 1, 1),
                          datetime.date(2003, 1, 1)])
        self.assertEqual(find_year(datetime.date(2025, 3, 1)),
                         [datetime.date(2014, 3, 1),
                          datetime.date(2008, 3, 1),
                          datetime.date(2003, 3, 1)])

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'year', type=int, default=datetime.date.today().year,
        help='integer target year (defaults to %(default)s)')
    args = parser.parse_args()

    if args.year >= EPOCH:
        january_set = frozenset(
            date.year for date in find_year(datetime.date(args.year, 1, 1)))
        march_set = frozenset(
            date.year for date in find_year(datetime.date(args.year, 3, 1)))
        for year in sorted(january_set.intersection(march_set), reverse=True):
            print('{} has the same configuration as {}.'.format(
                year, args.year))
    else:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(_UnitTest)
        unittest.TextTestRunner(verbosity=2).run(suite)
