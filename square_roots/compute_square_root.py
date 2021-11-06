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

DIGIT_TO_STRING = {x:str(x) for x in range(0, 11)}
ALPHABET = {chr(x) for x in range(ord("a"), ord("z")+1)}
HEX_OFFSET = ord("a") - 10
DIGIT_TO_STRING.update({ord(x) - HEX_OFFSET:x for x in ALPHABET})
print(DIGIT_TO_STRING)

def compute_square_root(num_digits: int, base=10) -> str:
    """
    Compute the first [num_digits] of sqrt(2),
    and return the result as a string.

    Arguments:
    * num_digits: amount of digits (precision) of the approximation 
        of sqrt(2) in the output string.
    * base: base of the number represented by the output string used.
        base=10 gives a normal number, base=2 a binary number,
        and base=16 a hexadecimal number.
        Valid values have 2 ≤ base ≤ 34.
        Digits representing the numbers 10, 11, ..., 34
        are represented by "a", "b", ..., "z" respectively.
    """
    if base != 10:
        raise NotImplementedError("Only base 10 supported at the moment")
    cumprod = 1
    digits = [None]*(num_digits-1)
    for power in range(-1, -num_digits, -1):
        for digit in range(9, -1, -1):
            potential_new_cumprod = cumprod *((1 + 10**power * digit)**2)
            if (potential_new_cumprod) <= 2:
                digits[1-power] = digit
                cumprod = potential_new_cumprod
                break
    return "1." + "".join(str(x) for x in digits)

