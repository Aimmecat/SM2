from Algorithm.TimesPoint import AddSub
from ECC import Point
from Utils.KDF import KDF
from Utils.TransformData import Trans_AsciiDecode
from SM3 import SM3

p = "8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3"
a = "787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498"
dB = "1649AB77A00637BD5E2EFE283FBF353534AA7F7CB89463F208DDBC2920BB0DA0"
k_len = 152


def CreatSM2Decryption(C1: str, C2: str, C3: str):
    C1 = Point(C1[2:66], C1[66:], p, a)
    point = AddSub(dB, C1)
    x = hex(point.x).replace('0x', '')
    y = hex(point.y).replace('0x', '')
    t = KDF(x + y, k_len)
    M = hex(int(C2, 16) ^ int(t, 16)).replace('0x', '')
    sm3 = SM3()
    u = sm3.CreateHv(x + M + y)
    if u.upper() == C3.upper():
        return Trans_AsciiDecode(M.upper())


C1 = '04245C26FB68B1DDDDB12C4B6BF9F2B6D5FE60A383B0D18D1C4144ABF17F6252E776CB9264C2A7E88E52B19903FDC47378F605E36811F5C07423A24B84400F01B8'
C2 = '650053A89B41C418B0C3AAD00D886C00286467'
C3 = '9C3D7360C30156FAB7C80A0276712DA9D8094A634B766D3A285E07480653426D'
print(CreatSM2Decryption(C1, C2, C3))
