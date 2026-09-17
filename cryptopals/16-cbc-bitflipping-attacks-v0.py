# https://exploitnotes.org/exploit/cryptography/algorithm/aes-cbc-bit-flipping-attack#encryption-process

import base64
import random
from Crypto.Cipher import AES

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


def split(data, size=6):
    block_len = 16
    blocks = [data[idx:idx+block_len] for idx in range(0, len(data), block_len)]
    blocks = [block.hex() for block in blocks]
    return blocks[0:size]

def split_plain(data, size=6):
    block_len = 16
    blocks = [data[idx:idx+block_len] for idx in range(0, len(data), block_len)]
    return blocks[0:size]

def edit_byte_array(arr, idx, val):
    return arr[0:idx] + int.to_bytes(val) + arr[idx+1:]



iv = b"\x00" * 16
key = random.randbytes(16)

plaintext = b"xxx=xxxx&admin=0&username=sometest"
ciphertext = cbc_encrypt(iv, key, plaintext)

print(split_plain(plaintext))
print(split(ciphertext))

# we can set value to 1 because IV is set to 0
payload = 1

iv = edit_byte_array(iv, len(iv)-1, payload)

plaintext = cbc_decrypt(iv, key, ciphertext)
print(split_plain(plaintext))