#include "math.h"
#include "stdio.h"
#include "time.h"


long long int ExitEuclidean(long long int a, long long int p) {
	if (p == 0)
		return 0;
	long long int x_last = 0, x_now = 1;
	long long int r_last = p, r_now = a;
	while (r_now != 0) {
		long long int q = (int)(r_last / r_now);
		long long int r_temp = r_last;
		long long int x_temp = x_last;
		r_last = r_now;
		x_last = x_now;
		r_now = r_temp - q * r_now;
		x_now = x_temp - q * x_now;
	}
	if (x_last < 0)
		x_last = p + x_last;
	return x_last;
}

long long int BExitEuclidean(long long int a, long long int p) {
	long long int init_p = p;
	long long int cnt = 0;
	long long int a00 = 1, a01 = 0;
	int flag_a = 0, flag_p = 1;
	while (a != 1) {
		flag_a = a & 1;
		flag_p = p & 1;
		if (flag_a && flag_p) {
			long long int num = (p - a) >> 1;
			if (a < num) {
				p = num;
				a01 = a01 - a00;
				a00 = a00 << 1;
			}
			else {
				p = a;
				a = num;
				long long int temp = a01;
				a01 = a00 << 1;
				a00 = temp - a00;
			}
		}
		else if (flag_a) {
			long long int num = p >> 1;
			if (a < num) {
				p = num;
				a00 = a00 << 1;
			}
			else {
				p = a;
				a = num;
				long long int temp = a01;
				a01 = a00 << 1;
				a00 = temp;
			}
		}
		else {
			a = a >> 1;
			a01 = a01 << 1;
		}
		cnt++;
	}
	for (int i = 0; i < cnt; i++) {
		if ((a00 & 1) == 0) {
			a00 = a00 >> 1;
		}
		else {
			a00 = (a00 + init_p) >> 1;
		}
	}
	return a00;
}


int main() {
	double start = 0.0;
	double end = 0.0;

	long long int a = 7789;
	long long int p = 390625;

	start = clock();
	for (int i = 0; i < 1000000; i++) {
		ExitEuclidean(a, p);
	}
	end = clock();

	printf("%lf\n", (double)(end - start) / CLK_TCK);

	start = clock();
	for (int i = 0; i < 1000000; i++) {
		BExitEuclidean(a, p);
	}
	end = clock();

	printf("%lf\n", (double)(end - start) / CLK_TCK);

	printf("%lld\n", ExitEuclidean(a, p));
	printf("%lld", BExitEuclidean(a, p));
	return 0;
}