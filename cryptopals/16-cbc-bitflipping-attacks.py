import base64
import random
from Crypto.Cipher import AES

print("""
____________________________
CBC bitflipping attacks

Generate a random AES key.

Combine your padding code and CBC code to write two functions.

The first function should take an arbitrary input string, prepend the string:

"comment1=cooking%20MCs;userdata="

.. and append the string:

";comment2=%20like%20a%20pound%20of%20bacon"

The function should quote out the ";" and "=" characters.

The function should then pad out the input to the 16-byte AES block length and encrypt it under the random AES key.

The second function should decrypt the string and look for the characters ";admin=true;" (or, equivalently, decrypt, split the string on ";", convert each resulting string into 2-tuples, and look for the "admin" tuple).

Return true or false based on whether the string exists.

If you've written the first function properly, it should not be possible to provide user input to it that will generate the string the second function is looking for. We'll have to break the crypto to do that.

Instead, modify the ciphertext (without knowledge of the AES key) to accomplish this.

You're relying on the fact that in CBC mode, a 1-bit error in a ciphertext block:

    Completely scrambles the block the error occurs in
    Produces the identical 1-bit error(/edit) in the next ciphertext block.

____________________________
""")

def xor(x, y):
    result = bytearray()
    for idx in range(min(len(x), len(y))):
        result.append(x[idx] ^ y[idx])
    return result


def pad(plaintext, block_len=16):
    pad_len = block_len - (len(plaintext) % block_len)
    pad_char = int.to_bytes(pad_len )
    return plaintext + pad_char * pad_len

def unpad(ciphertext, block_len=16):
    pad = ciphertext[-1]
    return ciphertext[:-pad]

def ecb_encrypt(key, plaintext):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(plaintext)

def ecb_decrypt(key, ciphertext):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(ciphertext)

def cbc_encrypt(iv, key, plaintext, block_len=16):

    plaintext = pad(plaintext)
    ciphertext = b""

    for idx in range(0, len(plaintext), block_len):
        
        if idx == 0:
            last_block = iv

        block = plaintext[idx:idx+block_len]
        block = xor(block, last_block)
        last_block = ecb_encrypt(key, block)
        ciphertext += last_block

    return ciphertext

def cbc_decrypt(iv, key, ciphertext, block_len=16):

    plaintext = b""

    for idx in range(0, len(ciphertext), block_len):
        
        if idx == 0:
            last_block = iv
        else:
            last_block = ciphertext[idx-block_len:idx]
        
        ciphertext_block = ciphertext[idx:idx+block_len]
        block = ecb_decrypt(key, ciphertext_block)

        block = xor(block, last_block)
        plaintext += block

    return unpad(plaintext)


def encryption_oracle(iv, key, plaintext):
    prefix = b"comment1=cooking%20MCs;userdata="
    suffix = b";comment2=%20like%20a%20pound%20of%20bacon"

    plaintext = plaintext.replace(";","").replace("=","")
    plaintext = prefix + plaintext.encode() + suffix

    ciphertext = cbc_encrypt(iv, key, plaintext)
    return plaintext, ciphertext

def decryption_oracle(iv, key, ciphertext):
    plaintext = cbc_decrypt(iv, key, ciphertext)
    return plaintext

def split(data, size=6):
    block_len = 16
    blocks = [data[idx:idx+block_len] for idx in range(0, len(data), block_len)]
    blocks = [block.hex() for block in blocks]
    return blocks[0:size]

def split_plain(data, size=6):
    block_len = 16
    blocks = [data[idx:idx+block_len] for idx in range(0, len(data), block_len)]
    return blocks[0:size]

def check_if_admin(plaintext):
    args = plaintext.split(b";")

    for a in args:
        if a == b"admin=true":
            return True
    return False

def edit_byte_array(arr, idx, val):
    return arr[0:idx] + int.to_bytes(val) + arr[idx+1:]

iv = random.randbytes(16)
key = random.randbytes(16)


block_len = 16
plaintext = "AAAAAAAAAAAAAAAA:admin<true"

plaintext, ciphertext = encryption_oracle(iv, key, plaintext)
print(split_plain(plaintext))

print(split(ciphertext))

#modified = ciphertext byte ^ plaintext byte ^ target (plaintext) byte 

new_byte = ciphertext[32] ^ ord(":") ^ ord(";") 
ciphertext = edit_byte_array(ciphertext, 32, new_byte)

new_byte = ciphertext[38] ^ ord("<") ^ ord("=")
ciphertext = edit_byte_array(ciphertext, 38, new_byte)


print(split(ciphertext))

plaintext = decryption_oracle(iv, key, ciphertext)
print(split_plain(plaintext))

print()
print(f"is admin: {check_if_admin(plaintext)}")


