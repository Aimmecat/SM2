from SM3 import SM3
from SM2 import GetSM2Parameter
from ECC import Point
import cProfile

R = 'F5A03B0648D2C4630EEAC513E1BB81A15944DA3827D5B74143AC7EACEEE720B3'
S = 'B1B6AA29DF212FD8763182BC0D421CA1BB9038FD1F7F42D4840B69C485BBC1AA'
M = 'B2E14C5C79C6DF5B85F4FE7ED8DB7A262B9DA7E07CCB0EA9F4747B8CCDA8A4F36D65737361676520646967657374'
xa = "09F9DF31 1E5421A1 50DD7D16 1E4BC5C6 72179FAD 1833FC07 6BB08FF3 56F35020".replace(' ', '')
ya = "CCEA490C E26775A5 2DC6EA71 8CC1AA60 0AED05FB F35E084A 6632F607 2DA9AD13".replace(' ', '')

def CreateSM2Verify(r, s, xa, ya, m):
    p, a, _, n, xg, yg = GetSM2Parameter()
    sm3 = SM3()
    e = sm3.CreateHv(m)
    t = (int(r, 16) + int(s, 16)) % int(n, 16)
    G = Point(xg, yg, p, a)
    point1 = G.PointMultiply(int(s, 16))
    PA = Point(xa, ya, p, a)
    point2 = PA.PointMultiply(t)
    point = point1 + point2
    r = (int(e, 16) + point.x) % int(n, 16)
    r = hex(r).replace('0x', '').upper()
    return r

def CreateSM2VerifyTime(receiveR, receiveS):
    ret = CreateSM2Verify(r=receiveR, s=receiveS, xa=xa, ya=ya, m=M)
    return ret


def CreateSM2VerifyTime2():
    for i in range(10):
        CreateSM2Verify(r=R, s=S, xa=xa, ya=ya, m=M)


if __name__ == "__main__":
    cProfile.run("CreateSM2VerifyTime2()")
