from ECC import Point, AdditiveIdentityElement
from Utils.JacobiPoint import JacobiPoint, JacobiAdditiveIdentityElement
import math

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

def SlideWindowPreCalcPlus(P: Point, w=4):
    prePP = {}
    P1 = P
    P2 = P + P
    prePP['1'] = P1
    prePP['2'] = P2
    for i in range(1, 2 ** w):
        prePP[str(i + 1)] = prePP[str(i)] + prePP['1']
    return prePP

def SlideWindowPlus(k, preP: dict, w: int = 4):
    if type(k) == str:
        k = int(k, 16)
    bin_k = bin(k).replace('0b', '')
    l = len(bin_k)
    bin_k = '0' * (math.ceil(l / 4) * 4 - l) + bin_k
    bin_k = ''.join(reversed(bin_k))
    l = len(bin_k)
    r = l // 4
    j = r - 1
    Q = AdditiveIdentityElement()
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
    return Q

##########################################################
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
##########################################################



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

    prePP = SlideWindowPreCalcPlus(testP, window_r)
    start4 = time.time()
    print(SlideWindowPlus(k, prePP, window_r))
    end4 = time.time()

    testP = JacobiPoint(int(xg, 16), int(yg, 16), 1, int(p, 16), int(a, 16))
    jacobi_preP = JacobiSlideWindowPreCalcPlus(testP, window_r)
    start5 = time.time()
    print(JacobiSlideWindowPlus(k, jacobi_preP, window_r))
    end6 = time.time()

    print("BinaryExpansion:" + str(end1 - start1))
    print("AddSub:" + str(end2 - start2))
    print("SlideWindow:" + str(end3 - start3))
    print("SlideWindowPlus:" + str(end4 - start4))
    print("JacobiSlideWindowPlus:" + str(end6 - start5))
