#
# Copyright (c) 2022 by Delphix. All rights reserved.
#

"""Classes used for Various Operations
"""

__all__ = ["ArithmeticOperations"]

from dlpx.virtualization.common.exceptions import ArithmeticException


class ArithmeticOperations(object):
    """class for Arithmetic Operations.

    Args:
        variable first: Operation First variable.
        variable second: Operation Second variable.

    """
    def __init__(self, first, second):
        if first:
            self.__first = first
        else:
            raise ArithmeticException("First variable can not be null or zero.")

        if second:
            self.__second = second
        else:
            raise ArithmeticException("Second variable can not be null or zero.")

    @property
    def first(self):
        return self.__first

    @property
    def second(self):
        return self.__second

    def add(self):
        """Adds two variables
        """
        return self.__first + self.__second

    def subtract(self):
        """Subtract first variable from second
        """
        return self.__first - self.__second

    def multiply(self):
        """multiple two variables
        """
        return self.__first * self.__second

    def divide(self):
        """divide first variable by second and return nearest integer value
        """
        return self.__first // self.__second
