# SM2
The implementation of SM2



1.27 进度汇报

加密：169.64ms

解密：87.27ms

签名：92.06ms

验证：154.29ms



1.28 换成SM2参数

加密：46.48ms

解密：29.03ms

签名：33.11ms

验证：42.89ms

2.2
完成二进制矩阵扩展欧几里得算法

2.3 转换为雅克比加重坐标计算 

加密：19.17ms

解密：15.26ms

签名：6.433ms

验证：10.04ms

由于SM3算法写的渣,起码占用了一半的时间,未来两天优化代码为主,全破突破100次每秒后基本可以转换成C语言, 保守估计速度快10倍

2.10
C语言代码写通了,SM3保守估计快了100倍,但是SM2甚至比python慢了100倍,且在内存管理方面写的非常渣,甚至不支持加解密签名验证同时跑,落泪,用miracl库做了大数的接口,但是频繁地访问接口,创建堆空间等使得整体效率过于低下,非常心累,白天再修复修复吧

加密：8.77s

解密：16.972s

签名：16.875s

验证：8.403s
