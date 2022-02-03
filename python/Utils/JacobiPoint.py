import Algorithm.Montgomery as mg
# from ECC import Point
import math


class JacobiPoint(object):
    a = None
    r = 115792089237316195423570985008687907853269984665640564039457584007913129639936
    r1 = 26959946667150639794667015087019630673716372585036390074623444647937
    r2 = 107839786681156762650902923513421286826326218306071004709145723011075
    _n = 115792089129476408767522629297870205758541517347941659817034995947026826395649

    # r = 256
    # r1 = 9
    # r2 = 5
    # _n = 229

    def __init__(self, x, y, z, p, a, value=1):
        self.jacobi_x = x
        self.jacobi_y = y
        self.jacobi_z = z
        self.p = p
        self.a = a
        self.value = value

    def __str__(self):
        return 'value:' + str(self.value)

    __repr__ = __str__

    def __add__(self, other):
        if type(other) == JacobiPoint:
            if self == other:
                return JacobiTimesPoint2(self)
            return JacobiAddPoint2(self, other)
        else:
            return self

    def Trance2Point(self):
        new_x = mg.MontgomeryDivisionMod(self.jacobi_x, self.jacobi_z ** 2, self.p, self.r, self.r1, self.r2, self._n)
        new_y = mg.MontgomeryDivisionMod(self.jacobi_y, self.jacobi_z ** 3, self.p, self.r, self.r1, self.r2, self._n)
        new_x = hex(new_x).replace('0x', '')
        new_y = hex(new_y).replace('0x', '')
        p = hex(self.p).replace('0x', '')
        a = hex(self.a).replace('0x', '')
        value = hex(self.value).replace('0x', '')
        # return Point(new_x, new_y, p, a, value)
        return new_x, new_y, p, a, value


class JacobiAdditiveIdentityElement(JacobiPoint):
    def __init__(self):
        pass

    def __add__(self, other):
        return other

    def __sub__(self, other):
        return other

    def __str__(self):
        return 'AdditiveIdentityElement'

    __repr__ = __str__


def JacobiAddPoint(P: JacobiPoint, Q: JacobiPoint):
    lambda1 = mg.MontgomeryMultiplyMod(P.jacobi_x, mg.MontgomeryExpMod(Q.jacobi_z, 2, P.p, P.r, P.r2, P._n), P.p, P.r,
                                       P.r2, P._n)
    lambda2 = mg.MontgomeryMultiplyMod(Q.jacobi_x, mg.MontgomeryExpMod(P.jacobi_z, 2, P.p, P.r, P.r2, P._n), P.p, P.r,
                                       P.r2, P._n)
    lambda3 = lambda1 - lambda2
    lambda4 = mg.MontgomeryMultiplyMod(P.jacobi_y, mg.MontgomeryExpMod(Q.jacobi_z, 3, P.p, P.r, P.r2, P._n), P.p, P.r,
                                       P.r2, P._n)
    lambda5 = mg.MontgomeryMultiplyMod(Q.jacobi_y, mg.MontgomeryExpMod(P.jacobi_z, 3, P.p, P.r, P.r2, P._n), P.p, P.r,
                                       P.r2, P._n)
    lambda6 = lambda4 - lambda5
    lambda7 = lambda1 + lambda2
    lambda8 = lambda4 + lambda5
    new_x = mg.MontgomeryExpMod(lambda6, 2, P.p, P.r, P.r2, P._n) - \
            mg.MontgomeryMultiplyMod(lambda7, mg.MontgomeryExpMod(lambda3, 2, P.p, P.r, P.r2, P._n), P.p, P.r, P.r2,
                                     P._n)
    lambda9 = mg.MontgomeryMultiplyMod(lambda7, mg.MontgomeryExpMod(lambda3, 2, P.p, P.r, P.r2, P._n), P.p, P.r, P.r2,
                                       P._n) \
              - 2 * new_x
    new_y = mg.MontgomeryMultiplyMod(lambda9, lambda6, P.p, P.r, P.r2, P._n) \
            - mg.MontgomeryMultiplyMod(lambda8, mg.MontgomeryExpMod(lambda3, 3, P.p, P.r, P.r2, P._n), P.p, P.r,
                                       P.r2, P._n)
    if new_y & 1:
        new_y += P.p
    new_y >>= 1
    new_z = mg.MontgomeryMultiplyMod(mg.MontgomeryMultiplyMod(P.jacobi_z, Q.jacobi_z, P.p, P.r, P.r2, P._n), lambda3,
                                     P.p, P.r, P.r2, P._n)
    value = P.value + Q.value
    return JacobiPoint(new_x, new_y, new_z, P.p, P.a, value)


def JacobiTimesPoint(P: JacobiPoint):
    lambda1 = 3 * mg.MontgomeryExpMod(P.jacobi_x, 2, P.p, P.r, P.r2, P._n) \
              + mg.MontgomeryMultiplyMod(P.a, mg.MontgomeryExpMod(P.jacobi_z, 4, P.p, P.r, P.r2, P._n), P.p, P.r,
                                         P.r2, P._n)
    lambda2 = 4 * mg.MontgomeryMultiplyMod(P.jacobi_x, mg.MontgomeryExpMod(P.jacobi_y, 2, P.p, P.r, P.r2, P._n), P.p,
                                           P.r,
                                           P.r2, P._n)
    lambda3 = 8 * mg.MontgomeryExpMod(P.jacobi_y, 4, P.p, P.r, P.r2, P._n)
    new_x = mg.MontgomeryExpMod(lambda1, 2, P.p, P.r, P.r2, P._n) - 2 * lambda2
    if new_x < 0:
        new_x += P.p
    new_y = mg.MontgomeryMultiplyMod(lambda1, (lambda2 - new_x), P.p, P.r,
                                     P.r2, P._n) - lambda3
    if new_y <= 0:
        new_y += P.p
    new_z = 2 * mg.MontgomeryMultiplyMod(P.jacobi_y, P.jacobi_z, P.p, P.r,
                                         P.r2, P._n)
    value = P.value * 2
    return JacobiPoint(new_x, new_y, new_z, P.p, P.a, value)


def JacobiAddPoint2(P: JacobiPoint, Q: JacobiPoint):
    x1, y1, z1 = P.jacobi_x, P.jacobi_y, P.jacobi_z
    x2, y2, z2 = Q.jacobi_x, Q.jacobi_y, Q.jacobi_z
    p = P.p
    lambda1 = x1 * z2 ** 2 % p
    lambda2 = x2 * z1 ** 2 % p
    lambda3 = (lambda1 - lambda2) % p
    lambda4 = y1 * z2 ** 3 % p
    lambda5 = y2 * z1 ** 3 % p
    lambda6 = (lambda4 - lambda5) % p
    lambda7 = (lambda1 + lambda2) % p
    lambda8 = (lambda4 + lambda5) % p
    new_x = (lambda6 ** 2 - lambda7 * lambda3 ** 2) % p
    lambda9 = (lambda7 * lambda3 ** 2 - 2 * new_x) % p
    new_y = (lambda9 * lambda6 - lambda8 * lambda3 ** 3) % p
    if new_y & 1 or new_y <= 0:
        new_y = new_y + p
    new_y >>= 1
    new_z = z1 * z2 * lambda3 % p
    value = P.value + Q.value
    return JacobiPoint(new_x, new_y, new_z, P.p, P.a, value)


def JacobiTimesPoint2(P: JacobiPoint):
    x1, y1, z1, p, a = P.jacobi_x, P.jacobi_y, P.jacobi_z, P.p, P.a
    lambda1 = (3 * x1 ** 2 + a * z1 ** 4) % p
    lambda2 = (4 * x1 * y1 ** 2) % p
    lambda3 = (8 * y1 ** 4) % p
    new_x = (lambda1 ** 2 - 2 * lambda2) % p
    new_y = (lambda1 * (lambda2 - new_x) - lambda3) % p
    new_z = 2 * y1 * z1 % p
    value = P.value * 2
    return JacobiPoint(new_x, new_y, new_z, P.p, P.a, value)


def JacobiSlideWindowPreCalcPlus(P: JacobiPoint, w=4):
    jacobi_preP = {}
    P1 = P
    P2 = P + P
    jacobi_preP['1'] = P1
    jacobi_preP['2'] = P2
    for i in range(1, 2 ** w):
        jacobi_preP[str(i + 1)] = jacobi_preP[str(i)] + jacobi_preP['1']
    return jacobi_preP


def JacobiSlideWindowPlus(k, preP: dict, w: int = 4):
    if type(k) == str:
        k = int(k, 16)
    bin_k = bin(k).replace('0b', '')
    l = len(bin_k)
    bin_k = '0' * (math.ceil(l / 4) * 4 - l) + bin_k
    bin_k = ''.join(reversed(bin_k))
    l = len(bin_k)
    r = l // 4
    j = r - 1
    Q = JacobiAdditiveIdentityElement()
    while j >= 0:
        Q = Q + Q
        Q = Q + Q
        Q = Q + Q
        Q = Q + Q
        t = 0
        for i in range(4):
            t += int(bin_k[4 * j + i]) << i
        if t != 0:
            Q += preP[str(t)]
        j -= 1
    return Q.Trance2Point()


if __name__ == "__main__":
    pass
    # x1, y1 = 23, 118
    # x2, y2 = 32, 192
    #
    # hex_x1, hex_y1 = hex(x1).replace('0x', ''), hex(y1).replace('0x', '')
    # hex_x2, hex_y2 = hex(x2).replace('0x', ''), hex(y2).replace('0x', '')
    #
    # p = '13'
    # P1 = Point(hex_x1, hex_y1, p)
    # P2 = Point(hex_x2, hex_y2, p)
    # print(P1 + P2)
    # print(P1 + P1)
    #
    # p = 19
    # P1 = JacobiPoint(x1, y1, 1, p, 1)
    # P2 = JacobiPoint(x2, y2, 1, p, 1)
    # addP = (P1 + P2).Trance2Point()
    # doubleP = (P1 + P1).Trance2Point()
    # print(addP)
    # print(doubleP)
