#pragma once
#ifndef _MONTGOMERY_H_
#define _MONTGOMERY_H_

#define R_BIT_LEN	(-256)

char* RapidMod(char* a, char* p);
char* BExitEuclidean(char* a, char* p);
char* RapidInverseMod(char* a, char* p);
char* MontgomeryReduction(char* x, char* n, char* r_mask, char* _n);
char* MontgomeryMod(char* a, char* n, char* r_mask, char* r1, char* _n);
char* MontgomeryMultiplyMod(char* a, char* b, char* n, char* r_mask, char* r2, char* _n);
char* MontgomeryExpMod(char* a, int b, char* n, char* r_mask, char* r2, char* _n);
char* MontgomeryDivisionMod(char* a, char* b, char* n, char* r_mask, char* r2, char* _n);


#endif // !_MONTGOMERY_H_
