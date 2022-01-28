from ECC import Point, AdditiveIdentityElement


def BinaryExpansion(k, P: Point):
    if type(k) == str:
        k = int(k, 16)
    bin_k = bin(k).replace('0b', '')
    Q = AdditiveIdentityElement()
    for bit_k in bin_k:
        Q = Q + Q
        if bit_k == '1':
            Q = Q + P
    return Q


def AddSub(k, P: Point):
    if type(k) == str:
        k = int(k, 16)
    third_k = 3 * k
    len_bin_3k = third_k.bit_length()
    Q = P
    for i in range(len_bin_3k - 2, 0, -1):
        Q = Q + Q
        if third_k & (1 << i) and k & (1 << i) == 0:
            Q = Q + P
        elif third_k & (1 << i) == 0 and k & (1 << i):
            Q = Q - P
    return Q


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
        if bin_k[j] == '0':
            Q = Q + Q
            j -= 1
        else:
            t = j + 1 - w
            while bin_k[t] != '1' or t < 0:
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


if __name__ == "__main__":
    import time

    p = "FFFFFFFE FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF 00000000 FFFFFFFF FFFFFFFF".replace(' ', '')
    k = "59276E27 D506861A 16680F3A D9C02DCC EF3CC1FA 3CDBE4CE 6D54B80D EAC1BC21".replace(' ', '')
    a = "FFFFFFFE FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF 00000000 FFFFFFFF FFFFFFFC".replace(' ', '')
    xg = "32C4AE2C 1F198119 5F990446 6A39C994 8FE30BBF F2660BE1 715A4589 334C74C7".replace(' ', '')
    yg = "BC3736A2 F4F6779C 59BDCEE3 6B692153 D0A9877C C62A4740 02DF32E5 2139F0A0".replace(' ', '')
    testP = Point(xg, yg, p, a)

    start1 = time.time()
    print(BinaryExpansion(k, testP))
    end1 = time.time()

    start2 = time.time()
    print(AddSub(k, testP))
    end2 = time.time()

    window_r = 4
    preP = SlideWindowPreCalc(testP, window_r)
    start3 = time.time()
    print(SlideWindow(k, preP, window_r))
    end3 = time.time()

    print("BinaryExpansion:" + str(end1 - start1))
    print("AddSub:" + str(end2 - start2))
    print("SlideWindow:" + str(end3 - start3))
