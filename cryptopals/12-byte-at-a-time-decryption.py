import base64
import random
from Crypto.Cipher import AES

print("""
____________________________
Byte-at-a-time ECB decryption (Simple)

Copy your oracle function to a new function that encrypts buffers under ECB mode using a consistent but unknown key (for instance, assign a single random key, once, to a global variable).

Now take that same function and have it append to the plaintext, BEFORE ENCRYPTING, the following string:

Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK

Spoiler alert.

Do not decode this string now. Don't do it.

Base64 decode the string before appending it. Do not base64 decode the string by hand; make your code do it. The point is that you don't know its contents.

What you have now is a function that produces:

AES-128-ECB(your-string || unknown-string, random-key)

It turns out: you can decrypt "unknown-string" with repeated calls to the oracle function!

Here's roughly how:

    Feed identical bytes of your-string to the function 1 at a time --- start with 1 byte ("A"), then "AA", then "AAA" and so on. Discover the block size of the cipher. You know it, but do this step anyway.
    Detect that the function is using ECB. You already know, but do this step anyways.
    Knowing the block size, craft an input block that is exactly 1 byte short (for instance, if the block size is 8 bytes, make "AAAAAAA"). Think about what the oracle function is going to put in that last byte position.
    Make a dictionary of every possible last byte by feeding different strings to the oracle; for instance, "AAAAAAAA", "AAAAAAAB", "AAAAAAAC", remembering the first block of each invocation.
    Match the output of the one-byte-short input to one of the entries in your dictionary. You've now discovered the first byte of unknown-string.
    Repeat for the next byte.
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

def ecb_encrypt(key, plaintext):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(plaintext)

def count_repetitions(ciphertext, block_len = 16):
    blocks = [ciphertext[idx:idx+block_len] for idx in range(0, len(ciphertext), block_len)]
    reps_count = max([blocks.count(block) for block in blocks])
    return reps_count

def encryption_oracle(key, plaintext):
    secret_text = base64.b64decode(b"Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")
    plaintext = pad(plaintext + secret_text)
    ciphertext = ecb_encrypt(key, plaintext)
    return ciphertext


key = random.randbytes(16)

ciphertext_len = len(encryption_oracle(key, b""))
print(f"ciphertext_len: {ciphertext_len}")


# Find block len
block_len = 0
last_len = 0
idx_start_count = 0

for l in range(1,40):
    current_len = len(encryption_oracle(key, b"A" * l))

    if last_len > 0 and last_len != current_len:
        if idx_start_count > 0:
            block_len = l - idx_start_count
            break
        idx_start_count = l
    last_len = current_len

print(f"Block len: {block_len}")


# confirm ECB cipher
ciphertext = encryption_oracle(key, b"A" * 60)
reps_count = count_repetitions(ciphertext)
cipher_status = "Probable ECB" if reps_count > 1 else "unknown"

print(f"Cipher: {cipher_status}")


# guess secret text
found = b""

for block_start in range(0, len(ciphertext), block_len):

    for pad_len in range(block_len-1, -1, -1):

        ref_ciphertext = encryption_oracle(key, b"A" * pad_len)
        
        for x in range(256):
            bx = int.to_bytes(x)
            ciphertext = encryption_oracle(key, b"A" * pad_len + found + bx)

            if ciphertext[block_start:block_start+block_len] == ref_ciphertext[block_start:block_start+block_len]:
                found += bx
                break
    

print(f"Found: {found}")