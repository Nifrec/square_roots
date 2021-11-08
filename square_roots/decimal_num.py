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

    def __init__(self, base: int, sign: bool | int = 1):
        """
        Arguments:
        * base: base of the number system used to represent the number.
            Base 10 would result in 'ordinary' numbers,
            base 2 in binary numbers, base 16 in hexadecimal numbers, etc.
        * sign: polarity of the DecimalNumber. Nonnegative ints and True
            set the sign to positive,
            negative ints and False set the sign to negative.
        """
        self.__base = base
        self.set_sign(sign)

    @property
    def sign(self) -> int:
        if self.__is_positive:
            return 1
        else:
            return -1

    def is_positive(self) -> bool:
        return self.__is_positive

    def is_negative(self) -> bool:
        return not self.__is_positive

    def set_sign(self, sign: int | bool):
        """
        Set the sign of the number.

        Arguments:
        * sign: if sign is a negative int or the bool False, 
            the sign is net to negative.
            For a nonnegative int or the bool True,
            the sign is set to positive.
        """
        if type(sign) is int:
            self.__is_positive = sign >= 0
        elif type(sign) is bool:
            self.__is_positive = sign
        else:
            raise ValueError("Sign must be an int or a bool.")

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
        str_repr = str_repr.lower()
        DecimalNumber.__check_valid_string_repr(str_repr)

        result = DecimalNumber(base)
        integer_part, decimal_part = str_repr.split(".")
        integer_part = reversed(integer_part)
        integer_part = tuple(map(lambda x: STRING_TO_DIGIT[x], integer_part))
        decimal_part = tuple(map(lambda x: STRING_TO_DIGIT[x], decimal_part))

        for i in range(len(integer_part)):
            result[i] = integer_part[i]
        
        i = -1
        for digit in decimal_part:
            result[i] = digit
            i += 1
        
        return result

    @staticmethod
    def __check_valid_string_repr(str_repr):
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
        

