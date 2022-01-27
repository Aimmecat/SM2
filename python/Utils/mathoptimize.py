import math

"""
    for example: 1/2 mod 19
        1/2 mod 19 = n
    --> n  ≡ 1/2 mod 19
    --> 2n ≡ 1   mod 19
    --> 2n mod 19 = 1
    --> n = 10
    
    but when denominator is large, it will lose accuracy when calc 1 / denominator
    
    with Fermat's Little theorem and Extended Euclid's theorem:
    
    the fast and reliable algorithm is calculate a^(p-2) % p instead of a^(-1) % p
    
    still 1/2 mod 19:
        start: --> calc ((1 % 19) * Pow(2, 17, 19)) % p
            x = 10 k = 10001 p = 19
            1、  ret = 1 * 2 % 19 = 2, k = 1000, x = 4 % 19 = 4
            2、  ret = 2, k = 100, x = 16 % 19 = 16
            3、  ret = 2, k = 10, x = 16 * 16 % 19 = 9
            4、  ret = 2, k = 1, x = 9 * 9 % 19 = 5
            5、  ret = 2 * 5 % 19 = 10,k = 0,x = 5 * 5 % 19 = 6
            return ret = 10
        the end if 1 % 19 * 10 % 19 = 10
    
    reference: https://blog.csdn.net/godleaf/article/details/79844074?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522164284849316780271940804%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=164284849316780271940804&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-1-79844074.first_rank_v2_pc_rank_v29&utm_term=%E5%88%86%E6%95%B0%E5%8F%96%E6%A8%A1&spm=1018.2226.3001.4187
"""


# x^k
def Rapid_Mod(x, k, p):
    ret = 1
    while k:
        if k & 1:
            ret = ret * x % p
        k >>= 1
        x = (x * x) % p
    return ret


# g^a
def Rapid_Exp(g, a, p):
    e = a % (p - 1)
    if e == 0:
        return 1
    bin_e = bin(e).replace('0b', '')[1:]
    x = g
    for ei in bin_e:
        x = x * x % p
        if ei == '1':
            x = g * x % p
    return x


"""
    Get Fraction Mod, You can use it as follow:
        Get_Fraction_Mod(1, 2, 17) --> 1/2 mod 19 = 10
"""


def Get_Fraction_Mod(numerator, denominator, p):
    # return ((numerator % p) * Rapid_Exp(denominator, p - 2, p)) % p
    return ((numerator % p) * Rapid_Mod(denominator, p - 2, p)) % p


"""
    Of course, python can direct process negative number,and get -73 % 23 = 19
    This show how to process negative number
"""


def Get_Number_Mod(number, p):
    if number >= 0:
        return number % p
    else:
        return number - p * math.floor(number / p)

