#!/usr/bin/env python3

"""Script contains a list of useful functions for work with dictionaries.

Functions:
- union, intersection, difference, symmetric difference
- sort dictionary by keys/values in different orders
- swap dictionary
"""

import cmath
import functools
import math


class Vector:
    __slots__ = ('_x', '__y')

    def __init__(self, x, y):
        self._x = x
        self.__y = y

    @property
    def x(self):
        return self._x  # this attr is pseudoprivate

    @property
    def y(self):
        return self.__y  # this one is private (mangled)

    @property
    @functools.lru_cache(maxsize=1)
    def length(self):
        # Directly -- not the most efficient way
        # return (self.x ** 2 + self.y ** 2) ** 0.5

        #print('this is lazy, doing computations...')
        return abs(self.x + 1j * self.y)


##    @property
##    def length(self):
##        if not hasattr(self, '_length'):
##            print('computing')
##            self._length = abs(self.x + 1j * self.y)
##        return self._length

# @length.setter
# def length(self, val):
#     print(f'Attemting to set length to {val}')

    @classmethod
    def from_polar(cls, length, angle, *, isdeg=True):
        """Make Vector from polar coordinates (length & angle)

        Args:
            length: vector length as returned by Vector.length
            angle: vector rotation in radians (if `isdeg` is False)
                   or in degrees (if `isdeg` is True or not provided)
            isdeg: angle is given in degrees (if True) or in radians
                   (if False)
        Returns:
            Vector instance
        """
        # do conversion to radians if needed
        if isdeg:
            angle = math.radians(angle)

        x = length * math.cos(angle)
        y = length * math.sin(angle)
        return cls(x=x, y=y)

    @staticmethod
    def angle_between(veca, vecb, *, isdeg=True):
        a, b = [vec.x + 1j * vec.y for vec in [veca, vecb]]
        anga, angb = [cmath.phase(el) for el in [a, b]]
        angle = angb - anga
        if isdeg:
            angle = math.degrees(angle)
        return angle

    def __repr__(self):
        clsname = self.__class__.__name__
        return f'{clsname}(x={self.x}, y={self.y})'

    def __bool__(self):
        return not self.x == self.y == 0

    def __add__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError(f'operands {self} and {other} type mismatch')

        # create a new vector with sum of coords
        x = self.x + other.x
        y = self.y + other.y
        # same as self.__class__(x=x, y=y)
        return type(self)(x=x, y=y)

    def __sub__(self, other):
        return self + (other * -1)  # call mul explicitly

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        # we will implement only Vector * scalar multiplication
        # resulting in proportional scaling of its coords

        if not isinstance(other, type(self)):
            # if has other type
            if not isinstance(other, int):
                # and this type is not integer
                # ==> ensure it is convertable to float
                other = float(other)
            # now we're either dealing with int, or with float
            return type(self)(x=other * self.x, y=other * self.y)

        # TODO: add vector by vector mul here
        # vector cross product and dot product
        # Note: you may use __mul__ for dot product,
        # and __matmul__ for cross product
        raise NotImplementedError('not done yet, see TODO')

    def __truediv__(self, other):
        if not other:
            raise ZeroDivisionError

        return self * (1 / other)

    def __eq__(self, other):
        try:
            return self.x == other.x and self.y == other.y
        except Exception:
            return False

    # __neq__ is implemented automatically

    def __len__(self):
        return 2

    def __getitem__(self, index):
        return [self.x, self.y][index]

    def __hash__(self):
        # if each object is unique
        # return id(self)
        # if it is not exactly unique and applicable to use
        # other object with same values during indexing
        return hash(self.x) ^ hash(self.y)


class Point(Vector):
    pass


if __name__ == '__main__':
    vec = Vector(3, 5)
    oth = Vector(10, 20)

    zero = Vector(0, 0)
    bool(zero)  # returns False

    res = vec * 3 + oth / 10

    diag = Vector.from_polar(length=10, angle=45, isdeg=True)

    one = Vector.from_polar(1, 45)
    two = Vector.from_polar(10, 135)

    angle = Vector.angle_between(one, two)
