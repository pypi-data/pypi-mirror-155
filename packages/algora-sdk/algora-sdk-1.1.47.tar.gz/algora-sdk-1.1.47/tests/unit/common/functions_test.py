import unittest
from dataclasses import dataclass
from datetime import date
from typing import Optional
import pandas as pd
from pandas._testing import assert_frame_equal

from algoralabs.common.functions import (
    coalesce, coalesce_callables, dataclass_to_dict, no_transform, to_pandas_with_index, transform_one_or_many,
    date_to_timestamp
)


class FunctionsTest(unittest.TestCase):
    def test_date_to_timestamp(self):
        self.assertEquals(date_to_timestamp(date(2022, 1, 1)), 1640995200000)

    def test_coalesce(self):
        self.assertEqual(coalesce(None, 1, 2), 1)
        self.assertEqual(coalesce(None, 0, 2), 0)
        self.assertEqual(coalesce(None, None, 2), 2)
        self.assertEqual(coalesce(1, 2, 3), 1)

    def test_coalesce_callables(self):
        dummy = lambda: None
        self.assertEqual(coalesce_callables(dummy, lambda: 1), 1)
        self.assertEqual(coalesce_callables(dummy, dummy), None)
        self.assertEqual(coalesce_callables(dummy, lambda: 0), 0)
        self.assertEqual(coalesce_callables(dummy, dummy, 0), 0)
        self.assertEqual(coalesce_callables(dummy, dummy, lambda: 2), 2)

    def test_dataclass_to_dict(self):
        @dataclass
        class Foo:
            x: int
            y: int
            z: Optional[int] = None
            score: Optional[float] = None

        f1 = Foo(1, 2)
        d1 = {
            "x": 1,
            "y": 2,
            "z": None,
            "score": None
        }
        d1_clean = {"x": 1, "y": 2}

        f2 = Foo(3, 0, 4, 2.79)
        d2 = {
            "x": 3,
            "y": 0,
            "z": 4,
            "score": 2.79
        }

        self.assertDictEqual(dataclass_to_dict(f1, remove_none=False), d1)
        self.assertDictEqual(dataclass_to_dict(f1, remove_none=True), d1_clean)
        self.assertDictEqual(dataclass_to_dict(f2, remove_none=False), d2)
        self.assertDictEqual(dataclass_to_dict(f2, remove_none=True), d2)

    def test_no_transform(self):
        d = {"x": 1, "y": 1}
        self.assertDictEqual(no_transform(d), d)

    @staticmethod
    def test_to_pandas_with_index():
        data = {
            "idx": [0, 1, 2],
            "x": ['a', 'b', 'c'],
            "y": [10, 20, 30]
        }
        expected = pd.DataFrame(data).set_index('idx', drop=True)
        result = to_pandas_with_index(data, index='idx')
        assert_frame_equal(expected, result)

    def test_transform_one_or_many(self):
        pass
