#include "headfile.h"

char* IDa = "31323334353637383132333435363738";
char* ENTLa = "0080";
char* m = "message digest";
char* xa = "09F9DF311E5421A150DD7D161E4BC5C672179FAD1833FC076BB08FF356F35020";
char* ya = "CCEA490CE26775A52DC6EA718CC1AA600AED05FBF35E084A6632F6072DA9AD13";
char* dA = "3945208F7B2144B13F36E38AC6D39F95889393692860B51A42FB81EF4DF7C5B8";

int main()
{
	mip = mirsys(1000, 16);
	Signature(IDa, ENTLa, m, xa, ya, dA);
	return 0;
}
 