import math
from Utils import mathoptimize

"""

    The whole Data type include:
        Bit string,
        Byte string,
        Domain element,
        Elliptic curve's Point

"""

"""
    1
    input:  
            1、 nonnegative integer x
            2、 target length: k
            (2 ** (8k) > x)
    output:
            Bytes M with length of k
"""


def Trans_Int2Bytes(x: int, k: int):
    ret = ''
    while x:
        ret = chr(x & 0xff) + ret
        x >>= 8
    if len(ret) < k:
        ret = chr(0) * (k - len(ret)) + ret
    return ret


"""
    2
    input:  
            Bytes M with length of k
    output:
            Integer x
"""


def Trans_Bytes2Int(M: str):
    ret = 0
    k = len(M)
    for idx, byte in enumerate(M):
        ret += 2 ** (8 * (k - 1 - idx)) * ord(byte)
    return ret


"""
    3
    input:  
            Bits S with length of m
    output:
            Bytes M with length of k
            
    k = ceil(m / 8)
"""


def Trans_Bits2Bytes(s: str):
    ret = ''
    k = math.ceil(len(s) / 8)
    data = '0' * int((8 * (k - len(s) / 8))) + s
    for idx in range(k):
        ret += chr(int(data[8 * idx:8 * (idx + 1)], 2))
    return ret


"""
    4
    input:  
            Bytes M with length of k
    output:
            Bits S with length of m

    m = 8k
"""


def Trans_Bytes2Bits(data: str):
    result = ''
    for byte in data:
        result += bin(ord(byte)).replace('0b', '')
    m = 8 * len(data)
    result = '0' * (m - len(result)) + result
    return result


"""
    5
    input:  
            element α in Fq
            q: value of Fq
            domain: type of Fq
            m when use GF(2^m)
    output:
            Bytes S with length of l

    L = ceil(t / 8) 
    t = ceil(log2(q))
"""


def Trans_Domain2Bytes(element, domain="prime", q=None):
    # 若q为奇素数
    if domain == "prime":
        t = math.ceil(math.log2(q))
        l = math.ceil(t / 8)
        return Trans_Int2Bytes(element, l)
    # 若q=2**m
    elif domain == "GF(2^m)":
        return Trans_Bits2Bytes(element)


"""
    6
    input:  
            domain: type of Fq
            S: length equal to ceil(t / 8), t = ceil(log2(p))
            q: value of Fq
    output:
            element α in Fq
"""


def Trans_Bytes2Domain(S: str, domain="prime", q=None):
    # 若q为奇素数
    if domain == "prime":
        alpha = Trans_Bytes2Int(S)
        if not 0 <= alpha <= q - 1:
            Exception("Error!")
        return alpha
    # 若q=2**m
    elif domain == "GF(2^m)":
        return Trans_Bytes2Bits(S)


"""
    7
    input:  
            element α in Fq
            domain: type of Fq
    output:
            integer x
"""


def Trans_Domain2Int(element, domain="prime"):
    # 若q为奇素数
    if domain == "prime":
        return element
    # 若q=2**m
    elif domain == "GF(2^m)":
        return int(element, 2)


"""
    8
    input:  
            point P (xp,yp)
            domain: type of Fq
            p: degree
            q: value of Fq
            compress_type: compress type
    output:
            Bytes S
"""


def Trans_Point2Bytes(xp, yp, p, q, compress="No", domain="prime"):
    S = ''
    yp_head = None
    X1 = Trans_Domain2Bytes(xp, domain, q)
    # 若q为奇素数
    if domain == "prime":
        yp_head = yp[-1:]
    # 若q=2**m
    elif domain == "GF(2^m)":
        if xp == '0':
            yp_head = '0'
        else:
            yp_head = mathoptimize.Get_Fraction_Mod(int(yp, 2), int(xp, 2), p)
    # 压缩形式
    if compress == "Yes":
        if yp_head == 0:
            PC = '02'
        else:
            PC = '03'
        S = PC + X1
    # 未压缩形式
    elif compress == "No":
        Y1 = Trans_Domain2Bytes(yp, q, domain)
        PC = '04'
        S = PC + X1 + Y1
    # 混合表示形式
    elif compress == "Mix":
        Y1 = Trans_Domain2Bytes(yp, q, domain)
        if yp_head == 0:
            PC = '06'
        else:
            PC = '07'
        S = PC + X1 + Y1
    return S


"""
    9
    input:  
           a,
           b,
           S,
           compress:,
    output:
            point P xp,yp
"""


def Trans_Bytes2Point(a, b, q, domain, compress, S):
    l = math.ceil(math.log2(q) / 8)
    PC = S[0]
    X1 = None
    Y1 = None
    yp = None
    # 压缩形式
    if compress == "Yes":
        X1 = S[1:]
    # 未压缩或混合
    elif compress == "No" or compress == "Mix":
        X1 = S[1:l + 1]
        Y1 = S[l + 1:]
    xp = Trans_Bytes2Domain(X1, domain, q)
    # 压缩形式
    if compress == "Yes":
        if PC == chr(2):
            yp_head = '0'''
        elif PC == chr(3):
            yp_head = '1'
        # 未完成计算yp
    # 未压缩形式
    elif compress == "No":
        yp = Trans_Bytes2Domain(Y1, domain, q)
    # 混合表示形式
    elif compress == "Mix":
        yp = Trans_Bytes2Domain(Y1, domain, q)
    if domain == "prime":
        pass  # 未完成检验
    elif domain == "GF(2^m)":
        pass  # 未完成检验
    return xp, yp


def Trans_SingleBin2Hex(data: str):
    return hex(int(data, 2)).replace('0x', '')


def Trans_SingleHex2Bin(data: str):
    return bin(int(data, 16)).replace('0b', '')


def Trans_Bin2Hex(data: str):
    ret = ''
    length = len(data)
    data = '0' * (4 - length % 4) + data
    length = int(len(data) / 4)
    for idx in range(length):
        ret += Trans_SingleBin2Hex(data[idx * 4: (idx + 1) * 4])
    return ret


"""
    example: 
        m = 'Hello'
        ret = Trans_AsciiEncode(m)
        print(ret)
        
        ret = '48656c6c6f'
"""


def Trans_AsciiEncode(m: str):
    ret = ""
    for char in m:
        add = bin(ord(char)).replace('0b', '')
        add = '0' * (8 - len(add)) + add
        ret += add
    return hex(int(ret, 2)).replace('0x', '')


"""
    example:
        m = '48656c6c6f'
        ret = Trans_AsciiDecode(m)
        print(ret)
        
        ret = 'Hello'
"""


def Trans_AsciiDecode(m: str):
    ret = ""
    l = len(m) // 2
    for i in range(l):
        ret += chr(int(m[i * 2: (i + 1) * 2], 16))
    return ret


"""
    example:
        m = 'AABBCCDDEEFF'
        ret = Beauty_Show_Hex(m)
        print(ret)
        
        ret = '0000AABB CCDDEEFF'
"""


def Beauty_Show_Hex(m: str):
    ret = ''
    l = math.ceil(len(m) / 8)
    m = '0' * (8 * l - len(m)) + m
    cnt = 0
    for single_hex in m:
        ret += single_hex
        cnt += 1
        if cnt == 8:
            ret += ' '
            cnt = 0
    return ret

