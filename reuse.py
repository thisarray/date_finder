"""Find old calendars with the same configuration as the given year."""

import datetime
import unittest

EPOCH = 2000
"""Integer year of when to stop the search."""

def find_year(target):
    """Return a list of years with the same day of the week as target.

    Args:
        target: datetime.date object to match.
    Returns:
        List of integer years less than target and greater than or equal
        to EPOCH with the same day of the week as target.
    """
    if not isinstance(target, datetime.date):
        raise TypeError('target must be a datetime.date.')

    result = []
    year = target.year - 1
    while year >= EPOCH:
        date = datetime.date(year, target.month, target.day)
        if date.weekday() == target.weekday():
            result.append(year)
        year -= 1

    return result

class _UnitTest(unittest.TestCase):
    def test_find_year(self):
        """Test finding years with the same day of the week."""
        for value in [None, 42, '', []]:
            self.assertRaises(TypeError, find_year, value)
        self.assertEqual(find_year(datetime.date(2025, 1, 1)),
                         [2020, 2014, 2003])
        self.assertEqual(find_year(datetime.date(2025, 3, 1)),
                         [2014, 2008, 2003])

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'year', type=int, default=datetime.date.today().year,
        help='integer target year (defaults to %(default)s)')
    args = parser.parse_args()

    if args.year >= EPOCH:
        january_set = frozenset(find_year(datetime.date(args.year, 1, 1)))
        march_set = frozenset(find_year(datetime.date(args.year, 3, 1)))
        overlap = sorted(january_set.intersection(march_set), reverse=True)
        if len(overlap) > 0:
            for year in overlap:
                print('{} has the same configuration as {}.'.format(
                    year, args.year))
            print()

        print('{} can be formed through a combination of'.format(args.year))
        print(sorted(january_set), 'for January and February')
        print(sorted(march_set), 'for the rest of the year')
    else:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(_UnitTest)
        unittest.TextTestRunner(verbosity=2).run(suite)
