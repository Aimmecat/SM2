from Algorithm.TimesPoint import AddSub
from ECC import Point
from Utils.KDF import KDF
from SM3 import SM3
from Utils.TransformData import Trans_AsciiEncode
from Utils.TransformData import Trans_Point2Bytes

p = "8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3"
a = "787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498"
b = "63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A"
xg = "421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D"
yg = "0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2"
n = "8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7"
dB = "1649AB77A00637BD5E2EFE283FBF353534AA7F7CB89463F208DDBC2920BB0DA0"
xb = "435B39CCA8F3B508C1488AFC67BE491A0F7BA07E581A0E4849A5CF70628A7E0A"
yb = "75DDBA78F15FEECB4C7895E2C1CDF5FE01DEBB2CDBADF45399CCF77BBA076A42"
k = "4C62EEFD6ECFC2B95B92FD6C3D9575148AFA17425546D49018E5388D49DD7B4F"
M = 'message digest'


def CreatSM2Encryption(M):
    G = Point(xg, yg, p, a)
    point1 = AddSub(k, G)
    x1 = hex(point1.x).replace('0x', '')
    y1 = hex(point1.y).replace('0x', '')
    C1 = '04' + x1 + y1
    PB = Point(xb, yb, p, a)
    point2 = AddSub(k, PB)
    x2 = hex(point2.x).replace('0x', '')
    y2 = hex(point2.y).replace('0x', '')
    M = Trans_AsciiEncode(M)
    k_len = len(M) * 4
    t = KDF(x2 + y2, k_len)
    C2 = hex(int(M, 16) ^ int(t, 16)).replace('0x', '')
    sm3 = SM3()
    C3 = sm3.CreateHv(x2 + M + y2)
    return (C1 + C2 + C3).upper()


print(CreatSM2Encryption(M))
