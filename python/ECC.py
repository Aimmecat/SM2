import Algorithm.Montgomery as mg
import Utils.JacobiPoint as jp


class Point(object):
    domain = "prime"
    a = None
    b = None
    r = 115792089237316195423570985008687907853269984665640564039457584007913129639936
    r1 = 26959946667150639794667015087019630673716372585036390074623444647937
    r2 = 107839786681156762650902923513421286826326218306071004709145723011075
    _n = 115792089129476408767522629297870205758541517347941659817034995947026826395649
    # r = 256
    # r1 = 9
    # r2 = 5
    # _n = 229

    def __init__(self, x, y, p, a='1', value='1'):
        self.x = int(x, 16)
        self.y = int(y, 16)
        self.p = int(p, 16)
        self.a = int(a, 16)
        self.value = int(value, 16)

        self.jacobi_x = int(x, 16)
        self.jacobi_y = int(y, 16)
        self.jacobi_z = 1

    def __str__(self):
        return "Point(" + hex(self.x).replace('0x', '').upper() + "," + hex(self.y).replace('0x', '').upper() + ")"

    __repr__ = __str__

    def __add__(self, other):
        if type(self) == Point and type(other) == Point:
            denominator = self.x - other.x
            if denominator != 0:
                return AffineAddPoint(self, other)
            return AffineTimesPoint(self)
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
                lambdas = mg.MontgomeryDivisionMod(numerator, denominator, self.p, self.r, self.r1, self.r2, self._n)
            else:
                numerator = 3 * self.x * self.x + self.a
                denominator = 2 * self.y
                lambdas = mg.MontgomeryDivisionMod(numerator, denominator, self.p, self.r, self.r1, self.r2, self._n)
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

    def Get_X(self):
        ret = hex(self.x).replace('0x', '').upper()
        l = len(ret)
        ret = '0' * (64 - l) + ret
        return ret

    def Get_Y(self):
        ret = hex(self.y).replace('0x', '').upper()
        l = len(ret)
        ret = '0' * (64 - l) + ret
        return ret

    def PointMultiply(self, k):
        # preP = SlideWindowPreCalc(self)
        # return SlideWindow(k, preP)
        jacobi_point = jp.JacobiPoint(self.x, self.y, 1, self.p, self.a)
        jacobi_preP  = jp.JacobiSlideWindowPreCalcPlus(jacobi_point)
        new_x, new_y, p, a, value = jp.JacobiSlideWindowPlus(k, jacobi_preP)
        return Point(new_x, new_y, p, a, value)


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

def SlideWindowPreCalc(P: Point, w=4):
    preP = {}
    P1 = P
    P2 = P + P
    preP['1'] = P1
    preP['2'] = P2
    for i in range(1, 2 ** (w - 1)):
        preP[str(2 * i + 1)] = preP[str(2 * i - 1)] + preP['2']
    return preP


def SlideWindow(k, preP: dict, w: int = 4):
    if type(k) == str:
        k = int(k, 16)
    bin_k = ''.join(reversed(bin(k).replace('0b', '')))
    l = len(bin_k)
    j = l - 1
    Q = AdditiveIdentityElement()
    while j >= 0:
        if k & (1 << j) == 0:
            Q = Q + Q
            j -= 1
        else:
            t = j + 1 - w
            while t < 0:
                t += 1
            while k & (1 << t) == 0:
                t += 1
            hj = 0
            for i in range(j - t + 1):
                hj += int(bin_k[t + i]) << i
            addQ = Q
            for i in range(j - t + 1):
                addQ = addQ + addQ
            addP = preP[str(hj)]
            Q = addQ + addP
            j = t - 1
    return Q

def AffineAddPoint(P: Point, Q: Point):
    numerator = P.y - Q.y
    denominator = P.x - Q.x
    lambdas = mg.MontgomeryDivisionMod(numerator, denominator, P.p, P.r, P.r1, P.r2, P._n)
    new_x = (lambdas * lambdas - P.x - Q.x) % P.p
    new_y = (lambdas * (P.x - new_x) - P.y) % P.p
    new_x = hex(new_x).replace('0x', '')
    new_y = hex(new_y).replace('0x', '')
    p = hex(P.p).replace('0x', '')
    a = hex(P.a).replace('0x', '')
    value = hex(P.value + P.value).replace('0x', '')
    return Point(new_x, new_y, p, a, value)

def AffineTimesPoint(P: Point):
    numerator = 3 * P.x * P.x + P.a
    denominator = 2 * P.y
    lambdas = mg.MontgomeryDivisionMod(numerator, denominator, P.p, P.r, P.r1, P.r2, P._n)
    new_x = (lambdas * lambdas - (P.x << 1) ) % P.p
    new_y = (lambdas * (P.x - new_x) - P.y) % P.p
    new_x = hex(new_x).replace('0x', '')
    new_y = hex(new_y).replace('0x', '')
    p = hex(P.p).replace('0x', '')
    a = hex(P.a).replace('0x', '')
    value = hex(P.value + P.value).replace('0x', '')
    return Point(new_x, new_y, p, a, value)


# p = '13'
# P1 = Point('A', '2', p)
# P2 = Point('9', '6', p)
# print(P1 + P2)
# print(P1 + P1)
