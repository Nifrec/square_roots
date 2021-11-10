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

import unittest

from square_roots.decimal_num import DecimalNumber


class DecimalNumberConstructorTestCase(unittest.TestCase):
    """
    Test class for infinite-precision numbers.

    This testcase focuses on the DecimalNumber.from_string() static method.
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




if __name__ == "__main__":
    unittest.main()
