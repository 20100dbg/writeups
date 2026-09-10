import base64
import random
from Crypto.Cipher import AES

print("""
____________________________
Byte-at-a-time ECB decryption (Harder)

Take your oracle function from #12. Now generate a random count of random bytes and prepend this string to every plaintext. You are now doing:

AES-128-ECB(random-prefix || attacker-controlled || target-bytes, random-key)

Same goal: decrypt the target-bytes.
Stop and think for a second.

What's harder than challenge #12 about doing this? How would you overcome that obstacle? The hint is: you're using all the tools you already have; no crazy math is required.

Think "STIMULUS" and "RESPONSE".

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

def encryption_oracle(key, prefix, plaintext):
    secret_text = base64.b64decode(b"Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")
    plaintext = pad(prefix + plaintext + secret_text)
    ciphertext = ecb_encrypt(key, plaintext)
    return ciphertext

def split(data, as_hex=False, block_len=16, size=None):
    blocks = [data[idx:idx+block_len] for idx in range(0, len(data), block_len)]
    if as_hex:
        blocks = [block.hex() for block in blocks]
    if size:
        blocks = blocks[0:size]
    return blocks

key = random.randbytes(16)
prefix = random.randbytes(random.randint(5,40))


ciphertext_len = len(encryption_oracle(key, prefix, b""))
#print(f"ciphertext_len: {ciphertext_len}")


# Find block len
block_len = 0
last_len = 0
idx_start_count = 0

for l in range(1,40):
    ciphertext = encryption_oracle(key, prefix, b"A" * l)
    current_len = len(ciphertext)

    if last_len > 0 and last_len != current_len:
        if idx_start_count > 0:
            block_len = l - idx_start_count
            break
        idx_start_count = l
    last_len = current_len

print(f"Block len: {block_len}")


# confirm ECB cipher
ciphertext = encryption_oracle(key, prefix, b"A" * 60)
reps_count = count_repetitions(ciphertext)
cipher_status = "Probable ECB" if reps_count > 1 else "unknown"

print(f"Cipher: {cipher_status}")


# find writable block
ciphertext_array = []

for l in range(0,block_len*2):

    ciphertext = encryption_oracle(key, prefix, b"A" * l)
    ciphertext = split(ciphertext, True, block_len, 4)
    ciphertext_array.append(ciphertext)


last_ciphertext = None
count_lines_without_change = []

for ciphertext in ciphertext_array:

    if last_ciphertext:
        for idx in range(len(ciphertext)):
            if ciphertext[idx] != last_ciphertext[idx]:
                count_lines_without_change[idx] += 1
    
    else:
        for idx in range(len(ciphertext)):
            count_lines_without_change.append(0)

    last_ciphertext = ciphertext


block_idx = 0
for idx in range(len(count_lines_without_change)):
    if count_lines_without_change[idx] >= block_len:
        block_idx = idx
        break

if block_idx > 0:
    prefix_len = count_lines_without_change[block_idx - 1]

# guess secret text
found = b""
ciphertext = encryption_oracle(key, prefix, b"")


for block_start in range(block_idx*block_len, len(ciphertext), block_len):

    for pad_len in range(block_len-1, -1, -1):

        ref_ciphertext = encryption_oracle(key, prefix, b"A" * (prefix_len+pad_len))

        for x in range(256):
            bx = int.to_bytes(x)
            ciphertext = encryption_oracle(key, prefix, b"A" * (prefix_len+pad_len) + found + bx)

            if ciphertext[block_start:block_start+block_len] == ref_ciphertext[block_start:block_start+block_len]:
                found += bx
                break
    

print(f"Found: {found}")