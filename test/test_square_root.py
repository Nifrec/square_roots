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

from square_roots.compute_square_root import compute_square_root

class ComputeSquareRootTestCase(unittest.TestCase):
    """
    Test numerical computation of square roots of various numbers.
    """


    def run_test(self, num_digits:int, k:int, expected:str, base:int=10):
        result = compute_square_root(num_digits, k, base)
        self.assertEqual(expected, result)

    def test_single_digit_dec(self):
        """
        Base case: the first digit of the decimal representation 
        of sqrt(2) is 1.
        """
        self.run_test(num_digits=1, k=2, expected="1.")

    def test_three_digit_dec(self):
        """
        Base case: the first three digits of the decimal representation 
        of sqrt(2) are '1.41'.
        """
        self.run_test(num_digits=3, k=2, expected="1.41")

    def test_eleven_digit_dec(self):
        """
        Base case: the first eleven digits of the decimal representation 
        of sqrt(2) are '1.4142135623'.
        """
        self.run_test(num_digits=11, k=2, expected="1.4142135623")

    def test_sqrt_9(self):
        """
        Base case: the first 15 digits of the decimal representation 
        of sqrt(9) are '3.0000...'.
        """
        self.run_test(num_digits=15, k=9, expected="3." + "0"*14)

    def test_single_digit_bin(self):
        """
        Base case: the first digit of the binary representation 
        of sqrt(2) is 1.
        """
        self.run_test(num_digits=1, k=2, base=2, expected="1.")

    def test_single_digit_hex(self):
        """
        Base case: the first digit of the hexadecimal representation 
        of sqrt(2) is 1.
        """
        self.run_test(num_digits=1, k=2, base=16, expected="1.")

    def test_six_digits_binary(self):
        """
        Base case: the first digit of the binary representation 
        of sqrt(2) are 1.01101.
        """
        self.run_test(num_digits=6, k=2, base=2, expected="1.01101")
if __name__ == "__main__":
    unittest.main()
