from Crypto.Cipher import AES

print("""
____________________________
Implement CBC mode

CBC mode is a block cipher mode that allows us to encrypt irregularly-sized messages, despite the fact that a block cipher natively only transforms individual blocks.

In CBC mode, each ciphertext block is added to the next plaintext block before the next call to the cipher core.

The first plaintext block, which has no associated previous ciphertext block, is added to a "fake 0th ciphertext block" called the initialization vector, or IV.

Implement CBC mode by hand by taking the ECB function you wrote earlier, making it encrypt instead of decrypt (verify this by decrypting whatever you encrypt to test), and using your XOR function from the previous exercise to combine them.

The file here is intelligible (somewhat) when CBC decrypted against "YELLOW SUBMARINE" with an IV of all ASCII 0 (\x00\x00\x00 &c) 
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

block_len = 16
plaintext = b"salut salut c'est un test"
key = b"YELLOW SUBMARINE"
iv = b"\x00" * block_len

print(f"Plaintext {plaintext} - {len(plaintext)}")
print(f"Key {key}")
print(f"IV {iv.hex()}")
print()

ciphertext = cbc_encrypt(iv, key, pad(plaintext))
print(f"ciphertext {ciphertext.hex()} - {len(ciphertext)}")
print()

plaintext = cbc_decrypt(iv, key, ciphertext)
print(f"Plaintext {plaintext} - {len(plaintext)}")
print()