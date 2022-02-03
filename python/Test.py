import time
from Encryption import CreatSM2EncryptionTime
from Decryption import CreatSM2DecryptionTime
from Signature import CreatSM2SignatureTime
from Verify import CreateSM2VerifyTime
from Utils.TransformData import Beauty_Show_Hex

Loop = 10

print('--------------------------------------------------------------------------')
print("Encryption")
Encryption_Time_Start = time.time()
ret = ''
for i in range(Loop):
    ret = CreatSM2EncryptionTime()
Encryption_Time_End = time.time()
use_time = str((Encryption_Time_End - Encryption_Time_Start) * 1000 / Loop) + 'ms'
print("The result of Encryption is:\t" + Beauty_Show_Hex(ret))
print('Encryption:\t' + use_time)

encryption_message = ret

print('--------------------------------------------------------------------------')
print("Decryption")
Decryption_Time_Start = time.time()
for i in range(Loop):
    ret = CreatSM2DecryptionTime(encryption_message)
Decryption_Time_End = time.time()
use_time = str((Decryption_Time_End - Decryption_Time_Start) * 1000 / Loop) + 'ms'
print("The result of Decryption is:\t" + ret)
print('Decryption:\t' + use_time)

print('--------------------------------------------------------------------------')
print("Signature")
Signature_Time_Start = time.time()
R = ''
S = ''
for i in range(Loop):
    R, S = CreatSM2SignatureTime()
Signature_Time_End = time.time()
use_time = str((Signature_Time_End - Signature_Time_Start) * 1000 / Loop) + 'ms'
print("The result of Signature is:\tR:" + Beauty_Show_Hex(R))
print("The result of Signature is:\tS:" + Beauty_Show_Hex(S))
print('Signature:\t' + use_time)

print('--------------------------------------------------------------------------')
print("Verify")
Verify_Time_Start = time.time()
for i in range(Loop):
    ret = CreateSM2VerifyTime(R, S)
Verify_Time_End = time.time()
use_time = str((Verify_Time_End - Verify_Time_Start) * 1000 / Loop) + 'ms'
print("The result of Verify is:\t" + Beauty_Show_Hex(ret))
print('Verify:\t' + use_time)

