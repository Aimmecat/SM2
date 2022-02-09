from SM3 import SM3
from SM2 import GetSM2Parameter, GetK
import Utils.TransformData as tf
from ECC import Point
import Algorithm.Montgomery as mg
import cProfile

ENTLa = "0080"
m = "message digest"
IDa = '31323334 35363738 31323334 35363738'.replace(' ', '')
dA = "3945208F 7B2144B1 3F36E38A C6D39F95 88939369 2860B51A 42FB81EF 4DF7C5B8".replace(' ', '')
xa = "09F9DF31 1E5421A1 50DD7D16 1E4BC5C6 72179FAD 1833FC07 6BB08FF3 56F35020".replace(' ', '')
ya = "CCEA490C E26775A5 2DC6EA71 8CC1AA60 0AED05FB F35E084A 6632F607 2DA9AD13".replace(' ', '')

r0 = 115792089237316195423570985008687907853269984665640564039457584007913129639936
r1 = 26959946667150639794667015087208360940682819471613774651619690594013
r2 = 13890758876747366292380987140861871730726264343299237038422391206777195679520
_n = 50307568889517732031517334307777217170252470892231192406845782083964144781685

preZa = 'B2E14C5C79C6DF5B85F4FE7ED8DB7A262B9DA7E07CCB0EA9F4747B8CCDA8A4F3'


def CreatSM2Signature(IDa, ENTLa, message, xa, ya, dA):
    # 获取参数
    p, a, b, n, xg, yg = GetSM2Parameter()
    # 生成摘要
    total_m = ENTLa + IDa + a + b + xg + yg + xa + ya
    sm3 = SM3()
    Za = sm3.CreateHv(total_m)
    Za = preZa
    ascii_m = tf.Trans_AsciiEncode(message)
    M = Za + ascii_m
    # 密码杂凑函数值
    e = sm3.CreateHv(M)
    e = tf.Trans_Bytes2Int(tf.Trans_Bits2Bytes(bin(int(e, 16)).replace('0b', '')))
    # 计算椭圆曲线点
    G = Point(xg, yg, p, a)
    k = GetK("signature")
    point = G.PointMultiply(k)
    x1 = tf.Trans_Domain2Int(point.x)
    # (e + x1) mod n
    r = (e + x1) % int(n, 16)
    # s
    inv_dA = mg.MontgomeryDivisionMod(1, 1 + int(dA, 16), int(n, 16), r0, r1, r2, _n)
    s = mg.MontgomeryMultiplyMod(inv_dA, int(k, 16) - r * int(dA, 16), int(n, 16), r0, r2, _n)
    return hex(r).replace('0x', '').upper(), hex(s).replace('0x', '').upper()


def CreatSM2SignatureTime():
    ret = CreatSM2Signature(IDa=IDa,
                            ENTLa=ENTLa,
                            message=m,
                            xa=xa,
                            ya=ya,
                            dA=dA)
    return ret


def CreatSM2SignatureTime2():
    for i in range(10):
        CreatSM2Signature(IDa=IDa,
                          ENTLa=ENTLa,
                          message=m,
                          xa=xa,
                          ya=ya,
                          dA=dA)


if __name__ == "__main__":
    cProfile.run("CreatSM2SignatureTime2()")
