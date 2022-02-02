import math


def ExitEuclidean(a: int, p: int) -> int:
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


test_n = "FFFFFFFE FFFFFFFF FFFFFFFF FFFFFFFF 7203DF6B 21C6052B 53BBF409 39D54123".replace(' ', '')
test_p = "FFFFFFFE FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF 00000000 FFFFFFFF FFFFFFF1".replace(' ', '')

if __name__ == "__main__":

    loop = 1000

    a = int(test_n, 16)
    p = int(test_p, 16)

    print(math.gcd(a, p))
    assert math.gcd(a, p) == 1

    import time as t

    t1 = t.time()
    for i in range(loop):
        ExitEuclidean(a, p)
    t2 = t.time()

    ret1 = ExitEuclidean(a, p)
    print(ret1)

    t3 = t.time()
    for i in range(loop):
        BExitEuclidean(a, p)
    t4 = t.time()

    ret2 = BExitEuclidean(a, p)
    print(ret2)
    print(t2 - t1)
    print(t4 - t3)
    print((t4 - t3) / (t2 - t1))
    assert ret1 == ret2
