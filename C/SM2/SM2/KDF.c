#include "headfile.h"

char* KDF(char* Z, int k_len) {
	uint32 cnt = 1;
	int length = (int)(k_len / V);
	char* k = (char*)calloc((length + 1) << 6, sizeof(char));
	for (int i = 0; i < length; ++i) {
		char* byte_cnt = TransformInt2HexByte(cnt);
		char* z_t = (char*)calloc(80, sizeof(char));
		strcat(z_t, Z);
		strcat(z_t, byte_cnt);
		String* newinfo = NewString(z_t);
		CreateHv(newinfo);
		strcat(k, newinfo->hash);
		cnt++;
	}
	char* byte_cnt = TransformInt2HexByte(cnt);
	char* z_t = (char*)calloc(80, sizeof(char));
	strcat(z_t, Z);
	strcat(z_t, byte_cnt);
	String* newinfo = NewString(z_t);
	CreateHv(newinfo);
	if (k_len % V != 0) {
		int tail = (k_len - V * (int)(k_len / V) + 1) >> 2;
		strcat(k, Substr(newinfo->hash, 0, tail));
	}
	else {
		strcat(k, newinfo->hash);
	}
	return k;
}