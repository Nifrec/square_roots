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