# The MIT License (MIT)
#
# Copyright (c) 2022 Scott Lau
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging

from sc_utilities import Singleton
from sc_utilities import log_init

log_init()

from sc_excel_column_calculator import PROJECT_NAME, __version__
import argparse
import re


class Runner(metaclass=Singleton):

    def __init__(self):
        self._ASCII_A = ord('A')

    def run(self, *, args):
        logging.getLogger(__name__).info("arguments {}".format(args))
        logging.getLogger(__name__).info("program {} version {}".format(PROJECT_NAME, __version__))
        column = args.column
        column_index = self._calculate_column_index(column)
        print(column_index)
        logging.getLogger(__name__).info("column index {}".format(column_index))
        return 0

    def _calculate_column_index(self, column: str) -> int:
        if column is None or len(column) == 0:
            return -1
        column_name = column.upper()
        column_letter_stack = list()
        for letter in column_name:
            column_letter_stack.append(ord(letter) - self._ASCII_A + 1)

        result = 0
        level = 1
        while len(column_letter_stack) > 0:
            ascii_value = column_letter_stack.pop()
            result += ascii_value * level
            level = level * 26
        return result


def main():
    try:
        parser = argparse.ArgumentParser(description='Python project')
        parser.add_argument('column', help='Column letter')
        args = parser.parse_args()
        if re.match(r'^[a-zA-Z]+$', args.column) is None:
            print("bad input, alpha characters only")
            logging.getLogger(__name__).exception('bad input, alpha characters only')
            return 2
        state = Runner().run(args=args)
    except Exception as e:
        logging.getLogger(__name__).exception('An error occurred.', exc_info=e)
        return 1
    else:
        return state
