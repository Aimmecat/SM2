#pragma once
#ifndef _TRANSFORMDATA_H_
#define _TRANSFORMDATA_H_

typedef struct String {
	char* data;
	char* hash;
	Register32* register_value;
	int hex_length;
	int bit_length;
} String;

String* NewString(char* data);
uint32 TransformHex2Int(char* hex);
char* Substr(char* source, int start, int n);
char* TransformInt2Hex(int num);
char* TransformInt2HexByte(int num);

#endif // !_TRANSFORMDATA_H_

