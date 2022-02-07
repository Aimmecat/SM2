#include "headfile.h"

Register32 Register[12];
Register32 Register_W[68];
Register32 Register_Ws[64];

void RegisterInit(void) {
	Register[A] = INIT_A_REGISTER;
	Register[B] = INIT_B_REGISTER;
	Register[C] = INIT_C_REGISTER;
	Register[D] = INIT_D_REGISTER;
	Register[E] = INIT_E_REGISTER;
	Register[F] = INIT_F_REGISTER;
	Register[G] = INIT_G_REGISTER;
	Register[H] = INIT_H_REGISTER;
	Register[SS1] = INIT_SS1_REGISTER;
	Register[SS2] = INIT_SS2_REGISTER;
	Register[TT1] = INIT_TT1_REGISTER;
	Register[TT2] = INIT_TT2_REGISTER;
}

void CF(String* m, int idx) {
	for (int i = 0; i < 16; ++i) {
		Register_W[i] = m->register_value[idx + i];
	}
	for (int i = 16; i < 68; ++i) {
		Register32 tmp = Register_W[i - 16] ^ Register_W[i - 9] ^ rol(Register_W[i - 3], 15);
		tmp = P(tmp, 1);
		Register_W[i] = tmp ^ rol(Register_W[i - 13], 7) ^ Register_W[i - 6];
	}
	for (int i = 0; i < 64; ++i) {
		Register_Ws[i] = Register_W[i] ^ Register_W[i + 4];
	}
	for (int i = 0; i < 64; ++i) {
		Register64 tmp = (Register64)((rol(Register[A], 12)) + (Register64)(Register[E]) + (Register64)(rol(GetTj(i), i)));
		tmp &= CUT32BIT;
		Register[SS1] = rol(tmp, 7);
		Register[SS2] = Register[SS1] ^ (rol(Register[A], 12));
		tmp = FF(Register[A], Register[B], Register[C], i) + (Register64)(Register[D])
			+ (Register64)(Register[SS2]) + (Register64)(Register_Ws[i]);
		Register[TT1] = tmp & CUT32BIT;
		tmp = GG(Register[E], Register[F], Register[G], i) + (Register64)(Register[H])
			+ (Register64)(Register[SS1]) + (Register64)(Register_W[i]);
		Register[TT2] = tmp & CUT32BIT;
		Register[D] = Register[C];
		Register[C] = rol(Register[B], 9);
		Register[B] = Register[A];
		Register[A] = Register[TT1];
		Register[H] = Register[G];
		Register[G] = rol(Register[F], 19);
		Register[F] = Register[E];
		Register[E] = P(Register[TT2], 0);
	}
}

void CreateHv(String* m) {
	RegisterInit();
	int length = m->hex_length >> 7;
	Register32 last_A = TransformHex2Int("7380166F");
	Register32 last_B = TransformHex2Int("4914B2B9");
	Register32 last_C = TransformHex2Int("172442D7");
	Register32 last_D = TransformHex2Int("DA8A0600");
	Register32 last_E = TransformHex2Int("A96F30BC");
	Register32 last_F = TransformHex2Int("163138AA");
	Register32 last_G = TransformHex2Int("E38DEE4D");
	Register32 last_H = TransformHex2Int("B0FB0E4E");
	for (int i = 0; i < length; ++i) {
		int idx = i << 4;
		CF(m, idx);
		Register[A] ^= last_A;
		Register[B] ^= last_B;
		Register[C] ^= last_C;
		Register[D] ^= last_D;
		Register[E] ^= last_E;
		Register[F] ^= last_F;
		Register[G] ^= last_G;
		Register[H] ^= last_H;
		last_A = Register[A];
		last_B = Register[B];
		last_C = Register[C];
		last_D = Register[D];
		last_E = Register[E];
		last_F = Register[F];
		last_G = Register[G];
		last_H = Register[H];
	}
	m->hash = (char*)calloc(64, sizeof(char));
	for (int i = 0; i < 8; ++i) {
		char* tmp = TransformInt2HexByte(Register[i]);
		strcat(m->hash, tmp);
	}
}

Register32 GetTj(int j) {
	if (j >= 0 and j <= 15) {
		return (Register64)(0x79CC4519);
	}
	return (Register64)(0x7A879D8A);
}

Register32 FF(Register32 x, Register32 y, Register32 z, int j) {
	if (j >= 0 and j <= 15) {
		return (Register64)(x ^ y ^ z);
	}
	return (Register64)(((x & y) | (x & z) | (y & z)));
}

Register32 GG(Register32 x, Register32 y, Register32 z, int j) {
	if (j >= 0 and j <= 15) {
		return (Register64)(x ^ y ^ z);
	}
	Register64 reverse_x = ~x;
	return (Register64)((x & y) | (reverse_x & z));
}

Register32 P(Register32 x, int label) {
	if (label == 0) {
		return x ^ rol(x, 9) ^ rol(x, 17);
	}
	return x ^ rol(x, 15) ^ rol(x, 23);
}
