from ECC import Point
from Utils.KDF import KDF
from Utils.TransformData import Trans_AsciiDecode
from SM3 import SM3
from SM2 import GetSM2Parameter

dB = "3945208F 7B2144B1 3F36E38A C6D39F95 88939369 2860B51A 42FB81EF 4DF7C5B8".replace(' ', '')
k_len = 152

C1 = '0404EBFC718E8D1798620432268E77FEB6415E2EDE0E073C0F4F640ECD2E149A73E858F9D81E5430A57B36DAAB8F950A3C64E6EE6A63094D99283AFF767E124DF0'
C2 = '21886ca989ca9c7d58087307ca93092d651efa'
C3 = '59983C18F809E262923C53AEC295D30383B54E39D609D160AFCB1908D0BD8766'


def CreatSM2Decryption(C1: str, C2: str, C3: str):
    p, a, _, _, _, _ = GetSM2Parameter()
    C1 = Point(C1[2:66], C1[66:], p, a)
    point = C1.PointMultiply(dB)
    x = point.Get_X()
    y = point.Get_Y()
    t = KDF(x + y, k_len)
    M = hex(int(C2, 16) ^ int(t, 16)).replace('0x', '')
    sm3 = SM3()
    u = sm3.CreateHv(x + M + y)
    if u.upper() == C3.upper():
        return Trans_AsciiDecode(M.upper())


def CreatSM2DecryptionTime():
    return CreatSM2Decryption(C1, C2, C3)

