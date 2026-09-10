import base64
import random
from Crypto.Cipher import AES

print("""
____________________________
PKCS#7 padding validation

Write a function that takes a plaintext, determines if it has valid PKCS#7 padding, and strips the padding off.

The string:

"ICE ICE BABY\x04\x04\x04\x04"

... has valid padding, and produces the result "ICE ICE BABY".

The string:

"ICE ICE BABY\x05\x05\x05\x05"

... does not have valid padding, nor does:

"ICE ICE BABY\x01\x02\x03\x04"

If you are writing in a language with exceptions, like Python or Ruby, make your function throw an exception on bad padding.

Crypto nerds know where we're going with this. Bear with us. 
____________________________
""")

def check_padding_validity(plaintext):

    if plaintext:    
        pad_char = plaintext[-1]
        if len(plaintext) % 16 == 0:
            if pad_char > 0 and pad_char <= 16:
                if plaintext[-pad_char:] == pad_char.to_bytes(1, 'big') * pad_char:
                    return True

    return False


print(f"Check passed: {check_padding_validity(b"ICE ICE BABY\x04\x04\x04\x04") == True}")
print(f"Check passed: {check_padding_validity(b"HELLO\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b") == True}")
print(f"Check passed: {check_padding_validity(b"123456789012345\x01") == True}")
print(f"Check passed: {check_padding_validity(b"1234567890123456\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10") == True}")
print(f"Check passed: {check_padding_validity(b"\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10") == True}")
print(f"Check passed: {check_padding_validity(b"1234567890\x06\x06\x06\x06\x06\x06") == True}")

print(f"Check passed: {check_padding_validity(b"") == False}")
print(f"Check passed: {check_padding_validity(b"HELLO\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b") == False}") #
print(f"Check passed: {check_padding_validity(b"123456789012345\x02") == False}")
print(f"Check passed: {check_padding_validity(b"1234567890123456\x01") == False}")
print(f"Check passed: {check_padding_validity(b"ABC\x04\x04\x04") == False}")
print(f"Check passed: {check_padding_validity(b"ABC\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00") == False}")
print(f"Check passed: {check_padding_validity(b"ABC\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11") == False}")
print(f"Check passed: {check_padding_validity(b"ICE ICE BABY\x05\x05\x05\x05") == False}")
print(f"Check passed: {check_padding_validity(b"ICE ICE BABY\x01\x02\x03\x04") == False}")
