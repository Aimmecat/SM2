#pragma once
#ifndef _PARAMETER_H_
#define _PARAMETER_H_

extern char* sm2_p;
extern char* sm2_a;
extern char* sm2_b;
extern char* sm2_n;
extern char* sm2_xg;
extern char* sm2_yg;

extern char* SIGNATURE_RMASK;
extern char* SIGNATURE_R1;
extern char* SIGNATURE_R2;
extern char* SIGNATURE_N;

extern char* R_MASK;
extern char* R1;
extern char* R2;
extern char* _N;

char* CreateRandomK(void);

#endif // !_PARAMETER_H_
