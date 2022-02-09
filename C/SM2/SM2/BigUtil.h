#pragma once

#include "miracl.h"

#ifndef _BIGUTIL_H_
#define _BIGUTIL_H_

extern miracl* mip;

char* BigAdd(char* num1, char* num2);
char* BigSub(char* num1, char* num2);
char* BigMultilpy(char* num1, char* num2);
char* BigAnd(char* num1, char* num2);
char* BigXor(char* num1, char* num2);
char* BigShift(char* num, int shift);
BOOL BigCompare(char* num1, char* num2);
BOOL BigDivisible(char* num1, int n);
char* BigCopy(char* num);
int GetBinLength(char* num);
char* GetComplement(char* num);

#endif // !_BIGUTIL_H_

