# coding=utf-8
"""
run the test from the sr/invesytoolbox directory:
python ../tests/test_data.py
"""

import sys
import unittest

sys.path.append(".")

from print_tools import \
    format_filesize, print_


class TestSystem(unittest.TestCase):
    def test_format_filesize(self):
        for prefix_type in ('binary', 'decimal'):
            for nb in (1, 40000, 23456, 34234234234):
                print(format_filesize(
                    nb,
                    prefix_type=prefix_type
                ))

    def test_print_(self):
        print_(
            'Das ist ein Test',
            'mit Ümläuten und Zeilenenden', '\n',
            'bla bla bla',
            color={2: 'red'},
            sep='#'
        )


if __name__ == '__main__':
    unittest.main()

    print('finished system tests.')
