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

def compute_square_root(num_digits: int, k:float, base:int = 10) -> str:
    """
    Compute the first [num_digits] of sqrt(k),
    and return the result as a string.

    Arguments:
    * num_digits: amount of digits (precision) of the approximation 
        of sqrt(k) in the output string.
    * k: number whose sqrt(k) is to be approximated.
    * base: base of the number represented by the output string used.
        base=10 gives a normal number, base=2 a binary number,
        and base=16 a hexadecimal number.
        Valid values have 2 ≤ base ≤ 34.
        Digits representing the numbers 10, 11, ..., 34
        are represented by "a", "b", ..., "z" respectively.
        (Higher bases are not supported as there are 
        no more obvious alphabet symbols for it.
        This is just a lack of conventions, not a theoretical one.)
    """
    if base < 2 or base > 34:
        raise ValueError("Base must be an integer in [2, 34]")
    # Invariant: sum_{i=0}^{num_digits} d[i]*(10^-i) = cumsum
    cumsum = 0
    d = [0]*num_digits
    for i in range(0, num_digits):
        while ((cumsum + (d[i] + 1)* (base**(-i)))**2 <= k) and (d[i] < base-1):
            d[i] += 1
        cumsum += d[i] * (base**(-i))
    return f"{d[0]}." + "".join((str(x) for x in d[1:]))

