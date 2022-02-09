import numpy as np

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
        q(i)   = floor(r(i-1) / r(i))
"""


def ExitEuclidean(a: int, p: int):
    if p == 0:
        return 0
    x_last, x_now = 0, 1
    r_last, r_now = p, a
    while r_now != 0:
        # q, c = RapidMod(r_last, r_now)
        # r_last, r_now = r_now, c
        q = r_last // r_now
        r_last, r_now = r_now, r_last - q * r_now
        x_last, x_now = x_now, x_last - q * x_now
    if x_last < 0:
        x_last += p
    return x_last


"""
    二进制扩展欧几里得
    a < p and gcd(a, p) = 1
    when a, p both odd:
        gcd(a, p) = gcd( (p - a) / 2, a ) = 1
        
        1) a > (p - a) / 2:
            F(a, p) ---> F( (p - a) / 2, a ) then
                x = -1/2 * x'  + y'
                y = 1/2 * x' 
                need x' to be even
                
                x    | -1/2  1 |  x'
                   = |         |
                y    |  1/2  0 |  y'
                
        2) a < (p - a) / 2:
            F(a, p) ---> F( a, (p - a) / 2 ) then
                x = x' - 1/2 * y' 
                y = 1/2 * y'
                need y' to be even
                
                x    | 1  -1/2 |  x'
                   = |         |
                y    | 0   1/2 |  y'
        
    when a is even, p is odd
        gcd(a, p) = gcd( a / 2, p ) = 1
        
            F(a, p) ---> F( a / 2, p ) then
                x = 1 / 2 * x'
                y = y'
                need x' to be even
                
                x    | 1/2   0 |  x'
                   = |         |
                y    | 0     1 |  y'
                
        
    when a is odd, p is even
        gcd(a, p) = gcd( a ,p / 2 ) = 1
        
        1) a > p / 2:
            F(a, p) ---> F( p / 2, a ) then
                x = y' 
                y = 1/2 * x' 
                need x' to be even
                
                x    |  0    1 |  x'
                   = |         |
                y    |  1/2  0 |  y'
                
        2) a < p / 2:
            F(a, p) ---> F( a, p / 2 ) then
                x = x'
                y = 1/2 * y'
                need y' to be even
                
                x    | 1     0 |  x'
                   = |         |
                y    | 0   1/2 |  y'
        
"""
def BExitEuclidean(a: int, p: int) -> int:
    init_p = p
    cnt = 0
    a00, a01 = 1, 0
    while a != 1:
        flag_a = a & 1
        flag_p = p & 1
        if flag_a and flag_p:
            num = (p - a) >> 1
            if a < num:
                p = num
                # [2, -1], [0, 1]
                a00, a01 = a00 << 1, a01 - a00
            else:
                a, p = num, a
                # [-1, 2], [1, 0]
                a00, a01 = a01 - a00, a00 << 1
        elif flag_a:
            num = p >> 1
            if a < num:
                p = num
                # [2, 0], [0, 1]
                a00 = a00 << 1
            else:
                a, p = num, a
                # [0, 2], [1, 0]
                a00, a01 = a01, a00 << 1
        elif flag_p:
            a = a >> 1
            # [1, 0], [0, 2]
            a01 = a01 << 1
        cnt += 1
    for i in range(cnt):
        if a00 & 1 == 0:
            a00 >>= 1
        else:
            a00 = (a00 + init_p) >> 1
    return a00


"""
    求解 a^-1 mod p
"""


def RapidInverseMod(a: int, p: int, r: int, r1: int, _n: int):
    _, a = RapidMod(a, p)
    x = BExitEuclidean(a, p)
    return RapidMod(x, p)[1]


def RapidInverseMod2(a: int, p: int):
    u, v, x1, x2, k = a, p, 1, 0, 0
    while v > 0:
        if v & 1 == 0:
            v >>= 1
            x1 <<= 1
        elif u & 1 == 0:
            u >>= 1
            x2 <<= 1
        elif v >= u:
            v = (v - u) >> 1
            x2 = x2 + x1
            x1 <<= 1
        else:
            u = (u - v) >> 1
            x1 = x2 + x1
            x2 <<= 1
        k += 1
    assert u == 1
    if x1 > p:
        x1 = x1 - p
    return x1, k


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
    x = ExitEuclidean(n, r)
    _, _n = RapidMod(-x, r)
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


def MontgomeryDivisionMod2(a: int, b: int, n: int, r: int, r2: int, _n: int):
    ar = MontgomeryReduction(a * r2, n, r, _n)
    br = MontgomeryReduction(b * r2, n, r, _n)
    x, k = RapidInverseMod2(br, n)
    x = MontgomeryReduction(x * r2, n, r, _n)
    x = MontgomeryReduction(x * (r << r.bit_length() - 1 >> k), n, r, _n)
    abr = MontgomeryReduction(ar * x, n, r, _n)
    return MontgomeryReduction(abr, n, r, _n)


test_n = "FFFFFFFE FFFFFFFF FFFFFFFF FFFFFFFF 7203DF6B 21C6052B 53BBF409 39D54123".replace(' ', '')
test_p = "FFFFFFFE FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF 00000000 FFFFFFFF FFFFFFFF".replace(' ', '')

if __name__ == "__main__":
    r, r1, r2, _n = MontgomeryPreCalculate(int(test_p, 16), 256)
    # r, r1, r2, _n = MontgomeryPreCalculate(int(test_n, 16), 256)
    # print(r)
    # print(r1)
    # print(r2)
    # print(_n)

    # a = 1
    # b = 23
    # n = 97
    # r, r1, r2, _n = MontgomeryPreCalculate(n, 12)
    #
    # print(MontgomeryDivisionMod(a, b, n, r, r1, r2, _n))
    # print(MontgomeryDivisionMod2(a, b, n, r, r2, _n))
    # x, k = RapidInverseMod2(b, n)
    # print(x, k)
    # print(MontgomeryDivisionMod(2 ** k, b, n, r, r1, r2, _n))
    # print(MontgomeryDivisionMod2(a, b, n, r, r2, _n))

    # import math
    #
    # a = int(test_n, 16)
    # p = int(test_p, 16)
    #
    # print(math.gcd(a, p))
    # assert math.gcd(a, p) == 1
    #
    # import time as t
    #
    # t1 = t.time()
    # for i in range(1000):
    #     ExitEuclidean(a, p)
    # t2 = t.time()
    #
    # ret1 = ExitEuclidean(a, p)
    # print(ret1)
    #
    # t3 = t.time()
    # for i in range(1000):
    #     BExitEuclidean(a, p)
    # t4 = t.time()
    #
    # ret2 = BExitEuclidean(a, p)
    # print(ret2)
    # print((t4 - t3) / (t2 - t1))
    # assert ret1 == ret2

    num1 = "38901280129789113687126868FFFCCCCC780908C7986C90C808C68A9879797A"
    num2 = "908013280182047107FFF78799A989CBCC098A0C980A99C071BBCCAFFEEA121C"
    num3 = "FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF"
    value1 = int(num1, 16)
    value2 = int(num2, 16)
    value3 = int(num3, 16)
    MontgomeryMod(value1, value2, r, r1, _n)
    ret = MontgomeryMultiplyMod(value1, value2, value3, r, r2, _n)
    ret2 = MontgomeryDivisionMod(value1, value2, value3, r, r1, r2, _n)
    print(hex(ret2).replace('0x', '').upper())
