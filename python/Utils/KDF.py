import math
from SM3 import SM3

v = 256


def KDF(Z: str, k_len):
    cnt = 1
    length = math.ceil(k_len / v)
    sm3 = SM3()
    H = []
    K = ''
    for i in range(1, length):
        add_cnt = (8 - len(hex(cnt).replace('0x', ''))) * '0' + hex(cnt).replace('0x', '')
        H.append(sm3.CreateHv(Z + add_cnt))
        cnt += 1
    add_cnt = (8 - len(hex(cnt).replace('0x', ''))) * '0' + hex(cnt).replace('0x', '')
    tail = sm3.CreateHv(Z + add_cnt)
    if k_len / v != k_len // v:
        tail = tail[0: (k_len - v * math.floor(k_len / v) + 1) // 4]
    for ha_i in H:
        K += ha_i
    K += tail
    return K

# x2 = '64D20D27D0632957F8028C1E024F6B02EDF23102A566C932AE8BD613A8E865FE'
# y2 = '58D225ECA784AE300A81A2D48281A828E1CEDF11C4219099840265375077BF78'
# klen = 152
# print(KDF(x2+y2, klen))
