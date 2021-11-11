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
from typing import Any, Iterator, Tuple
import math
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
        # Dictionary mapping indices to digit values.
        # Conventions:
        # * Index 0 is the first integer digit, and -1 the first decimal digit.
        # * Digits with value 0 are not explicitly stored in self.__digits.
        self.__digits = dict()

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

    def copy(self) -> DecimalNumber:
        """
        Create a new DecimalNumber instance identical to self.
        """
        result = DecimalNumber(self.base, self.sign)
        for pos, digit_value in self:
            result[pos] = digit_value
        return result

    def __iter__(self) -> Iterator[Tuple[int, int]]:
        """
        Return all (position, digit-value) pairs of this DecimalNumber.
        Sort the output in descending order by position.
        The greatest position is that of the most significant digit,
        and the least position is that of the least significant digit.
        Do not return any pair where the digit value is 0.
        """
        pairs = tuple((pos, digit_value) for pos, digit_value
                      in sorted(self.__digits.items(), key=lambda x: x[0],
                                reverse=True))
        return iter(pairs)

    def __add__(self, other: DecimalNumber | int) -> DecimalNumber:
        if isinstance(other, int):
            other = DecimalNumber.from_int(other, self.base)
        return add_decimal_numbers(self, other)
        # result = self.copy()
        # result.add(other)
        # return result

    # def add(self, other: DecimalNumber | int):
    #     """
    #     Add another number to self in-place.

    #     Arguments:
    #         * other: decimal number to add to self.
    #             Alternatively, also an integer can be given.
    #     """
    #
    #     self.__raise_error_if_different_bases(other)
    #     if other.sign != self.sign:
    #         raise NotImplementedError()
    #     for (pos, digit_value) in other:
    #         self._add_to_digit(pos, digit_value)

    def _add_to_digit(self, pos: int, value: int):
        """
        Add [value] amount to the digit at position [pos].
        E.g. adding value 3 at pos 4 in base=10 means adding 3000.
        [value] may exceed self.base,
        and self[pos]+value may also exceed self.base:
        in either case, self[pos] is trimmed in the range [0, self.base)
        and the remaining carry digits are recursively 
        added to higher positions.
        """
        assert value >= 0

        if value > 0:
            carry_digits = (self[pos] + value)//self.base
            self[pos] = (self[pos] + value) % self.base
            if carry_digits > 0:
                self._add_to_digit(pos+1, carry_digits)

    def _subtract_from_digit(self, pos: int, value: int):
        """
        Subtract [value] amount from digit at position [pos].
        If [value] > self[pos], recursively subtract borrows from higher
        positions.
        Raise an error if need to borrow and pos is the most significant digit.
        """
        assert value >= 0

        if pos >= self.get_most_significant_pos() and value > self[pos]:
            raise RuntimeError("Cannot subtract from position: "
                               "unable to borrow sufficient "
                               "from higher positions.")

        if value > self[pos]:
            # First pay as much dept as we can.
            value -= self[pos]
            self[pos] = 0
            print(f"Unaffordable dept: {value}, pos: {pos}")
            # Borrow remaining dept from higher positions.
            borrows = math.ceil(value/self.base)
            print(
                f"Amount borrows: {borrows}, borrowed value: {borrows * self.base}")
            self[pos] = borrows * self.base - value
            self._subtract_from_digit(pos+1, borrows)

        else:
            self[pos] -= value

    def get_most_significant_pos(self) -> int:
        """
        Return the position of the most significant digit.
        0 is the position of first digit left of the float point,
        1 the second, etc.

        Return 0 if this number is (plus or minus) 0 (without any other digit).
        """
        if len(self.__digits.keys()) == 0:
            return 0
        else:
            return max(self.__digits.keys())

    def get_lest_significant_pos(self) -> int:
        """
        Return the position of the least significant digit.
        0 is the position of first digit left of the float point,
        -1 the first decimal digit, -2 the second decimal digit, etc.

        Return 0 if this number is (plus or minus) 0 (without any other digit).
        """
        if len(self.__digits.keys()) == 0:
            return 0
        else:
            return min(self.__digits.keys())

    def get_most_significant_digit(self) -> int:
        return self[self.get_most_significant_pos()]

    def __sub__(self, other: DecimalNumber | int):
        raise NotImplementedError()

    def __mul__(self, other: DecimalNumber | int):
        raise NotImplementedError()

    def __truediv__(self, other: DecimalNumber | int):
        raise NotImplementedError()

    def __raise_error_if_incompatible_num(self, other: Any):
        """
        Raise an error if other is not a DecimalNumber or if other
        has a different base than self.base.
        """
        if not isinstance(other, DecimalNumber):
            raise NotImplementedError("This arithmetric operation is currently "
                                      "only supported between "
                                      "two DecimalNumbers.")
        elif other.base != self.base:
            raise NotImplementedError("Arithmetic between numbers of "
                                      "different bases not (yet) supported.")

    def shift(self, positions: int):
        if positions == 0:
            return
        old_digits = self.__digits.copy()
        self.__digits = {old_pos + positions: self.__digits[old_pos]
                         for old_pos in old_digits.keys()}

    def __int__(self) -> int:
        raise NotImplementedError()

    def __round__(self, ndigits: int) -> float:
        raise NotImplementedError()

    def __float__(self) -> float:
        raise NotImplementedError()

    def __setitem__(self, position: int, value: int | str):
        """
        Set an individual digit of the decimal number.

        Arguments:
        * position: index of digit to set. Index 0 is the first integer digit,
            index 1 the second integer digit, -1 the first decimal digit, etc.
        * value: value to assign to the digit. Can be an integer in [0, 9]
            Or a string in [0-9a-zA-Z]
        """
        self.__raise_error_if_value_negative(value)

        if isinstance(value, str):
            value = value.lower()
            value = STRING_TO_DIGIT[value]

        self.__check_valid_digit(value)
        if value != 0:
            self.__digits[position] = value
        elif position in self.__digits.keys():
            del self.__digits[position]

    def __raise_error_if_value_negative(self, value: int | str):
        if ((isinstance(value, int) and value < 0)
                or (isinstance(value, str) and value[0] == "-")):
            raise ValueError("Can only set positive digit values.\n"
                             "To change the polarity, "
                             "use DecimalNumber.set_sign()")

    def __check_valid_digit(self, d: int):
        """
        Check if d < self.base.
        Raise an error otherwise.
        """
        if d < 0:
            raise RuntimeError(
                f"Digit value exceeds maximum digit value in base {self.base}")

    def __getitem__(self, position: int) -> int:
        if not type(position) == int:
            raise IndexError(
                "DecimalNumbers can only be indexed with integers")
        elif position in self.__digits.keys():
            return self.__digits[position]
        else:
            # Zero-digits are not explicitly stored in self.__digits
            return 0

    @property
    def base(self) -> int:
        return self.__base

    def __str__(self) -> str:
        digit_positions = self.__digits.keys()
        if len(digit_positions) == 0:
            return "0."
        most_significant_pos = max(digit_positions)
        least_significant_pos = min(digit_positions)

        if most_significant_pos < 0:
            integer_part = ["0"]
        else:
            integer_part = ["0"]*(most_significant_pos+1)
            for pos in range(most_significant_pos+1):
                if pos in digit_positions:
                    integer_part[most_significant_pos -
                                 pos] = DIGIT_TO_STRING[self.__digits[pos]]

        decimal_part = [""]
        if least_significant_pos < 0:
            decimal_part = ["0"]*abs(least_significant_pos)
            for pos in range(-1, least_significant_pos - 1, -1):
                if pos in digit_positions:
                    decimal_part[-1 -
                                 pos] = DIGIT_TO_STRING[self.__digits[pos]]

        result = "-"*(not self.__is_positive)
        result += "".join(integer_part) + "." + "".join(decimal_part)
        return result

    def __repr__(self) -> str:
        return f'DecimalNumber.from_string("{str(self)}")'

    def __eq__(self, other: DecimalNumber) -> bool:
        max_pos = max(self.get_most_significant_pos(),
                          other.get_most_significant_pos())
        min_pos = min(self.get_lest_significant_pos(),
                        other.get_lest_significant_pos())

        if other.base != self.base:
            return False
        # If both are simply "0.", then the sign doesn't matter.
        elif max_pos == 0 and min_pos == 0 and self[0] == 0 and other[0] == 0:
            return True
        elif self.sign != other.sign:
            return False
        else:
            
            for pos in range(max_pos, min_pos-1, -1):
                if self[pos] != other[pos]:
                    return False
            return True
    def __ge__(self, other: DecimalNumber) -> bool:
        self.__raise_error_if_incompatible_num(other)
        return (self == other) | (self > other)

    def __gt__(self, other: DecimalNumber) -> bool:
        self.__raise_error_if_incompatible_num(other)
        if self == other:
            return False
        elif self.sign > other.sign:
            return True
        elif self.sign < other.sign:
            return False
        else:
            # If both are negative, 
            # then the number with the smallest magnitude is the greatest
            bigger_mag_is_biggest = self.sign > 0
            max_pos = max(self.get_most_significant_pos(),
                          other.get_most_significant_pos())
            min_pos = min(self.get_lest_significant_pos(),
                          other.get_lest_significant_pos())
            for pos in range(max_pos, min_pos-1, -1):
                if self[pos] > other[pos]:
                    return bigger_mag_is_biggest
                if self[pos] < other[pos]:
                    return not bigger_mag_is_biggest
            return not bigger_mag_is_biggest

    def __le__(self, other: DecimalNumber) -> bool:
        self.__raise_error_if_incompatible_num(other)
        return (other >= self)

    def __lt__(self, other: DecimalNumber) -> bool:
        self.__raise_error_if_incompatible_num(other)
        return (other > self)

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
        return _decimal_number_from_string(str_repr, base)

    @staticmethod
    def from_int(int_value: int, base: int) -> DecimalNumber:
        """
        Construct a DecimalNumber from an integer with the given base.
        Arguments:
        * int_value: value of the decimal number.
            E.g. int_value = 123 (base 10) 
            would result in the DecimalNumber "123."
        * base: amount of different values that a single digit can have.
            Base 10 is 'normal' decimal notation, 2 is binary, 16 hexadecimal.
            This argument must satisfy 2 <= base <= 34
        """
        result = DecimalNumber(base, int_value >= 0)
        result._add_to_digit(0, abs(int_value))
        return result


def _decimal_number_from_string(str_repr: str, base: int) -> DecimalNumber:
    """
    Same as DecimalNumber.from_string().
    """
    __check_base_is_valid(str_repr, base)
    str_repr = str_repr.lower()
    __check_valid_string_repr(str_repr)

    result = DecimalNumber(base)
    if str_repr[0] == "-":
        result.set_sign(-1)
        str_repr = str_repr[1:]
    integer_part, decimal_part = str_repr.split(".")
    integer_part = reversed(integer_part)
    integer_part = tuple(map(lambda x: STRING_TO_DIGIT[x], integer_part))
    decimal_part = tuple(map(lambda x: STRING_TO_DIGIT[x], decimal_part))

    for i in range(len(integer_part)):
        result[i] = integer_part[i]

    i = -1
    for digit in decimal_part:
        result[i] = digit
        i -= 1

    return result


def __check_valid_string_repr(str_repr):
    if re.fullmatch(r"-?[0-9a-z]+\.[0-9a-z]*", str_repr) is None:
        raise ValueError("Invalid string representation.")


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
    decimal_string = decimal_string.replace(".", "").replace("-", "")
    return max(STRING_TO_DIGIT[digit] for digit in decimal_string)


def add_decimal_numbers(num_1: DecimalNumber, num_2: DecimalNumber) -> DecimalNumber:
    """
    Return a new DecimalNumber instance 
    whose value is the sum of two other DecimalNumbers.

    Operants must have the same base,
    raise an error if they have different bases.

    Arguments:
    * num_1, num_2: DecimalNumbers whose sum to compute.
    """
    if num_1.base != num_2.base:
        raise NotImplementedError(
            "Can only add DecimalNumbers of the same base.")

    if num_1.sign == num_2.sign:
        return __add_decimal_numbers_same_sign(num_1, num_2)
    else:
        return __add_decimal_numbers_opposite_sign(num_1, num_2)


def __add_decimal_numbers_same_sign(num_1: DecimalNumber,
                                    num_2: DecimalNumber) -> DecimalNumber:
    result = num_1.copy()
    for (pos, digit_value) in num_2:
        result._add_to_digit(pos, digit_value)
    return result


def __add_decimal_numbers_opposite_sign(num_1: DecimalNumber,
                                        num_2: DecimalNumber) -> DecimalNumber:
    # Find number greatest magnitute;
    # subtract smallest from largest to avoid no-available-borrow problem.
    # Set the correct sign separately.
    num_1_inverted = num_1.copy()
    num_1_inverted.set_sign(num_1.sign * -1)
    if (num_1_inverted >= num_2):
        if num_2.sign == 1:
            biggest = num_1
            smallest = num_2
        else:
            biggest = num_2
            smallest = num_1
    elif num_2.sign == 1:
        biggest = num_2
        smallest = num_1
    else:
        biggest = num_1
        smallest = num_2
    result = biggest.copy()
    result.set_sign(biggest.sign)
    for (pos, digit_value) in smallest:
        result._subtract_from_digit(pos, digit_value)
    return result
