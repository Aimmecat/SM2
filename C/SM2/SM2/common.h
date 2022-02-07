#pragma once
#ifndef _COMMON_H_
#define _COMMON_H_

#define and		&&
#define or		||

#define Int10(x)	(x - '0')
#define Int16(x)	(x - 'A' + 10)

typedef int						int32;
typedef long long int			int64;

typedef unsigned int			uint32;
typedef unsigned int			Register32;

typedef unsigned long long int  uint64;
typedef unsigned long long int	Register64;


#endif // !_COMMON_H_
