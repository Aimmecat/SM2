#pragma once
#ifndef _SM2_H_
#define _SM2_H_

typedef struct SignatureInfo {
	char* SignatureR;
	char* SignatureS;
}SignatureInfo;

SignatureInfo* Signature(char* IDa, char* ENTLa, char* m, char* xa, char* ya, char* dA);
char* Verify(char* r, char* s, char* m, char* xa, char* ya);
char* Encryption(char* m, char* xa, char* ya);
char* Decryption(char* m, char* dA, int k_len);
char* CreateC1(char* x, char* y);

#endif // !_SM2_H_
