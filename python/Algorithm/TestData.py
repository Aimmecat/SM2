import random
import Algorithm.Montgomery as mg
import time as t
from Utils.mathoptimize import Get_Fraction_Mod

"""
    生成测试的随机数列表
    范围: 2 ** 256 ~ 2 ** 512
"""

l = 2000

def CreateRandomNumber(start=2 ** 256 - 10000, end=2 ** 256):
    global l
    a = []
    b = []
    for i in range(l):
        a.append(random.randint(start, end))
        b.append(random.randint(start, end))
    return a, b


if __name__ == "__main__":
    a, b = CreateRandomNumber()
    n = int('8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3', 16)

    # 蒙哥马利预计算
    r, r1, r2, _n = mg.MontgomeryPreCalculate(n, 512)

    print("----------------------------------------------------------------")
    print('a mod n')

    ret = []
    ret1 = []
    ret2 = []

    # 快速模、蒙哥马利模验证与测速
    t1 = t.time()
    for idx in range(l):
        ret.append(a[idx] % n)
    t2 = t.time()

    print('build in function use time \t:' + str((t2 - t1) * 1000 / l) + 'ms')

    t3 = t.time()
    for idx in range(l):
        ret1.append(mg.RapidMod(a[idx], n)[1])
    t4 = t.time()

    print('Rapid method use time:     \t:' + str((t4 - t3) * 1000 / l) + 'ms')

    t5 = t.time()
    for idx in range(l):
        ret2.append(mg.MontgomeryMod(a[idx], n, r, r1, _n))
    t6 = t.time()

    print('Montgomery method use time \t:' + str((t6 - t5) * 1000 / l) + 'ms')

    print('The result of Rapid method is ' + str(ret == ret1))
    print('The result of Montgomery method is ' + str(ret == ret2))

    print("----------------------------------------------------------------")
    print('a * b mod n')

    ret = []
    ret1 = []
    ret2 = []

    # 快速模乘、蒙哥马利模乘验证与测速
    t1 = t.time()
    for idx in range(l):
        ret.append(a[idx] * b[idx] % n)
    t2 = t.time()

    print('build in function use time \t:' + str((t2 - t1) * 1000 / l) + 'ms')

    t3 = t.time()
    for idx in range(l):
        ret1.append(mg.RapidMultiplyMod(a[idx], b[idx], n))
    t4 = t.time()

    print('Rapid method use time:     \t:' + str((t4 - t3) * 1000 / l) + 'ms')

    t5 = t.time()
    for idx in range(l):
        ret2.append(mg.MontgomeryMultiplyMod(a[idx], b[idx], n, r, r2, _n))
    t6 = t.time()

    print('Montgomery method use time \t:' + str((t6 - t5) * 1000 / l) + 'ms')

    print('The result of Rapid method is ' + str(ret == ret1))
    print('The result of Montgomery method is ' + str(ret == ret2))

    print("----------------------------------------------------------------")
    print('a / b mod n')

    ret = []
    ret1 = []
    ret2 = []

    # 快速模除、蒙哥马利模除验证与测速
    t1 = t.time()
    for idx in range(l):
        ret.append(Get_Fraction_Mod(a[idx], b[idx], n))
    t2 = t.time()

    print('Rapid method use time:     \t:' + str((t2 - t1) * 1000 / l) + 'ms')

    t3 = t.time()
    for idx in range(l):
        ret1.append(mg.MontgomeryDivisionMod(a[idx], b[idx], n, r, r1, r2, _n))
    t4 = t.time()

    print('Montgomery method1 use time\t:' + str((t4 - t3) * 1000 / l) + 'ms')

    t5 = t.time()
    for idx in range(l):
        ret2.append(mg.MontgomeryDivisionMod2(a[idx], b[idx], n, r,  r2, _n))
    t6 = t.time()

    print('Montgomery method2 use time\t:' + str((t6 - t5) * 1000 / l) + 'ms')

    print('The result of Rapid method is ' + str(ret == ret1))
    print('The result of Montgomery method1 is ' + str(ret == ret1))
    print('The result of Montgomery method2 is ' + str(ret == ret2))

    # print("----------------------------------------------------------------")
    # print('a ** b mod n')
    #
    # ret = []
    # ret1 = []
    # ret2 = []

    # 快速模幂、 蒙哥马利模幂测速与验证
    # t1 = t.time()
    # for idx in range(l):
    #     ret.append(a[idx] ** b[idx] % n)
    # t2 = t.time()
    #
    # print('build in function use time:\t' + str((t2 - t1) * 1000 / l) + 'ms')

    # t3 = t.time()
    # for idx in range(l):
    #     ret1.append(mg.RapidPowerMod(a[idx], b[idx], n))
    # t4 = t.time()
    #
    # print('Rapid method use time:     \t:' + str((t4 - t3) * 1000 / l) + 'ms')
    #
    # t5 = t.time()
    # for idx in range(l):
    #     ret2.append(mg.MontgomeryExpMod(a[idx], b[idx], n, r, r2, _n))
    # t6 = t.time()
    #
    # print('Montgomery method use time:\t:' + str((t6 - t5) * 1000 / l) + 'ms')
    #
    # print('The result of Rapid method is ' + str(ret1 == ret2))
    # print('The result of Montgomery method is ' + str(ret1 == ret2))

