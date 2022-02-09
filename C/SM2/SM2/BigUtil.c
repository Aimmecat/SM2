#include "headfile.h"

miracl* mip;

char* BigAdd(char* num1, char* num2) {
	int max_len = max(strlen(num1),strlen(num2));
	mip->IOBASE = 16;
	big big_num1 = mirvar(0);
	big big_num2 = mirvar(0);
	big big_ret = mirvar(0);
	cinstr(big_num1, num1);
	cinstr(big_num2, num2);
	add(big_num1, big_num2, big_ret);
	char* ret = (char*)calloc(max_len + 1, sizeof(char));
	cotstr(big_ret, ret);
	return ret;
}

char* BigSub(char* num1, char* num2) {
	int max_len = max(strlen(num1), strlen(num2));
	mip->IOBASE = 16;
	big big_num1 = mirvar(0);
	big big_num2 = mirvar(0);
	big big_ret = mirvar(0);
	cinstr(big_num1, num1);
	cinstr(big_num2, num2);
	subtract(big_num1, big_num2, big_ret);
	char* ret = (char*)calloc(max_len + 1, sizeof(char));
	cotstr(big_ret, ret);
	return ret;
}

char* BigMultilpy(char* num1, char* num2) {
	int max_len = max(strlen(num1), strlen(num2));
	mip->IOBASE = 16;
	big big_num1 = mirvar(0);
	big big_num2 = mirvar(0);
	big big_ret = mirvar(0);
	cinstr(big_num1, num1);
	cinstr(big_num2, num2);
	multiply(big_num1, big_num2, big_ret);
	char* ret = (char*)calloc(max_len << 1, sizeof(char));
	cotstr(big_ret, ret);
	return ret;
}

char* GetComplement(char* num) {
	int length = strlen(num);
	char* copy_num = BigCopy(num);
	for (int i = 0; i < length; ++i) {
		copy_num[i] = 'F';
	}
	char* new_num = BigSub(copy_num, num);
	new_num = BigAdd(new_num, "1");
	return new_num;
}

char* BigAnd(char* num1, char* num2) {
	int max_len = max(strlen(num1), strlen(num2));
	if(num1[0] == '-'){
		num1 = GetComplement(Substr(num1, 1, strlen(num1) - 1));
	}
	if (num2[0] == '-') {
		num2 = GetComplement(Substr(num2, 1, strlen(num2) - 1));
	}
	mip->IOBASE = 16;
	big big_num1 = mirvar(0);
	big big_num2 = mirvar(0);
	big big_ret = mirvar(0);
	cinstr(big_num1, num1);
	cinstr(big_num2, num2);
	mr_and(big_num1, big_num2, big_ret);
	char* ret = (char*)calloc(max_len << 1, sizeof(char));
	cotstr(big_ret, ret);
	return ret;
}

char* BigXor(char* num1, char* num2) {
	int max_len = max(strlen(num1), strlen(num2));
	if (num1[0] == '-') {
		num1 = GetComplement(Substr(num1, 1, strlen(num1) - 1));
	}
	if (num2[0] == '-') {
		num2 = GetComplement(Substr(num2, 1, strlen(num2) - 1));
	}
	mip->IOBASE = 16;
	big big_num1 = mirvar(0);
	big big_num2 = mirvar(0);
	big big_ret = mirvar(0);
	cinstr(big_num1, num1);
	cinstr(big_num2, num2);
	mr_xor(big_num1, big_num2, big_ret);
	char* ret = (char*)calloc(max_len << 1, sizeof(char));
	cotstr(big_ret, ret);
	return ret;
}


char* BigShift(char* num, int shift) {
	int len = strlen(num);
	if (shift > 0)
		len += (shift >> 2) + 1;
	mip->IOBASE = 16;
	big big_num = mirvar(0);
	big big_ret = mirvar(0);
	cinstr(big_num, num);
	sftbit(big_num, shift, big_ret);
	char* ret = (char*)calloc(len, sizeof(char));
	cotstr(big_ret, ret);
	return ret;
}

BOOL BigCompare(char* num1, char* num2) {
	mip->IOBASE = 16;
	big big_num1 = mirvar(0);
	big big_num2 = mirvar(0);
	cinstr(big_num1, num1);
	cinstr(big_num2, num2);
	BOOL ret = mr_compare(big_num1, big_num2) == 1 ? TRUE : FALSE;
	return ret;
}

char* BigCopy(char* num) {
	int len = strlen(num);
	mip->IOBASE = 16;
	big big_num = mirvar(0);
	big big_ret = mirvar(0);
	cinstr(big_num, num);
	copy(big_num, big_ret);
	char* ret = (char*)calloc(len, sizeof(char));
	cotstr(big_ret, ret);
	return ret;
}

BOOL BigDivisible(char* num1, int n) {
	mip->IOBASE = 16;
	big big_num1 = mirvar(0);
	cinstr(big_num1, num1);
	BOOL ret = subdivisible(big_num1, n) == TRUE ? FALSE : TRUE;
	return ret;
}

int GetBinLength(char* num) {
	int length = strlen(num);
	char* p = num;
	while (*p == '0') {
		p++;
		length--;
	}
	length = (length - 1) << 2;
	if (*p <= '1') {
		length += 1;
	}
	else if (*p <= '3') {
		length += 2;
	}
	else if (*p <= '7') {
		length += 3;
	}
	else length += 4;
	return length;
}



//for test:
//char* num1 = "2183974919283412";
//char* num2 = "8129379512351231";
//GetBinLength(num1);
//BigDivisible("B", "2");
//BigAdd(num1, num2);
//BigSub(num2, num1);
//BigMultilpy(num1, num2);
//BigShift(num1, -8);
//BigAnd(num1, num2);
//BigCompare(num2, "1");