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
        self.assertEqual(input_base, dec_num.base())

    def test_constructor_2(self):
        """
        Base case: hexagonal number.
        """
        input_str="a.2bf"
        input_base = 16
        dec_num = DecimalNumber.from_string(input_str, input_base)
        result_str = str(dec_num)
        self.assertEqual(input_str, result_str)
        self.assertEqual(input_base, dec_num.base())

    def test_constructor_err_1(self):
        """
        Error case: wrong base.
        """
        input_str="1.2"
        input_base = 2
        with self.assertRaises(RuntimeError):
            DecimalNumber.from_string(input_str, input_base)

    def test_constructor_err_2(self):
        """
        Error case: two floating points (invalid syntax).
        """
        input_str="1.2.3"
        input_base = 10
        with self.assertRaises(ValueError):
            DecimalNumber.from_string(input_str, input_base)

    def test_constructor_err_3(self):
        """
        Error case: base not supported.
        """
        input_str="1.2"
        input_base = 40
        with self.assertRaises(NotImplementedError):
            DecimalNumber.from_string(input_str, input_base)

    def test_constructor_err_4(self):
        """
        Error case: base not possible.
        """
        input_str="1.2"
        input_base = 0
        with self.assertRaises(ValueError):
            DecimalNumber.from_string(input_str, input_base)
        

if __name__ == "__main__":
    unittest.main()