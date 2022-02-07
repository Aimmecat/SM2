#include "headfile.h"


int main()
{
	char* data1 = "616263";
	char* data2 = "61626364616263646162636461626364616263646162636461626364616263646162636461626364616263646162636461626364616263646162636461626364";

	double start, end = 0;

	start = clock();
	String* test1;
	for (int i = 0; i < 1000; ++i) {
		test1 = NewString(data1);
		CreateHv(test1);
	}
	end = clock();
	printf("%lf\n", (end - start) / CLK_TCK * 1000);
	printf("%s\n", test1->hash);

	start = clock();
	String* test2;
	for (int i = 0; i < 1000; ++i) {
		test2 = NewString(data2);
		CreateHv(test2);
	}
	end = clock();
	printf("%lf\n", (end - start) / CLK_TCK * 1000);
	printf("%s", test2->hash);


	return 0;
}
