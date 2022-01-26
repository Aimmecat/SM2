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
    bin_3k = bin(3 * k).replace('0b', '')
    bin_k = bin(k).replace('0b', '')
    len_bin_3k = len(bin_3k)
    len_bin_k = len(bin_k)
    bin_k = '0' * (len_bin_3k - len_bin_k) + bin_k
    Q = P
    for i in range(1, len_bin_3k - 1):
        Q = Q + Q
        if bin_3k[i] == '1' and bin_k[i] == '0':
            Q = Q + P
        elif bin_3k[i] == '0' and bin_k[i] == '1':
            Q = Q - P
    return Q


def SlideWindow(k, P: Point, r: int):
    if type(k) == str:
        k = int(k, 16)
    # P1 P2 P3 P5 P7...
    preP = {}
    bin_k = ''.join(reversed(bin(k).replace('0b', '')))
    l = len(bin_k)
    # 预计算
    # a)
    P1 = P
    P2 = P + P
    preP['1'] = P1
    preP['2'] = P2
    # b)
    for i in range(1, 2 ** (r - 1)):
        preP[str(2*i+1)] = preP[str(2*i-1)] + preP['2']
    # c)
    j = l - 1
    Q = AdditiveIdentityElement()
    while j >= 0:
        if bin_k[j] == '0':
            Q = Q + Q
            j -= 1
        else:
            t = j + 1 - r
            while bin_k[t] != '1':
                t += 1
            hj = 0
            for i in range(j - t + 1):
                hj += int(bin_k[t + i]) * 2 ** i
            addQ = AdditiveIdentityElement()
            for i in range(2 ** (j - t + 1)):
                addQ += Q
            addP = preP[str(hj)]
            Q = addQ + addP
            j = t - 1
    return Q


# import time
#
# p = "8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3"
# k = '6CB28D99385C175C94F94E934817663FC176D925DD72B727260DBAAE1FB2F96F'
# testP = Point("421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D", "0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2", p, "787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498")
#
# start1 = time.time()
# print(BinaryExpansion(k, testP))
# end1 = time.time()
#
# start2 = time.time()
# print(AddSub(k, testP))
# end2 = time.time()
#
# start3 = time.time()
# print(SlideWindow(k, testP, 2))
# end3 = time.time()
#
# print("BinaryExpansion:" + str(end1 - start1))
# print("AddSub:" + str(end2 - start2))
# print("SlideWindow:" + str(end3 - start3))
