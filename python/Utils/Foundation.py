class Register32(object):
    TYPE = 32
    LEN = 8

    def __init__(self, value: str):
        if len(value) <= self.LEN:
            self.value = (self.LEN - len(value)) * '0' + value
        else:
            self.value = value[-self.LEN:]

    def __str__(self):
        return 'Hex:\t' + "'" + self.value.upper() + "'\t" + 'Type:' + str(self.TYPE) + 'bit' \
               + '\tBin:' + self.GetBinDisplay()

    __repr__ = __str__

    def __add__(self, other):
        sum_value = hex(int(self.value, 16) + int(other.value, 16)).replace('0x', '')
        return Register32(sum_value)

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __truediv__(self, other):
        pass

    def __and__(self, other):
        value = hex(int(self.value, 16) & int(other.value, 16)).replace('0x', '')
        value = (self.LEN - len(value)) * '0' + value
        return Register32(value)

    def __or__(self, other):
        value = hex(int(self.value, 16) | int(other.value, 16)).replace('0x', '')
        value = (self.LEN - len(value)) * '0' + value
        return Register32(value)

    def __xor__(self, other):
        value = hex(int(self.value, 16) ^ int(other.value, 16)).replace('0x', '')
        value = (self.LEN - len(value)) * '0' + value
        return Register32(value)

    def __eq__(self, other):
        self.value = other.value

    def __lshift__(self, b):
        b %= self.TYPE
        value = bin(int(self.value, 16)).replace('0b', '')
        value = '0' * (self.TYPE - len(value)) + value
        creat_value = hex(int(value[b:] + value[0:b], 2)).replace('0x', '')
        creat_value = '0' * (self.LEN - len(creat_value)) + creat_value
        return Register32(creat_value)

    def __rshift__(self, b):
        b %= self.TYPE
        value = bin(int(self.value, 16)).replace('0b', '')
        value = '0' * (self.TYPE - len(value)) + value
        creat_value = hex(int(value[self.TYPE - b:] + value[0:self.TYPE - b], 2)).replace('0x', '')
        creat_value = '0' * (self.LEN - len(creat_value)) + creat_value
        return Register32(creat_value)

    def GetBinDisplay(self):
        bin_display = bin(int(self.value, 16)).replace('0b', '')
        bin_display = (self.TYPE - len(bin_display)) * '0' + bin_display
        new_bin_display = ""
        cnt = 1
        for bins in bin_display:
            new_bin_display += bins
            cnt += 1
            if cnt == 5:
                new_bin_display += ' '
                cnt = 1
        return new_bin_display

    def BitReverse(self):
        bin_value = bin(int(self.value, 16)).replace('0b', '')
        bin_value = (self.TYPE - len(bin_value)) * '0' + bin_value
        reverse_bit_value = ""
        for bins in bin_value:
            if bins == "0":
                reverse_bit_value += "1"
            else:
                reverse_bit_value += "0"
        reverse_value = hex(int(reverse_bit_value, 2)).replace('0x', '')
        return Register32(reverse_value)


# A = Register32('77FF99CC')
# B = Register32('99331100')
# print(A)
# print(B)
# print(A + B)
# print(A ^ B)
# print(A | B)
# print(A & B)
# print(A.BitReverse())
# print(A << 4)
# print(A >> 8)
