#include "headfile.h"

String* NewString(char* data) {
	String* string = malloc(sizeof(String));
	if (string != NULL) {
		string->hex_length = strlen(data);
		string->bit_length = string->hex_length << 2;
		// 计数总共需要多少比特
		int cnt = 1;
		while ((cnt << 7) <= string->hex_length)cnt++;
		

		// 计数要补的长度字符
		int cnt_length = 1;
		while ((1 << (cnt_length << 2)) <= string->bit_length)cnt_length++;
		char* hexlength = TransformInt2Hex(string->bit_length);

		// 计算需要补的0的个数并生成对应字符串
		int align = (cnt << 7) - 1 - string->hex_length - cnt_length;
		char* align_zero = (char*)calloc(align, sizeof(char));
		for (int i = 0; i < align; ++i) {
			strcat(align_zero, "0");
		}

		string->hex_length = (cnt << 7);
		string->data = (char*)calloc(string->hex_length, sizeof(char));
		strcat(string->data, data);
		strcat(string->data, "8");
		strcat(string->data, align_zero);
		strcat(string->data, hexlength);

		int size = string->hex_length >> 3;
		string->register_value = (Register32*) calloc(size, sizeof(Register32));
		for (int i = 0; i < size; ++i) {
			char* value = Substr(string->data, 8 * i, 8);
			*(string->register_value + i) = TransformHex2Int(value);
		}
	}
	return string;
}


uint32 TransformHex2Int(char* hex) {
	uint32 ret = 0;
	int num = 0;
	for (int i = 0; i < 8; ++i) {
		num = (hex[i] >= 'A') ? Int16(hex[i]) : Int10(hex[i]);
		ret += num * (1 << ((7 - i) << 2));
	}
	return ret;
}

char* TransformInt2Hex(int num) {
	char* ret = (char*)calloc(16, sizeof(char));
	char* symbol = "0123456789ABCDEF";
	int cnt = 1;
	while ((1 << (cnt << 2)) <= num)cnt++;
	ret = ret + cnt;
	*(ret--) = '\0';
	for (int i = 0; i < cnt; ++i) {
		int idx = num - ((num >> 4) << 4);
		num = num >> 4;
		*(ret--) = *(symbol + idx);
	}
	ret += 1;
	return ret;
}

char* TransformInt2HexByte(int num) {
	char* ret = (char*)calloc(16, sizeof(char));
	char* symbol = "0123456789ABCDEF";
	ret = ret + 8;
	*(ret--) = '\0';
	for (int i = 0; i < 8; ++i) {
		int idx = num - ((num >> 4) << 4);
		num = num >> 4;
		*(ret--) = *(symbol + idx);
	}
	ret += 1;
	return ret;
}

char* Substr(char* source, int start, int n) {
	char* p = (char*) calloc(16, sizeof(char));
	char* ret = p;
	char* q = source + start;
	while (n--) {
		*(p++) = *(q++);
	}
	*(p++) = '\0';
	return ret;
}