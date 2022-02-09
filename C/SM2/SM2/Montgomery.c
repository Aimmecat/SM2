#include "headfile.h"

//char* R_MASK = "FF";
//char* R1 = "9";
//char* R2 = "5";
//char* _N = "E5";

char* RapidMod(char* a, char* p) {
	if (BigCompare(p, a))
		return a;
	int a_len = GetBinLength(a);
	int p_len = GetBinLength(p);
	int d_len = a_len - p_len;
	if (d_len == 0)
		return BigSub(a, p);
	char* a1;
	char* b1;
	for (int j = d_len; j >= 0; --j) {
		a1 = BigShift(a, -j);
		if (BigCompare(p, a1))
			continue;
		b1 = BigSub(a, BigShift(a1, j));
		a1 = BigSub(a1, p);
		a = BigAdd(BigShift(a1, j), b1);
	}
	return a;
}


char* BExitEuclidean(char* a, char* p) {
	char* copy_p = BigCopy(p);
	int cnt = 0;
	char* a00 = "1";
	char* a01 = "0";
	while (BigCompare(a, "1")) {
		BOOL flag_a = BigDivisible(a, 2);
		BOOL flag_p = BigDivisible(p, 2);
		if (flag_a and flag_p) {
			char* num = BigShift(BigSub(p, a), -1);
			if (BigCompare(num, a)) {
				p = num;
				a01 = BigSub(a01, a00);
				a00 = BigShift(a00, 1);
			}
			else {
				p = a;
				a = num;
				char* tmp = BigCopy(a00);
				a00 = BigSub(a01, a00);
				a01 = BigShift(tmp, 1);
			}
		}
		else if (flag_a) {
			char* num = BigShift(p, -1);
			if (BigCompare(num, a)) {
				p = num;
				a00 = BigShift(a00, 1);
			}
			else {
				p = a;
				a = num;
				char* tmp = BigCopy(a01);
				a01 = BigShift(a00, 1);
				a00 = BigCopy(tmp);
			}
		}
		else {
			a = BigShift(a, -1);
			a01 = BigShift(a01, 1);
		}
		cnt++;
	}
	for (int i = 0; i < cnt; ++i) {
		if (!BigDivisible(a00, 2)) {
			a00 = BigShift(a00, -1);
		}
		else {
			a00 = BigShift(BigAdd(a00, copy_p), -1);
		}
	}
	return a00;
}

char* RapidInverseMod(char* a, char* p) {
	a = RapidMod(a, p);
	char* x = BExitEuclidean(a, p);
	return RapidMod(x, p);
}


char* MontgomeryReduction(char* x, char* n, char* r_mask, char* _n) {
	char* m = BigAnd(BigMultilpy(BigAnd(x, r_mask), _n), r_mask);
	char* ret = BigShift(BigAdd(x, BigMultilpy(m, n)), R_BIT_LEN);
	if (BigCompare(ret, n))
		ret = BigSub(ret, n);
	return ret;
}

char* MontgomeryMod(char* a, char* n, char* r_mask, char* r1, char* _n) {
	return MontgomeryReduction(BigMultilpy(a, r1), n, r_mask, _n);
}

char* MontgomeryMultiplyMod(char* a, char* b, char* n, char* r_mask, char* r2, char* _n) {
	char* ar = MontgomeryReduction(BigMultilpy(a, r2), n, r_mask, _n);
	char* br = MontgomeryReduction(BigMultilpy(b, r2), n, r_mask, _n);
	char* abr = MontgomeryReduction(BigMultilpy(ar, br), n, r_mask, _n);
	return MontgomeryReduction(abr, n, r_mask, _n);
}

char* MontgomeryExpMod(char* a, int b, char* n, char* r_mask, char* r2, char* _n) {
	char* rs = "1";
	int length = GetBinLength(TransformInt2Hex(b));
	for (int i = length; i >= 0; --i) {
		rs = MontgomeryMultiplyMod(rs, rs, n, r_mask, r2, _n);
		if(b & (1 << i))
			rs = MontgomeryMultiplyMod(rs, a, n, r_mask, r2, _n);
	}
	return rs;
}

char* MontgomeryDivisionMod(char* a, char* b, char* n, char* r_mask, char* r2, char* _n) {
	b = RapidInverseMod(b, n);
	return MontgomeryMultiplyMod(a, b, n, r_mask, r2, _n);
}

//for test:
//char* num1 = "38901280129789113687126868FFFCCCCC780908C7986C90C808C68A9879797A";
//char* num2 = "908013280182047107FFF78799A989CBCC098A0C980A99C071BBCCAFFEEA121C";
//char* num3 = "FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF";
//char* ret1 = MontgomeryMod(num1, num3, R_MASK, R1, _N);
//char* ret2 = MontgomeryMultiplyMod(num1, num2, num3, R_MASK, R2, _N);
//char* ret3 = MontgomeryDivisionMod(num1, num2, num3, R_MASK, R2, _N);