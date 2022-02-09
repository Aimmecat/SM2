#include "headfile.h"

char* CreateE(char* IDa, char* ENTLa, char* m, char* xa, char* ya) {
	int length_IDa = strlen(IDa);
	int length_ENTLa = strlen(IDa);
	int length_m = strlen(IDa);
	char* total_m = (char*)calloc(length_IDa + length_ENTLa + length_m + 193, sizeof(char));
	strcat(total_m, ENTLa);
	strcat(total_m, IDa);
	strcat(total_m, sm2_a);
	strcat(total_m, sm2_b);
	strcat(total_m, sm2_xg);
	strcat(total_m, sm2_yg);
	strcat(total_m, xa);
	strcat(total_m, ya);
	String* Za = NewString(total_m);
	char* Za_hash = CreateHv(Za);
	char* ascii_m = Trans_AsciiEncode(m);
	strcat(Za_hash, ascii_m);
	String* M = NewString(Za_hash);
	return CreateHv(M);
}

SignatureInfo* Signature(char* IDa, char* ENTLa, char* m, char* xa, char* ya, char* dA) {
	char* e = CreateE(IDa, ENTLa, m, xa, ya);
	Point* SM2_G = CreateNewPoint(sm2_xg, sm2_yg, "1", JacobiPoint);
	char* k = CreateRandomK();
	JacobiSlideWindowPlusPreCalc(SM2_G);
	Point* point = JacobiPoint2BasicPoint(JacobiSlideWindowPlus(k));
	char* r = MontgomeryMod(BigAdd(e, point->x), sm2_n, SIGNATURE_RMASK, SIGNATURE_R1, SIGNATURE_N);
	char* inv_dA = MontgomeryDivisionMod("1", BigAdd("1", dA), sm2_n, SIGNATURE_RMASK, SIGNATURE_R2, SIGNATURE_N);
	char* s = MontgomeryMultiplyMod(inv_dA, BigSub(k, MontgomeryMultiplyMod(r, dA, sm2_n, SIGNATURE_RMASK, SIGNATURE_R2, SIGNATURE_N)), sm2_n, SIGNATURE_RMASK, SIGNATURE_R2, SIGNATURE_N);
	SignatureInfo* signature_info;
	signature_info->SignatureR = r;
	signature_info->SignatureS = s;
	return signature_info;
}

char* Verify(char* r, char* s, char* m, char* xa, char* ya) {
	String* e = NewString(m);
	CreateHv(e);
	char* t = MontgomeryMod(BigAdd(r, s), sm2_n, SIGNATURE_RMASK, SIGNATURE_R1, SIGNATURE_N);
	Point* SM2_G = CreateNewPoint(sm2_xg, sm2_yg, "1", JacobiPoint);
	JacobiSlideWindowPlusPreCalc(SM2_G);
	Point* point1 = JacobiPoint2BasicPoint(JacobiSlideWindowPlus(s));
	Point* PA = CreateNewPoint(xa, ya, "1", JacobiPoint);
	JacobiSlideWindowPlusPreCalc(PA);
	Point* point2 = JacobiPoint2BasicPoint(JacobiSlideWindowPlus(t));
	char* ret = MontgomeryMod(BigAdd(e, point2->x), sm2_n, SIGNATURE_RMASK, SIGNATURE_R1, SIGNATURE_N);
	return ret;
}

char* Encryption(char* m, char* xa, char* ya) {
	Point* SM2_G = CreateNewPoint(sm2_xg, sm2_yg, "1", JacobiPoint);
	char* k = CreateRandomK();
	JacobiSlideWindowPlusPreCalc(SM2_G);
	Point* point1 = JacobiPoint2BasicPoint(JacobiSlideWindowPlus(k));

	char* C1 = BigCopy("04");
	strcat(C1, point1->x);
	strcat(C1, point1->y);

	Point* PA = CreateNewPoint(xa, ya, "1", JacobiPoint);
	JacobiSlideWindowPlusPreCalc(PA);
	Point* point2 = JacobiPoint2BasicPoint(JacobiSlideWindowPlus(k));
	char* M = Trans_AsciiEncode(m);
	int k_len = strlen(M) << 2;
	
	char* tmp1 = BigCopy(point2->x);
	strcat(tmp1, point2->y);
	char* t = KDF(tmp1, k_len);
	char* C2 = BigXor(M, t);

	char* tmp2 = BigCopy(point2->x);
	strcat(tmp1, M);
	strcat(tmp1, point2->y);
	String* c3 = NewString(tmp2);
	char* C3 = CreateHv(c3);

	strcat(C1, C3);
	strcat(C1, C2);
	return C1;
}

char* Decryption(char* m, char* dA, int k_len) {
	char* C1 = Substr(m, 2, 128);
	char* C3 = Substr(m, 130, 64);
	char* C2 = Substr(m, 194, strlen(m) - 194);
	char* x = Substr(C1, 0, 64);
	char* y = Substr(C1, 64, 64);
	Point* point = CreateNewPoint(x, y, "1", JacobiPoint);
	JacobiSlideWindowPlusPreCalc(point);
	point = JacobiPoint2BasicPoint(JacobiSlideWindowPlus(dA));
	
	char* tmp1 = BigCopy(point->x);
	strcat(tmp1, point->y);

	char* t = KDF(tmp1, k_len);
	char* M = BigXor(C2, t);

	char* tmp2 = BigCopy(point->x);
	strcat(tmp1, M);
	strcat(tmp1, point->y);
	String* u = NewString(tmp2);
	char* U = CreateHv(u);

	return U;
}