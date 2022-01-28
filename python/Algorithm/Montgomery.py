"""
    蒙哥马利预计算：高位相减法快速求 a mod p
"""


def RapidMod(a: int, p: int):
    if a < 0:
        c, r = RapidMod(-a, p)
        if r:
            return -c - 1, p - r
        else:
            return -c, 0
    if a < p:
        return 0, a
    a_len = a.bit_length()
    p_len = p.bit_length()
    d_len = a_len - p_len
    if d_len == 0:
        return 1, a - p
    c = 0
    for j in range(d_len, -1, -1):
        c <<= 1
        a1 = a >> j
        if a1 < p:
            continue
        c += 1
        b1 = a - (a1 << j)
        a1 = a1 - p
        a = (a1 << j) + b1
    return c, a


"""
    蒙哥马利预计算：快速模乘 a * b mod p
"""


def RapidMultiplyMod(a: int, b: int, p: int):
    _, a = RapidMod(a, p)
    _, b = RapidMod(b, p)
    r = 0
    b_len = b.bit_length()
    for bit in range(b_len):
        if b & (1 << bit):
            _, r = RapidMod(a + r, p)
        _, a = RapidMod(a << 1, p)
    return r


"""
    快速模幂： a ** b mod p
"""


def RapidPowerMod(a: int, b: int, p: int):
    _, a = RapidMod(a, p)
    r = 1
    b_len = b.bit_length()
    for bj in range(b_len, -1, -1):
        r = RapidMultiplyMod(r, r, p)
        if b & (1 << bj):
            r = RapidMultiplyMod(r, a, p)
    return r


"""
    扩展欧几里得求模逆元
    a * a^(-1) + p * (-k) = 1
    Init:
        x(0) = 1, y(0) = 0, r(0) = a
        x(0) = 0, y(0) = 1, r(1) = p
    Loop:
        x(i+1) = x(i-1) - q(i) * x(i)
        y(i+1) = y(i-1) - q(i) * y(i)
        r(i+1) = r(i-1) - q(i) * r(i)
        q(i)   = ceil(r(i-1) / r(i))
"""


def ExitEuclidean(a: int, p: int, label=None):
    if p == 0:
        return 0
    x_last, x_now = (1, 0) if label is None else (0, 1)
    r_last, r_now = a, p
    while r_now != 0:
        # q, c = RapidMod(r_last, r_now)
        # r_last, r_now = r_now, c
        q = r_last // r_now
        r_last, r_now = r_now, r_last - q * r_now
        x_last, x_now = x_now, x_last - q * x_now
    return x_last


"""
    求解 a^-1 mod p
"""


def RapidInverseMod(a: int, p: int, r: int, r1: int, _n: int):
    a = MontgomeryMod(a, p, r, r1, _n)
    x = ExitEuclidean(a, p)
    return MontgomeryMod(x, p, r, r1, _n)


"""
    蒙哥马利预计算：
    Input:
            n:  mod n 取模数
    Output: 
            r : R
            r1: R mod n
            r2: R mod n
            _n: N'
"""


def MontgomeryPreCalculate(n: int, max_bit=512):
    lens = n.bit_length()
    r_len = (lens + 7) // 8 * 8
    while r_len < max_bit:
        r_len += 8
    r = 2 ** r_len
    _, r1 = RapidMod(r, n)
    r2 = RapidMultiplyMod(r1, r1, n)
    y = ExitEuclidean(r, n, 'Pre')
    _, _n = RapidMod(-y, r)
    return r, r1, r2, _n


"""
    蒙哥马利模约减
    Input:
            x:   number a 
            n:   取模数
            r:   R
            _n:  N'
    Output:
            x mod n
"""


def MontgomeryReduction(x: int, n: int, r: int, _n: int):
    r_bit_len = r.bit_length() - 1
    r_mask = r - 1
    m = ((x & r_mask) * _n) & r_mask
    x = (x + m * n) >> r_bit_len
    ret = x if (x < n) else (x - n)
    return ret


"""
    蒙哥马利取模
    Input:
            a:   number a
            n:   取模数
            r:   R
            r1:  R mod p
            _n:  N'
    Output:
            a mod p
"""


def MontgomeryMod(a: int, n: int, r: int, r1: int, _n: int):
    return MontgomeryReduction(a * r1, n, r, _n)


"""
    蒙哥马利模乘
    Input:
            a:   number a
            b:   number b
            n:   取模数
            r:   R
            r2:  R * R mod p
            _n:  N'
    Output:
            a * b mod p
"""


def MontgomeryMultiplyMod(a: int, b: int, n: int, r: int, r2: int, _n: int):
    ar = MontgomeryReduction(a * r2, n, r, _n)
    br = MontgomeryReduction(b * r2, n, r, _n)
    abr = MontgomeryReduction(ar * br, n, r, _n)
    return MontgomeryReduction(abr, n, r, _n)


"""
    蒙哥马利模幂
    Input:
            a:   number a
            b:   number b
            n:   取模数
            r:   R
            r2:  R * R mod p
            _n:  N'
    Output:
            a ** b mod p
"""


def MontgomeryExpMod(a: int, b: int, n: int, r: int, r2: int, _n: int):
    rs = 1
    b_len = b.bit_length()
    for bit in range(b_len, -1, -1):
        rs = MontgomeryMultiplyMod(rs, rs, n, r, r2, _n)
        if b & (1 << bit):
            rs = MontgomeryMultiplyMod(rs, a, n, r, r2, _n)
    return rs


"""
    蒙哥马利模除
    Input:
            a:   number a
            b:   number b
            n:   取模数
            r:   R
            r2:  R * R mod p
            _n:  N'
    Output:
            a / b mod p
"""


def MontgomeryDivisionMod(a: int, b: int, n: int, r: int, r1: int, r2: int, _n: int):
    b = RapidInverseMod(b, n, r, r1, _n)
    ar = MontgomeryReduction(a * r2, n, r, _n)
    br = MontgomeryReduction(b * r2, n, r, _n)
    abr = MontgomeryReduction(ar * br, n, r, _n)
    return MontgomeryReduction(abr, n, r, _n)


"""
    蒙哥马利模除2
    Input:
            a:   number a
            b:   number b
            n:   取模数
            r:   R
            r2:  R * R mod p
            _n:  N'
    Output:
            a / b mod p
"""


def MontgomeryDivisionMod2(a: int, b: int, n: int, r: int, r1: int, r2: int, _n: int):
    numerator = MontgomeryMod(a, n, r, r1, _n)
    denominator = MontgomeryExpMod(b, n - 2, n, r, r2, _n)
    return MontgomeryMod(numerator * denominator, n, r, r1, _n)


# r, r1, r2, _n = MontgomeryPreCalculate(int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF", 16), 256)
# print(r)
# print(r1)
# print(r2)
# print(_n)

# r, r1, r2, _n = MontgomeryPreCalculate(int("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123", 16), 512)
# print(r)
# print(r1)
# print(r2)
# print(_n)
