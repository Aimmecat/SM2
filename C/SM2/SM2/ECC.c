#include "headfile.h"

Point* PreCalcPoint[PRE_CALC_LEN];

Point* CreateNewPoint(char* axis_x, char* axis_y, char* axis_z, PointType point_type) {
	Point* new_point = (Point*)malloc(sizeof(Point));
	new_point->x = BigCopy(axis_x);
	new_point->y = BigCopy(axis_y);
	new_point->z = BigCopy(axis_z);
	new_point->type = point_type;
	return new_point;
}

Point* JacobiAddPoint(Point* P, Point* Q) {
	if (P->type == JacobiPoint and Q->type == JacobiPoint) {
		char* lambda1 = MontgomeryMultiplyMod(P->x, MontgomeryExpMod(Q->z, 2, sm2_p, R_MASK, R2, _N), sm2_p, R_MASK, R2, _N);
		char* lambda2 = MontgomeryMultiplyMod(Q->x, MontgomeryExpMod(P->z, 2, sm2_p, R_MASK, R2, _N), sm2_p, R_MASK, R2, _N);
		char* lambda3 = BigSub(lambda1, lambda2);
		char* lambda4 = MontgomeryMultiplyMod(P->y, MontgomeryExpMod(Q->z, 3, sm2_p, R_MASK, R2, _N), sm2_p, R_MASK, R2, _N);
		char* lambda5 = MontgomeryMultiplyMod(Q->y, MontgomeryExpMod(P->z, 3, sm2_p, R_MASK, R2, _N), sm2_p, R_MASK, R2, _N);
		char* lambda6 = BigSub(lambda4, lambda5);
		char* lambda7 = BigAdd(lambda1, lambda2);
		char* lambda8 = BigAdd(lambda4, lambda5);
		char* tmp = MontgomeryMultiplyMod(lambda7, MontgomeryExpMod(lambda3, 2, sm2_p, R_MASK, R2, _N), sm2_p, R_MASK, R2, _N);
		char* new_x = BigSub(MontgomeryExpMod(lambda6, 2, sm2_p, R_MASK, R2, _N), tmp);
		char* lambda9 = BigSub(tmp, BigShift(new_x, 1));
		char* new_y = BigSub(MontgomeryMultiplyMod(lambda9, lambda6, sm2_p, R_MASK, R2, _N), MontgomeryMultiplyMod(lambda8, MontgomeryExpMod(lambda3, 3, sm2_p, R_MASK, R2, _N), sm2_p, R_MASK, R2, _N));
		if (BigDivisible(new_y, 2))
			new_y = BigAdd(new_y, sm2_p);
		new_y = BigShift(new_y, -1);
		char* new_z = MontgomeryMultiplyMod(MontgomeryMultiplyMod(P->z, Q->z, sm2_p, R_MASK, R2, _N), lambda3, sm2_p, R_MASK, R2, _N);
		new_x = MontgomeryMod(new_x, sm2_p, R_MASK, R1, _N);
		new_y = MontgomeryMod(new_y, sm2_p, R_MASK, R1, _N);
		return CreateNewPoint(new_x, new_y, new_z, JacobiPoint);
	}
	else{
		return Q;
	}
}

Point* JacobiDoublePoint(Point* P) {
	if (P->type == JacobiPoint) {
		char* lambda1 = BigAdd(BigMultilpy("3", MontgomeryExpMod(P->x, 2, sm2_p, R_MASK, R2, _N)), BigMultilpy(sm2_a, MontgomeryExpMod(P->z, 4, sm2_p, R_MASK, R2, _N)));
		char* lambda2 = MontgomeryMultiplyMod(BigMultilpy("4", P->x), MontgomeryExpMod(P->y, 2, sm2_p, R_MASK, R2, _N), sm2_p, R_MASK, R2, _N);
		char* lambda3 = BigMultilpy("8", MontgomeryExpMod(P->y, 4, sm2_p, R_MASK, R2, _N));
		char* new_x = BigSub(MontgomeryExpMod(lambda1, 2, sm2_p, R_MASK, R2, _N), BigMultilpy("2", lambda2));
		char* new_y = BigSub(MontgomeryMultiplyMod(lambda1, BigSub(lambda2, new_x), sm2_p, R_MASK, R2, _N), lambda3);
		char* new_z = BigMultilpy("2", MontgomeryMultiplyMod(P->y, P->z, sm2_p, R_MASK, R2, _N));
		new_x = MontgomeryMod(new_x, sm2_p, R_MASK, R1, _N);
		new_y = MontgomeryMod(new_y, sm2_p, R_MASK, R1, _N);
		new_z = MontgomeryMod(new_z, sm2_p, R_MASK, R1, _N);
		return CreateNewPoint(new_x, new_y, new_z, JacobiPoint);
	}
	else {
		return P;
	}
}

void JacobiSlideWindowPlusPreCalc(Point* P) {
	*PreCalcPoint = P;
	for (int i = 1; i < PRE_CALC_LEN; ++i) {
		*(PreCalcPoint + i) = JacobiAddPoint(P, *(PreCalcPoint + i - 1));
	}
}

Point* JacobiSlideWindowPlus(char* k) {
	int j = strlen(k) - 1;
	Point* Q = CreateNewPoint("0", "0", "0", AdditiveIdentityElement);
	while (j >= 0) {
		Q = JacobiDoublePoint(Q);
		Q = JacobiDoublePoint(Q);
		Q = JacobiDoublePoint(Q);
		Q = JacobiDoublePoint(Q);
		int t = k[j] <= '9' ? Int10(k[j]) : Int16(k[j]);
		if (t != 0)
			Q = JacobiAddPoint(Q, PreCalcPoint[t - 1]);
		j--;
	}
	return Q;
}

Point* JacobiPoint2BasicPoint(Point* P) {
	char* new_x = MontgomeryDivisionMod(P->x, MontgomeryExpMod(P->z, 2, sm2_p, R_MASK, R2, _N), sm2_p, R_MASK, R2, _N);
	char* new_y = MontgomeryDivisionMod(P->y, MontgomeryExpMod(P->z, 3, sm2_p, R_MASK, R2, _N), sm2_p, R_MASK, R2, _N);
	return CreateNewPoint(new_x, new_y, "1", BasicPoint);
}

// for test:
//Point* newpoint1 = CreateNewPoint("18", "76", "1", JacobiPoint);
//Point* newpoint2 = CreateNewPoint("1F", "C0", "1", JacobiPoint);
//
//Point* ret1 = JacobiPoint2BasicPoint(JacobiAddPoint(newpoint1, newpoint2));
//Point* ret2 = JacobiPoint2BasicPoint(JacobiDoublePoint(newpoint1));