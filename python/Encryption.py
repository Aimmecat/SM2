from ECC import Point
from Utils.KDF import KDF
from SM3 import SM3
from Utils.TransformData import Trans_AsciiEncode
from SM2 import GetSM2Parameter, GetK

import cProfile

xb = "09F9DF31 1E5421A1 50DD7D16 1E4BC5C6 72179FAD 1833FC07 6BB08FF3 56F35020".replace(' ', '')
yb = "CCEA490C E26775A5 2DC6EA71 8CC1AA60 0AED05FB F35E084A 6632F607 2DA9AD13".replace(' ', '')
M = 'encryption standard'


def CreatSM2Encryption(m, xb, yb):
    p, a, b, n, xg, yg = GetSM2Parameter()
    G = Point(xg, yg, p, a)
    k = GetK("encryption")
    point1 = G.PointMultiply(k)
    x1 = point1.Get_X()
    y1 = point1.Get_Y()
    C1 = '04' + x1 + y1
    PB = Point(xb, yb, p, a)
    point2 = PB.PointMultiply(k)
    x2 = point2.Get_X()
    y2 = point2.Get_Y()
    M = Trans_AsciiEncode(m)
    k_len = len(M) * 4
    t = KDF(x2 + y2, k_len)
    C2 = hex(int(M, 16) ^ int(t, 16)).replace('0x', '')
    sm3 = SM3()
    C3 = sm3.CreateHv(x2 + M + y2)
    return (C1 + C3 + C2).upper()


def CreatSM2EncryptionTime():
    ret = CreatSM2Encryption(m=M, xb=xb, yb=yb)
    return ret

def CreatSM2EncryptionTime2():
    for i in range(20):
        CreatSM2Encryption(m=M, xb=xb, yb=yb)


if __name__ == "__main__":
    cProfile.run("CreatSM2EncryptionTime2()")
