from ECC import Point
from Utils.KDF import KDF
from Utils.TransformData import Trans_AsciiDecode
from SM3 import SM3
from SM2 import GetSM2Parameter
import cProfile

dB = "3945208F 7B2144B1 3F36E38A C6D39F95 88939369 2860B51A 42FB81EF 4DF7C5B8".replace(' ', '')
k_len = 152

C1 = '0404EBFC718E8D1798620432268E77FEB6415E2EDE0E073C0F4F640ECD2E149A73E858F9D81E5430A57B36DAAB8F950A3C64E6EE6A63094D99283AFF767E124DF0'
C2 = '21886ca989ca9c7d58087307ca93092d651efa'
C3 = '59983C18F809E262923C53AEC295D30383B54E39D609D160AFCB1908D0BD8766'

testM = '0404EBFC718E8D1798620432268E77FEB6415E2EDE0E073C0F4F640ECD2E149A73E858F9D81E5430A57B36DAAB8F950A3C64E6EE6A63094D99283AFF767E124DF059983C18F809E262923C53AEC295D30383B54E39D609D160AFCB1908D0BD876621886CA989CA9C7D58087307CA93092D651EFA'


def CreatSM2Decryption(m: str):
    p, a, _, _, _, _ = GetSM2Parameter()
    m = m[2:]
    C1 = m[0: 128]
    C3 = m[128: 192]
    C2 = m[192:]
    C1 = Point(C1[0:64], C1[64:], p, a)
    point = C1.PointMultiply(dB)
    x = point.Get_X()
    y = point.Get_Y()
    t = KDF(x + y, k_len)
    M = hex(int(C2, 16) ^ int(t, 16)).replace('0x', '')
    sm3 = SM3()
    u = sm3.CreateHv(x + M + y)
    if u.upper() == C3.upper():
        return Trans_AsciiDecode(M.upper())


def CreatSM2DecryptionTime(m: str):
    return CreatSM2Decryption(m)


def CreatSM2DecryptionTime2():
    for i in range(20):
        CreatSM2Decryption(testM)


if __name__ == "__main__":
    cProfile.run('CreatSM2DecryptionTime2()')
