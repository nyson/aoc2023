
from unittest import TestCase
from aoc2023 import day5

class TestRanges(TestCase):
    def test_union(self):
        self.assertEqual(
            range(3,5),
            day5.range_union(range(1,5), range(3,7)),
            "Can get range overlap")

    def test_prefix(self):
        self.assertEqual(
            range(1,5),
            day5.range_prefix(range(1,10), range(5,20)),
            "Can get range prefix")

        self.assertEqual(
            range(1,5),
            day5.range_prefix(range(1,5), range(100, 300)),
            "Can get range before second range"
        )

    def test_suffix(self):
        self.assertEqual(
            range(5,10),
            day5.range_suffix(range(1,10), range(2,5)),
            "Can get range suffix")

        self.assertEqual(
            range(234,255),
            day5.range_suffix(range(234,255), range(2,5)),
            "Can get range suffix after range")



class TestMapTransform(TestCase):
    pass