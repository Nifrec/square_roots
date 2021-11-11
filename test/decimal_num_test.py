"""
Copyright (C) 2021 Lulof Pirée, 

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from typing import Sequence, Tuple
import unittest
import warnings

from square_roots.decimal_num import DecimalNumber

warnings.warn("Testcases still allow a NotImplementedError\n"
              "when doing arithmetic between numbers of different bases.\n"
              "A method DecimalNumber.convert_base(to:int) would resolve this!")

warnings.warn("DecimalNumber comparisons with integers not yet implemented or tested.")


class DecimalNumberConstructorTestCase(unittest.TestCase):
    """
    Test class for infinite-precision numbers.

    This testcase focuses on the DecimalNumber.from_string() and .from_int() 
    static methods.
    """

    def test_constructor_1(self):
        """
        Base case: base-10 number with decimals
        """
        input_str = "101.03"
        input_base = 10
        dec_num = DecimalNumber.from_string(input_str, input_base)
        result_str = str(dec_num)
        self.assertEqual(input_str, result_str)
        self.assertEqual(input_base, dec_num.base)

    def test_constructor_2(self):
        """
        Base case: hexagonal number.
        """
        input_str = "a.2bf"
        input_base = 16
        dec_num = DecimalNumber.from_string(input_str, input_base)
        result_str = str(dec_num)
        self.assertEqual(input_str, result_str)
        self.assertEqual(input_base, dec_num.base)

    def test_constructor_3(self):
        """
        Base case: negative number.
        """
        input_str = "-1.02"
        input_base = 10
        dec_num = DecimalNumber.from_string(input_str, input_base)
        result_str = str(dec_num)
        self.assertEqual(input_str, result_str)
        self.assertEqual(input_base, dec_num.base)

    def test_constructor_int_1(self):
        """
        Base case: base-10 number.
        """
        input_int = 123
        input_base = 10
        expected = "123."
        dec_num = DecimalNumber.from_int(input_int, input_base)
        result_str = str(dec_num)
        self.assertEqual(expected, result_str)
        self.assertEqual(input_base, dec_num.base)

    def test_constructor_int_2(self):
        """
        Base case: hexadecimal number.
        """
        input_int = 123
        input_base = 16
        expected = "7b."
        dec_num = DecimalNumber.from_int(input_int, input_base)
        result_str = str(dec_num)
        self.assertEqual(expected, result_str)
        self.assertEqual(input_base, dec_num.base)

    def test_constructor_err_1(self):
        """
        Error case: wrong base.
        """
        input_str = "1.2"
        input_base = 2
        with self.assertRaises(RuntimeError):
            DecimalNumber.from_string(input_str, input_base)

    def test_constructor_err_2(self):
        """
        Error case: two floating points (invalid syntax).
        """
        input_str = "1.2.3"
        input_base = 10
        with self.assertRaises(ValueError):
            DecimalNumber.from_string(input_str, input_base)

    def test_constructor_err_3(self):
        """
        Error case: base not supported.
        """
        input_str = "1.2"
        input_base = 40
        with self.assertRaises(NotImplementedError):
            DecimalNumber.from_string(input_str, input_base)

    def test_constructor_err_4(self):
        """
        Error case: base not possible.
        """
        input_str = "1.2"
        input_base = 0
        with self.assertRaises(ValueError):
            DecimalNumber.from_string(input_str, input_base)

    def test_constructor_1_getter(self):
        """
        Base case: same as test_constructor_1,
        but now checking the result with getter methods.
        """
        input_str = "101.03"
        input_base = 10
        dec_num = DecimalNumber.from_string(input_str, input_base)
        self.assertEqual(dec_num[-2], 3)
        self.assertEqual(dec_num[-1], 0)
        self.assertEqual(dec_num[0], 1)
        self.assertEqual(dec_num[1], 0)
        self.assertEqual(dec_num[2], 1)
        self.assertEqual(input_base, dec_num.base)

    


class DecimalNumberStringTestCase(unittest.TestCase):
    """
    Test class for infinite-precision numbers.

    This testcase focuses on str() and repr() dunder methods.

    Also tests the __setitem__ method implicitly.
    """

    def test_str_1(self):
        """
        Base case: binary number.
        """
        decnum = DecimalNumber(2)
        decnum[0] = 1
        decnum[1] = 0
        decnum[2] = 1
        decnum[-1] = 0
        decnum[-2] = 1
        expected_str = "101.01"
        expected_repr = 'DecimalNumber.from_string("101.01")'

        self.assertEqual(str(decnum), expected_str)
        self.assertEqual(repr(decnum), expected_repr)

    def test_str_2(self):
        """
        Base case: hexadecimal number.
        Zeros are added implicitly.
        """
        decnum = DecimalNumber(16)
        decnum[5] = "a"
        decnum[1] = 0
        decnum[2] = "f"
        decnum[-1] = 0
        decnum[-2] = 1
        decnum[-3] = "d"
        expected_str = "a00f00.01d"
        expected_repr = 'DecimalNumber.from_string("a00f00.01d")'

        self.assertEqual(str(decnum), expected_str)
        self.assertEqual(repr(decnum), expected_repr)

    def test_str_3(self):
        """
        Base case: negative number.
        """
        decnum = DecimalNumber(10)
        decnum.set_sign(False)
        decnum[0] = 4
        decnum[1] = 3
        decnum[-1] = 3
        expected_str = "-34.3"
        expected_repr = 'DecimalNumber.from_string("-34.3")'

        self.assertEqual(str(decnum), expected_str)
        self.assertEqual(repr(decnum), expected_repr)


class DecimalNumberSignTestCase(unittest.TestCase):
    """
    Test class for infinite-precision numbers.

    This testcase focuses on polarity of a DecimalNumber.
    """

    def test_sign_constructor(self):
        decnum = DecimalNumber(10, sign=False)
        self.assertFalse(decnum.is_positive())
        self.assertTrue(decnum.is_negative())
        self.assertEqual(decnum.sign, -1)

        decnum = DecimalNumber(10, sign=True)
        self.assertFalse(decnum.is_negative())
        self.assertTrue(decnum.is_positive())
        self.assertEqual(decnum.sign, 1)

    def test_sign_setter_bool(self):
        decnum = DecimalNumber(10, sign=False)
        decnum.set_sign(True)
        self.assertTrue(decnum.is_positive())

    def test_sign_setter_int(self):
        decnum = DecimalNumber(10, sign=True)
        decnum.set_sign(-1)
        self.assertTrue(decnum.is_negative())


class DecimalNumberShiftTestCase(unittest.TestCase):
    """
    Test class for infinite-precision numbers.

    This testcase focuses 'shifting' a number:
    moving all digits one place left or right.
    This is equivalent to multiplying or dividing 
    over the used base respectively.
    """

    def check_shift(self, base: int, input_str: str,
                    expected_str: str, positions: int):
        decnum = DecimalNumber.from_string(input_str, base)
        decnum.shift(positions)
        result = str(decnum)
        self.assertEqual(expected_str, result)

    def test_shift_left_1(self):
        """
        Base case: decimal number, shift 1 position.
        """
        base = 10
        positions = 1
        input_str = "10.3"
        expected = "103."
        self.check_shift(base, input_str, expected, positions)

    def test_shift_left_2(self):
        """
        Base case: binary number, shift 3 positions.
        """
        base = 2
        positions = 3
        input_str = "1.01101"
        expected = "1011.01"
        self.check_shift(base, input_str, expected, positions)

    def test_shift_right_1(self):
        """
        Base case: hexadecimal number, shift -2 positions.
        """
        base = 16
        positions = -2
        input_str = "3fa.9de"
        expected = "3.fa9de"
        self.check_shift(base, input_str, expected, positions)


class DecimalNumberAddTestCase(unittest.TestCase):
    """
    Test class for infinite-precision numbers.

    This testcase focuses adding two numbers.
    """

    def check_add(self, base_1: int, num_1: str, base_2: int, num_2: str,
                  expected_str: str):
        decnum_1 = DecimalNumber.from_string(num_1, base_1)
        decnum_2 = DecimalNumber.from_string(num_2, base_2)
        result = str(decnum_1 + decnum_2)
        self.assertEqual(expected_str, result)

    def test_add_decimal_1(self):
        """
        Base case: 1.34 + 98.01 = 99.35
        """
        base_1 = 10
        num_1 = "1.34"
        base_2 = 10
        num_2 = "98.01"
        expected = "99.35"
        self.check_add(base_1, num_1, base_2, num_2, expected)

    def test_add_decimal_2(self):
        """
        Corner case: one number is negative 1.34 + (-98.01) = -96.67
        """
        base_1 = 10
        num_1 = "1.34"
        base_2 = 10
        num_2 = "-98.01"
        expected = "-96.67"
        self.check_add(base_1, num_1, base_2, num_2, expected)

    def test_add_decimal_3(self):
        """
        Corner case: both numbers are negative (-1.23) + (-32.11) = -33.34
        """
        base_1 = 10
        num_1 = "-1.23"
        base_2 = 10
        num_2 = "-32.11"
        expected = "-33.34"
        self.check_add(base_1, num_1, base_2, num_2, expected)

    def test_add_binary_1(self):
        """
        Base case: 1.0101bin + 0.01bin = 1.3125dec + 0.25dec 
            = 2.5625dec = 1.1001bin
        """
        base_1 = 2
        num_1 = "1.0101"
        base_2 = 2
        num_2 = "0.01"
        expected = "1.1001"
        self.check_add(base_1, num_1, base_2, num_2, expected)

    def test_add_binary_2(self):
        """
        Corner case: one number is negative 
            1.0101bin +(-0.1bin) 
            = 1.3125dec -0.5dec
            = 0.8125dec
            = 0.1101bin
        """
        base_1 = 2
        num_1 = "1.0101"
        base_2 = 2
        num_2 = "-0.1"
        expected = "0.1101"
        self.check_add(base_1, num_1, base_2, num_2, expected)

    def test_add_binary_2(self):
        """
        Corner case: one number is negative, result is also negative
            0.0101bin +(-0.1bin) 
            = 0.3125dec -0.5dec
            = -0.8125dec
            = -0.0011bin
        """
        base_1 = 2
        num_1 = "0.0101"
        base_2 = 2
        num_2 = "-0.1"
        expected = "-0.0011"
        self.check_add(base_1, num_1, base_2, num_2, expected)

    def test_add_mixed_bases(self):
        decnum_1 = DecimalNumber.from_string("1.5", base=10)
        decnum_2 = DecimalNumber.from_string("1.5", base=16)

        with self.assertRaises(NotImplementedError):
            decnum_1 + decnum_2

    def test_add_returns_copy(self):
        """
        Corner case: addings two DecimalNumbers should return a fresh
        object, and not modify one of the old objects.
        """
        base_1 = 10
        num_1 = "1.34"
        base_2 = 10
        num_2 = "98.01"
        decnum_1 = DecimalNumber.from_string(num_1, base_1)
        decnum_2 = DecimalNumber.from_string(num_2, base_2)
        decnum_3 = decnum_1 + decnum_2

        self.assertIsNot(decnum_3, decnum_1)
        self.assertIsNot(decnum_3, decnum_2)
        # The following would only fail in case of an extremely weird bug.
        # Still, it is important!
        self.assertIsNot(decnum_1, decnum_2)

    def test_add_int(self):
        """
        corner case: add an integer to a hexadecimal number.
        """
        base = 16
        decnum = DecimalNumber.from_string("1f.2b", base)
        result = str(decnum + 10)
        expected = "29.2b"
        self.assertEqual(result, expected)

    def test_sub_from_digit_1(self):
        """
        Testcase used to debug test_add_decimal_2.
        """
        base_1 = 10
        num_1 = "-98.01"
        decnum = DecimalNumber.from_string(num_1, base_1)
        # Number "1.34" already decomposed in (pos, value) pairs:
        pos_val_pairs_to_subtract = ((0, 1), (-1, 3), (-2, 4))
        expected_intermediates = ("-97.01", "-96.71", "-96.67")
        for ((pos, value), expected) in zip(pos_val_pairs_to_subtract, expected_intermediates):
            decnum._subtract_from_digit(pos, value)
            self.assertEqual(str(decnum), expected)


class DecimalNumberIterTestCase(unittest.TestCase):
    """
    Test class for infinite-precision numbers.

    This testcase focuses on the DecimalNumber.__iter__() method.
    This method should return all (position, digit-value) pairs in
    descending order (sorted on position).
    """

    def check_iter(self, base: int, input_str: int,
                   expected: Sequence[Tuple[int, int]]):
        decnum = DecimalNumber.from_string(input_str, base)

        for actual, expected in zip(iter(decnum), expected):
            self.assertTupleEqual(actual, expected)

    def test_iter_1(self):
        """
        Base case: decimal number.
        """
        base = 10
        input_str = "4321.1234"
        expected = ((3, 4), (2, 3), (1, 2), (0, 1),
                    (-1, 1), (-2, 2), (-3, 3), (-4, 4))
        self.check_iter(base, input_str, expected)

    def test_iter_2(self):
        """
        Corner case: hexadecimal number.
        Should return integers, not characters such as "a" and "f".
        """
        base = 16
        input_str = "2af5.b"
        expected = ((3, 2), (2, 10), (1, 15), (0, 5), (-1, 11))
        self.check_iter(base, input_str, expected)

    def test_iter_3(self):
        """
        Corner case: leading, tailing and intermediate 0's should be ignored.
        """
        base = 10
        input_str = "010.30"
        expected = ((1, 1), (-1, 3))
        self.check_iter(base, input_str, expected)

class DecimalNumberComparisonTestCase(unittest.TestCase):
    """
    Test class for infinite-precision numbers.

    These testcases test ==, <=, >=, >, <.
    """
    def test_lt(self):
        base = 10

        num_1 = DecimalNumber.from_string("-12.34", base)
        num_2 = DecimalNumber.from_string("23.45", base)
        num_3 = DecimalNumber.from_string("100.003", base)

        self.assertTrue(num_1 < num_2)
        self.assertFalse(num_2 < num_1)
        self.assertTrue(num_1 < num_3)
        self.assertFalse(num_3 < num_1)
        self.assertTrue(num_2 < num_3)
        self.assertFalse(num_3 < num_2)

        self.assertFalse(num_1 < num_1)
        self.assertFalse(num_2 < num_2)

    def test_gt(self):
        base = 16

        num_1 = DecimalNumber.from_string("-a.3e", base)
        num_2 = DecimalNumber.from_string("-d.45", base)
        num_3 = DecimalNumber.from_string("100.003", base)
        num_4 = DecimalNumber.from_string("-a.3e0001", base)

        self.assertTrue(num_1 > num_2)
        self.assertFalse(num_2 > num_1)
        self.assertTrue(num_3 > num_1)
        self.assertFalse(num_1 > num_3)
        self.assertTrue(num_3 > num_2)
        self.assertFalse(num_2 > num_3)

        self.assertTrue(num_1 > num_4)
        self.assertFalse(num_4 > num_1)

        self.assertFalse(num_1 > num_1)
        self.assertFalse(num_3 > num_3)

    def test_eq(self):
        base = 2

        num_1 = DecimalNumber.from_string("111.01", base)
        num_2 = DecimalNumber.from_string("111.10", base)
        num_3 = DecimalNumber.from_string("101.01", base)

        self.assertTrue(num_1 == num_1)
        self.assertFalse(num_2 == num_1)
        self.assertTrue(num_3 == num_3)
        self.assertFalse(num_1 == num_3)
        self.assertTrue(num_2 == num_2)
        self.assertFalse(num_2 == num_3)

    def test_leq(self):
        base = 2

        num_1 = DecimalNumber.from_string("111.01", base)
        num_2 = DecimalNumber.from_string("111.10", base)

        self.assertTrue(num_1 <= num_2)
        self.assertTrue(num_1 <= num_1)
        self.assertFalse(num_2 <= num_1)

    def test_geq(self):
        base = 2

        num_1 = DecimalNumber.from_string("111.01", base)
        num_2 = DecimalNumber.from_string("111.10", base)

        self.assertFalse(num_1 >= num_2)
        self.assertTrue(num_1 >= num_1)
        self.assertTrue(num_2 >= num_1)

    def test_zeros(self):
        """
        Corner case: 0. == -0.
        """
        base = 10
        num_1 = DecimalNumber.from_string("0.", base)
        num_2 = DecimalNumber.from_string("-0.", base)

        self.assertFalse(num_1 > num_2)
        self.assertFalse(num_1 < num_2)
        self.assertTrue(num_1 == num_2)



if __name__ == "__main__":
    unittest.main()
