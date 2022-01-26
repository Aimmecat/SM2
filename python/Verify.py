from SM3 import SM3
from ECC import Point
from Algorithm.TimesPoint import AddSub

R = '40F1EC59F793D9F49E09DCEF49130D4194F79FB1EED2CAA55BACDB49C4E755D1'
S = '6FC6DAC32C5D5CF10C77DFB20F7C2EB667A457872FB09EC56327A67EC7DEEBE7'
M = 'F4A38489E32B45B6F876E3AC2168CA392362DC8F23459C1D1146FC3DBFB7BC9A6d65737361676520646967657374'
n = "8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7"
xg = "421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D"
yg = "0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2"
xa = "0AE4C7798AA0F119471BEE11825BE46202BB79E2A5844495E97C04FF4DF2548A"
ya = "7C0240F88F1CD4E16352A73C17B7F16F07353E53A176D684A9FE0C6BB798E857"
p = "8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3"
a = "787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498"

def CreateSM2Verify():
    sm3 = SM3()
    e = sm3.CreateHv(M)
    t = (int(R, 16) + int(S, 16)) % int(n, 16)
    G = Point(xg, yg, p, a)
    point1 = AddSub(int(S, 16), G)
    PA = Point(xa, ya, p, a)
    point2 = AddSub(t, PA)
    point = point1 + point2
    r = (int(e, 16) + point.x) % int(n, 16)
    r = hex(r).replace('0x', '').upper()
    return r == R


result = CreateSM2Verify()
print(result)

