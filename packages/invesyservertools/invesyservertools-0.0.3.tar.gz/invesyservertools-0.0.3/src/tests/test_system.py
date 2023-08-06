# coding=utf-8
"""
run the test from the sr/invesytoolbox directory:
python ../tests/test_data.py
"""

import sys
import unittest

sys.path.append(".")

from system_tools import \
    get_username, find_file_path


class TestSystem(unittest.TestCase):
    def test_get_username(self):
        print(get_username())

    def test_find_file_path(self):
        print(find_file_path(
            filename='test_system.py',
            rootpath='~/Projekte/Python Packages',
            not_found='not found'
        ))
        print(find_file_path(
            filename='test_system.py',
            rootpath='~/Projekte/Python Packages',
            path_only=True,
            not_found='not found'
        ))
        print(find_file_path(
            filename='xtest_system.py',
            rootpath='~/Projekte/Python Packages',
            path_only=True
        ))
        print(find_file_path(
            filename='xtest_system.py',
            rootpath='~/Projekte/Python Packages',
            path_only=True,
            not_found='could not find anything in {rootpath}'
        ))


if __name__ == '__main__':
    unittest.main()

    print('finished system tests.')
