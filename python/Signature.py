from SM3 import SM3
import Utils.TransformData as tf
from Algorithm.TimesPoint import AddSub
from Utils.mathoptimize import Get_Fraction_Mod
from ECC import Point

usr = "ALICE123@YAHOO.COM"
ENTLa = "0090"
m = "message digest"
p  = "8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3"
a  = "787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498"
b  = "63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A"
n  = "8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7"
xg = "421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D"
yg = "0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2"
dA = "128B2FA8BD433C6C068C8D803DFF79792A519A55171B1B650C23661D15897263"
xa = "0AE4C7798AA0F119471BEE11825BE46202BB79E2A5844495E97C04FF4DF2548A"
ya = "7C0240F88F1CD4E16352A73C17B7F16F07353E53A176D684A9FE0C6BB798E857"
k  = "6CB28D99385C175C94F94E934817663FC176D925DD72B727260DBAAE1FB2F96F"


def CreatSM2Signature(message):
    # 生成摘要
    IDa = tf.Trans_AsciiEncode(usr)
    total_m = ENTLa + IDa + a + b + xg + yg + xa + ya
    sm3 = SM3()
    Za = sm3.CreateHv(total_m)
    ascii_m = tf.Trans_AsciiEncode(message)
    M = Za + ascii_m
    # 密码杂凑函数值
    e = sm3.CreateHv(M)
    e = tf.Trans_Bytes2Int(tf.Trans_Bits2Bytes(bin(int(e, 16)).replace('0b', '')))
    # 计算椭圆曲线点
    G = Point(xg, yg, p, a)
    point = AddSub(k, G)
    x1 = tf.Trans_Domain2Int(point.x)
    # (e + x1) mod n
    r = (e + x1) % int(n, 16)
    # s
    s = (Get_Fraction_Mod(1, (1 + int(dA, 16)), int(n, 16)) * (int(k, 16) - r * int(dA, 16))) % int(n, 16)
    return hex(r).replace('0x', '').upper(), hex(s).replace('0x', '').upper()

def CreatSM2SignatureTime():
    return CreatSM2Signature(m)

# R, S = CreatSM2Signature(m)
# print(R)
# print(S)
