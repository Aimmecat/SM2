#pragma once
#ifndef _SM3_H_
#define _SM3_H_

#define A					0
#define B					1
#define C					2
#define D					3
#define E					4
#define F					5
#define G					6
#define H					7
#define SS1					8
#define SS2					9
#define TT1					10
#define TT2					11

#define CUT32BIT			0xFFFFFFFF

#define INIT_A_REGISTER		0x7380166F
#define INIT_B_REGISTER		0x4914B2B9
#define INIT_C_REGISTER		0x172442D7
#define INIT_D_REGISTER		0xDA8A0600
#define INIT_E_REGISTER		0xA96F30BC
#define INIT_F_REGISTER		0x163138AA
#define INIT_G_REGISTER		0xE38DEE4D
#define INIT_H_REGISTER		0xB0FB0E4E
#define INIT_SS1_REGISTER	0x00000000
#define INIT_SS2_REGISTER	0x00000000
#define INIT_TT1_REGISTER	0x00000000
#define INIT_TT2_REGISTER	0x00000000

#define REGISTER_LENGTH		32

#define rol(value, bits) (((value) << (bits)) | ((value) >> (32 - bits)))

void RegisterInit(void);
void CF(String* m, int idx);
char* CreateHv(String* m);
Register32 GetTj(int j);
Register32 FF(Register32 x, Register32 y, Register32 z, int j);
Register32 GG(Register32 x, Register32 y, Register32 z, int j);
Register32 P(Register32 x, int label);

#endif // !_SM3_H_
