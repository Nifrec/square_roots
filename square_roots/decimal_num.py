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
from __future__ import annotations
import re

from square_roots.digit_to_string import DIGIT_TO_STRING, STRING_TO_DIGIT


class DecimalNumber:
    """
    Representation of decimal numbers with an arbitrary precision.
    Much slower and much more memory-hungry than build-in floats
    and longs. 
    However, DecimalNumber is completely free from rounding errors.
    """

    def __init__(self, base: int):
        """
        Arguments:
        * base: base of the number system used to represent the number.
            Base 10 would result in 'ordinary' numbers,
            base 2 in binary numbers, base 16 in hexadecimal numbers, etc.
        """
        self.__base = base

    def __add__(self, other: DecimalNumber | int):
        ...

    def __mul__(self, other: DecimalNumber | int):
        ...

    def shift(self, positions: int):
        ...

    def __setitem__(self, position: int, value: int):
        ...

    def check_valid_digit(self, d: int):
        """
        Check if 0 <= d < self.base.
        Raise an error otherwise.
        """
        ...

    @property
    def base(self) -> int:
        return self.__base

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    def __eq__(self, other: DecimalNumber | int) -> bool:
        raise NotImplementedError()

    def __geq__(self, other: DecimalNumber | int) -> bool:
        raise NotImplementedError()

    def __ge__(self, other: DecimalNumber | int) -> bool:
        raise NotImplementedError()

    def __leq__(self, other: DecimalNumber | int) -> bool:
        raise NotImplementedError()

    def __le__(self, other: DecimalNumber | int) -> bool:
        raise NotImplementedError()

    @staticmethod
    def from_string(str_repr: str, base: int) -> DecimalNumber:
        """
        Create a new DecimalNumber from a string.

        Arguments:
        * str_repr: string in the format "A.B", 
            where A and B can be any integer, and B may be omitted.

            In Context-Free Grammar notation:
            S -> I.D
            D -> 0|1|2|3|4|...|a|b|...|z|ε
            I -> 0D|1D|...|zD
            ("ε" is the empty character, "a" is the character representing 10
            as a single digit, "b" represents 11, etc.)
        * base: amount of different values that a single digit can have.
            Base 10 is 'normal' decimal notation, 2 is binary, 16 hexadecimal.
            This argument must satisfy 2 <= base <= 34
        """
        decimal_number_from_string(str_repr, base)
        DecimalNumber.__parse_string(str_repr)
    @staticmethod
    def __parse_string(str_repr):
        str_repr = str_repr.lower()
        if re.fullmatch(r"[0-9a-z]+\.[0-9a-z]*", str_repr) is None:
            raise ValueError("Invalid string representation.")


def decimal_number_from_string(str_repr: str, base: int) -> DecimalNumber:
    """
    Same as DecimalNumber.from_string().
    """
    __check_base_is_valid(str_repr, base)

def __check_base_is_valid(input_str: str, base: int):
    if base > 35:
        raise NotImplementedError("Unly bases up to 34 are supported, "
                                    "for notational-practical reasons")
    elif base < 2:
        raise ValueError("Invalid base, must be 2 or greater.")
    else:
        max_digit = __find_max_digit_in_str(input_str)
        if max_digit >= base:
            raise RuntimeError(
                "Input string uses greater base than specified base.")

def __find_max_digit_in_str(decimal_string: str) -> int:
    """
    Given an input string of the form "I.D" 
    (see DecimalNumber.from_string for the syntax convention),
    find the digit with the greatest value and return this value.
    """
    decimal_string = decimal_string.replace(".", "")
    return max (STRING_TO_DIGIT[digit] for digit in decimal_string)
        

