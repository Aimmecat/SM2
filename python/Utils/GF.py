import math
"""
    GF field:
        give p witch is:
            1、Odd prime Numbers            p = p
            2、Expanding domain element     p = 2**m (wait to finish...)
        you should input the p with the style of str to init...
            such as:
                GF('17')
"""


class GF(object):
    def __init__(self, inp, p):
        self.p = p
        self.inp = inp
        self.inp %= self.p

    def __add__(self, other):
        return (self.inp + other.inp) % self.p

    def __sub__(self, other):
        return (self.inp - other.inp) % self.p

    def __mul__(self, other):
        return (self.inp * other.inp) % self.p

    def __truediv__(self, other):
        return (self.inp - other.inp) % self.p


