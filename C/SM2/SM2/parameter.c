#include "headfile.h"


char* sm2_p = "FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF";
char* sm2_a = "FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC";
char* sm2_b = "28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93";
char* sm2_n = "FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123";
//char* sm2_p = "13";
//char* sm2_a = "1";
char* sm2_xg = "32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7";
char* sm2_yg = "BC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0";

char* SIGNATURE_RMASK = "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF";
char* SIGNATURE_R1 = "10000000000000000000000008DFC2094DE39FAD4AC440BF6C62ABEDD";
char* SIGNATURE_R2 = "1EB5E412A22B3D3B620FC84C3AFFE0D43464504ADE6FA2FA901192AF7C114F20";
char* SIGNATURE_N = "6F39132F82E4C7BC2B0068D3B08941D4DF1E8D34FC8319A5327F9E8872350975";

char* R_MASK = "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF";
char* R1 = "100000000000000000000000000000000FFFFFFFF0000000000000001";
char* R2 = "400000002000000010000000100000002FFFFFFFF0000000200000003";
char* _N = "FFFFFFFC00000001FFFFFFFE00000000FFFFFFFF000000010000000000000001";

char* CreateRandomK(void) {
	return "59276E27D506861A16680F3AD9C02DCCEF3CC1FA3CDBE4CE6D54B80DEAC1BC21";
}
