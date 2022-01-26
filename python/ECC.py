from Utils.mathoptimize import Get_Fraction_Mod


class Point(object):
    domain = "prime"
    a = None
    b = None

    def __init__(self, x, y, p, a='1', value='1'):
        self.x = int(x, 16)
        self.y = int(y, 16)
        self.p = int(p, 16)
        self.a = int(a, 16)
        self.value = int(value, 16)

    def __str__(self):
        return "Point(" + hex(self.x).replace('0x', '').upper() + "," + hex(self.y).replace('0x', '').upper() + ")"

    __repr__ = __str__

    def __add__(self, other):
        if type(self) == Point and type(other) == Point:
            denominator = self.x - other.x
            if denominator != 0:
                numerator = self.y - other.y
                lambdas = Get_Fraction_Mod(numerator, denominator, self.p)
            else:
                numerator = 3 * self.x * self.x + self.a
                denominator = 2 * self.y
                lambdas = Get_Fraction_Mod(numerator, denominator, self.p)
            new_x = (lambdas * lambdas - self.x - other.x) % self.p
            new_y = (lambdas * (self.x - new_x) - self.y) % self.p
            new_x = hex(new_x).replace('0x', '')
            new_y = hex(new_y).replace('0x', '')
            p = hex(self.p).replace('0x', '')
            a = hex(self.a).replace('0x', '')
            value = hex(self.value + other.value).replace('0x', '')
            return Point(new_x, new_y, p, a, value)
        else:
            new_x = hex(self.x).replace('0x', '')
            new_y = hex(self.y).replace('0x', '')
            p = hex(self.p).replace('0x', '')
            a = hex(self.a).replace('0x', '')
            return Point(new_x, new_y, p, a)

    def __sub__(self, other):
        if type(self) == Point and type(other) == Point:
            denominator = self.x - other.x
            if denominator != 0:
                numerator = self.y + other.y
                lambdas = Get_Fraction_Mod(numerator, denominator, self.p)
            else:
                numerator = 3 * self.x * self.x + self.a
                denominator = 2 * self.y
                lambdas = Get_Fraction_Mod(numerator, denominator, self.p)
            new_x = (lambdas * lambdas - self.x - other.x) % self.p
            new_y = (lambdas * (self.x - new_x) - self.y) % self.p
            new_x = hex(new_x).replace('0x', '')
            new_y = hex(new_y).replace('0x', '')
            p = hex(self.p).replace('0x', '')
            a = hex(self.a).replace('0x', '')
            value = hex(self.value - other.value).replace('0x', '')
            return Point(new_x, new_y, p, a, value)
        else:
            new_x = hex(self.x).replace('0x', '')
            new_y = hex(self.y).replace('0x', '')
            p = hex(self.p).replace('0x', '')
            a = hex(self.a).replace('0x', '')
            return Point(new_x, new_y, p, a)


class AdditiveIdentityElement(Point):
    def __init__(self):
        pass

    def __add__(self, other):
        return other

    def __sub__(self, other):
        return other

    def __str__(self):
        return 'AdditiveIdentityElement'
    __repr__ = __str__

# p = '13'
# P1 = Point('A', '2', p)
# P2 = Point('9', '6', p)
# print(P1 + P2)
# print(P1 + P1)
