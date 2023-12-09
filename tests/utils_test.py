from unittest import TestCase

from aoc2023.utils import minimize_ranges, range_overlaps, range_prefix, range_suffix, range_union


class TestRanges(TestCase):
    def test_minimize_ranges(self):
        self.assertEqual(
            [range(1,9)],
            list(minimize_ranges(range(1,3), range(2,9)))
        )

        self.assertEqual(
            [range(1,3), range(3,9)],
            list(minimize_ranges(range(1,3), range(3,9)))
        )

        self.assertEqual(
            [range(1,3), range(3,9)],
            list(minimize_ranges(range(1,3), range(5,9), range(3,9)))
        )

        self.assertEqual(
            [range(1,3), range(3,9)],
            list(minimize_ranges(range(1,3), range(3,9), range(5,9)))
        )

        self.assertEqual(
            [range(1,3), range(3,9)],
            list(minimize_ranges(range(3,9), range(5,9), range(1,3)))
        )

    def test_overlaps(self):
        self.assertTrue(
            range_overlaps(range(1,3), range(2,4)),
            "Can check if ranges overlap"
        )

        self.assertFalse(
            range_overlaps(range(1,3), range(3,4)),
            "No false positives"
        )

    def test_union(self):
        self.assertEqual(
            range(3,5),
            range_union(range(1,5), range(3,7)),
            "Can get range overlap")
        
    def test_no_overlap(self):
        self.assertEqual(
            None,
            range_union(range(79,93), range(98, 100)),
            "Should not overlap on non-overlappning ranges"
        )

    def test_prefix(self):
        self.assertEqual(
            range(1,5),
            range_prefix(range(1,10), range(5,20)),
            "Can get range prefix")

        self.assertEqual(
            range(1,5),
            range_prefix(range(1,5), range(100, 300)),
            "Can get range before second range"
        )

    def test_suffix(self):
        self.assertEqual(
            range(5,10),
            range_suffix(range(1,10), range(2,5)),
            "Can get range suffix")

        self.assertEqual(
            range(234,255),
            range_suffix(range(234,255), range(2,5)),
            "Can get range suffix after range")
