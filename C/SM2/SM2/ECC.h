#pragma once
#ifndef _ECC_H_
#define _ECC_H_

#define AXIS_LEN		256
#define SLIDE_WINDOW	4
#define PRE_CALC_LEN	(1 << SLIDE_WINDOW)

typedef enum {
	AdditiveIdentityElement = 0,
	BasicPoint,
	JacobiPoint
} PointType;

typedef struct Point {
	PointType type;
	char* x;
	char* y;
	char* z;
}Point;

extern Point* PreCalcPoint[PRE_CALC_LEN];

Point* CreateNewPoint(char* axis_x, char* axis_y, char* axis_z, PointType point_type);
Point* JacobiAddPoint(Point* P, Point* Q);
Point* JacobiDoublePoint(Point* P);
Point* JacobiSlideWindowPlus(char* k);
void JacobiSlideWindowPlusPreCalc(Point* P);

#endif // !_ECC_H_

