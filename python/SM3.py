from Utils.Foundation import Register32
import time
import cProfile

"""
    Reference: https://wenku.baidu.com/view/8d67d80178563c1ec5da50e2524de518964bd3b6.html?qq-pf-to=pcqq.c2c
"""


class SM3(object):
    DEBUG = False

    def __init__(self):
        # Init Register
        self.A = Register32('7380166F')
        self.B = Register32('4914b2b9')
        self.C = Register32('172442d7')
        self.D = Register32('da8a0600')
        self.E = Register32('a96f30bc')
        self.F = Register32('163138aa')
        self.G = Register32('e38dee4d')
        self.H = Register32('b0fb0e4e')
        self.SS1 = Register32('00000000')
        self.SS2 = Register32('00000000')
        self.TT1 = Register32('00000000')
        self.TT2 = Register32('00000000')
        self.V = '7380166F4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e'

    def init(self):
        self.A = Register32('7380166F')
        self.B = Register32('4914b2b9')
        self.C = Register32('172442d7')
        self.D = Register32('da8a0600')
        self.E = Register32('a96f30bc')
        self.F = Register32('163138aa')
        self.G = Register32('e38dee4d')
        self.H = Register32('b0fb0e4e')
        self.SS1 = Register32('00000000')
        self.SS2 = Register32('00000000')
        self.TT1 = Register32('00000000')
        self.TT2 = Register32('00000000')
        self.V = '7380166F4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e'

    def CF(self, Bi):
        w = []
        ws = []
        for idx in range(16):
            word = hex(int(Bi[32 * idx: 32 * (idx + 1)], 2)).replace('0x', '')
            w.append(Register32(word))
        for idx in range(16, 68):
            val = P(w[idx - 16] ^ w[idx - 9] ^ (w[idx - 3] << 15), 1)
            val = val ^ (w[idx - 13] << 7)
            val = val ^ w[idx - 6]
            w.append(val)
        for idx in range(64):
            ws.append(w[idx] ^ w[idx + 4])
        for j in range(64):
            Tj = Get_Tj(j)
            self.SS1 = ((self.A << 12) + self.E + (Tj << j)) << 7
            self.SS2 = self.SS1 ^ (self.A << 12)
            self.TT1 = FF(self.A, self.B, self.C, j) + self.D + self.SS2 + ws[j]
            self.TT2 = GG(self.E, self.F, self.G, j) + self.H + self.SS1 + w[j]
            self.D = self.C
            self.C = self.B << 9
            self.B = self.A
            self.A = self.TT1
            self.H = self.G
            self.G = self.F << 19
            self.F = self.E
            self.E = P(self.TT2, 0)

    def CreateHv(self, m):
        self.init()
        # Storage input message
        m = Get_Message(m)
        length = len(m) // 512
        for i in range(length):
            Bi = m[i * 512: (i + 1) * 512]
            self.CF(Bi)
            V = self.A.value + self.B.value + self.C.value + self.D.value \
                + self.E.value + self.F.value + self.G.value + self.H.value
            self.V = hex(int(self.V, 16) ^ int(V, 16)).replace('0x', '')
            self.V = '0' * (64 - len(self.V)) + self.V
            self.A = Register32(self.V[0:8])
            self.B = Register32(self.V[8:16])
            self.C = Register32(self.V[16:24])
            self.D = Register32(self.V[24:32])
            self.E = Register32(self.V[32:40])
            self.F = Register32(self.V[40:48])
            self.G = Register32(self.V[48:56])
            self.H = Register32(self.V[56:64])
        return self.V.upper()


def Get_Tj(j):
    if 0 <= j <= 15:
        return Register32('79cc4519')
    elif 16 <= j <= 63:
        return Register32('7a879d8a')


def FF(X: Register32, Y: Register32, Z: Register32, j):
    if 0 <= j <= 15:
        return X ^ Y ^ Z
    elif 16 <= j <= 63:
        return (X & Y) | (X & Z) | (Y & Z)


def GG(X: Register32, Y: Register32, Z: Register32, j):
    if 0 <= j <= 15:
        return X ^ Y ^ Z
    elif 16 <= j <= 63:
        return (X & Y) | (X.BitReverse() & Z)


def P(X: Register32, label=0):
    if label == 0:
        return X ^ (X << 9) ^ (X << 17)
    elif label == 1:
        return X ^ (X << 15) ^ (X << 23)


def Get_Message(m):
    bin_m = bin(int(m, 16)).replace('0b', '')
    bin_m = (4 * len(m) - len(bin_m)) * '0' + bin_m
    length = len(bin_m)
    length_bit = bin(length).replace('0b', '')
    cnt = 1
    while 512 * cnt <= length:
        cnt += 1
    init_m = bin_m + '1' + '0' * (512 * cnt - 1 - len(length_bit) - length) + length_bit
    return init_m


"""
    This Demo is given by the SM3 standard 
"""

loop = 1000
m1 = '616263'
m2 = '61626364616263646162636461626364616263646162636461626364616263646162636461626364616263646162636461626364616263646162636461626364'
Test = SM3()


def TestTimeConsume1():
    solve1 = None
    start1 = time.time()
    for i in range(loop):
        solve1 = Test.CreateHv(m1)
    end1 = time.time()
    print("Input 616263:")
    print("You should get:" + '66c7f0f462eeedd9d1f2d46bdc10e4e24167c4875cf2f7a2297da02b8f4ba8e0'.upper())
    print("You real   get:" + solve1)
    print("The Result is:" + str(solve1 == '66c7f0f462eeedd9d1f2d46bdc10e4e24167c4875cf2f7a2297da02b8f4ba8e0'.upper()))
    print("It costs time:" + str((end1 - start1) * 1000) + ' ms')


def TestTimeConsume2():
    solve2 = None
    start2 = time.time()
    for i in range(loop):
        solve2 = Test.CreateHv(m2)
    end2 = time.time()
    print(
        "Input 61626364616263646162636461626364616263646162636461626364616263646162636461626364616263646162636461626364616263646162636461626364:")
    print("You should get:" + "debe9ff92275b8a138604889c18e5a4d6fdb70e5387e5765293dcba39c0c5732".upper())
    print("You real   get:" + solve2)
    print("The Result is:" + str(solve2 == 'debe9ff92275b8a138604889c18e5a4d6fdb70e5387e5765293dcba39c0c5732'.upper()))
    print("It costs time:" + str((end2 - start2) * 1000) + ' ms')


if __name__ == "__main__":
    TestTimeConsume1()
    # cProfile.run("TestTimeConsume1()")
    print('--------------------------------------------------------------------------------------------------')
    TestTimeConsume2()
    # cProfile.run("TestTimeConsume2()")
