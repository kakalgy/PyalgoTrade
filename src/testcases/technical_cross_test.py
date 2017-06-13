# coding=utf-8
'''
Created on 2017年6月12日

@author: Administrator
'''

from pyalgotrade.technical import cross



class HelpersTestCase(common.TestCase):
    def test_get_stripped_left(self):
        v1, v2 = cross._get_stripped([1, 2, 3], [1], True)
        self.assertEqual(v1, [1])
        self.assertEqual(v2, [1])

        v1, v2 = cross._get_stripped([1], [1, 2, 3], True)
        self.assertEqual(v1, [1])
        self.assertEqual(v2, [1])

        v1, v2 = cross._get_stripped([1, 2, 3], [1, 2], True)
        self.assertEqual(v1, [1, 2])
        self.assertEqual(v2, [1, 2])

        v1, v2 = cross._get_stripped([1, 2], [1, 2, 3], True)
        self.assertEqual(v1, [1, 2])
        self.assertEqual(v2, [1, 2])

    def test_get_stripped_right(self):
        v1, v2 = cross._get_stripped([1, 2, 3], [1], False)
        self.assertEqual(v1, [3])
        self.assertEqual(v2, [1])

        v1, v2 = cross._get_stripped([1], [1, 2, 3], False)
        self.assertEqual(v1, [1])
        self.assertEqual(v2, [3])

        v1, v2 = cross._get_stripped([1, 2, 3], [1, 2], False)
        self.assertEqual(v1, [2, 3])
        self.assertEqual(v2, [1, 2])

        v1, v2 = cross._get_stripped([1, 2], [1, 2, 3], False)
        self.assertEqual(v1, [1, 2])
        self.assertEqual(v2, [2, 3])

    def test_compute_diff(self):
        self.assertEqual(cross.compute_diff([1, 1, 1], [0, 1, 2]), [1, 0, -1])
        self.assertEqual(cross.compute_diff([0, 1, 2], [1, 1, 1]), [-1, 0, 1])