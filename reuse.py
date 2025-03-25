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
        and equal to EPOCH with the same day of the week as target.
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
        """Test finding a date with the same day of the week."""
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
        for target in [datetime.date(args.year, 1, 1),
                       datetime.date(args.year, 3, 1)]:
            matches = find_year(target)
            if len(matches) > 0:
                print('{} matched'.format(target.isoformat()))
                for match in matches:
                    print('\t{}'.format(match.isoformat()))
    else:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(_UnitTest)
        unittest.TextTestRunner(verbosity=2).run(suite)
