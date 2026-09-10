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

def find_repeating_block(ciphertext, block_len = 16):
    blocks = [ciphertext[idx:idx+block_len] for idx in range(0, len(ciphertext), block_len)]

    last_block = None
    count_block = 0
    for block in blocks:
        if blocks.count(block) > count_block:
            count_block = blocks.count(block)
            last_block = block
    
    return last_block


def encryption_oracle(key, plaintext):
    secret_text = base64.b64decode(b"Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")
    #prefix = random.randbytes(random.randint(5,40))
    prefix = random.randbytes(random.randint(14,18))
    plaintext = pad(prefix + plaintext + secret_text)
    ciphertext = ecb_encrypt(key, plaintext)
    return plaintext, ciphertext

def split(data, size=6):
    as_hex = True
    block_len = 16

    blocks = [data[idx:idx+block_len] for idx in range(0, len(data), block_len)]
    if as_hex:
        blocks = [block.hex() for block in blocks]
    if size:
        blocks = blocks[0:size]
    return blocks

def split_plain(data, size=6):
    block_len = 16

    blocks = [data[idx:idx+block_len] for idx in range(0, len(data), block_len)]
    if size:
        blocks = blocks[0:size]
    return blocks


print("=" * 30)
print("Not working ! (yet)")
print("=" * 30)

key = random.randbytes(16)


plaintext, ciphertext = encryption_oracle(key, b"")
ciphertext_len = len(ciphertext)
#print(f"ciphertext_len: {ciphertext_len}")


# Find block len

for l in [8, 16, 32]:
    payload = b"B" * l * 3
    plaintext, ciphertext = encryption_oracle(key, b"A" * (l-1) + payload)
    reps_count = count_repetitions(ciphertext)
    if reps_count in [2,3]:
        block_len = l
        break

print(f"Block len: {block_len}")


"""
# find secret_text len
ciphertext = encryption_oracle(key, b"A" * block_len * 3)
repeating_block = find_repeating_block(ciphertext)
idx = ciphertext.rfind(repeating_block) + block_len

secret_text_cipher = ciphertext[idx:]
secret_text_cipher_len = len(secret_text_cipher)
secret_blocks_len = secret_text_cipher_len // block_len


print(f"secret_text_cipher_len {secret_text_cipher_len} (real+unpadded is 138)")
print(f"secret_blocks_len {secret_blocks_len}")
"""

pad_block = b"A" * block_len

plaintext, ciphertext = encryption_oracle(key, pad_block * 3)
repeating_block = find_repeating_block(ciphertext)
print(f"repeating_block {repeating_block.hex()}")

secret_text_cipher_len = 144

# guess secret text
found = b""


for cipher_block_idx in range(0, secret_text_cipher_len // block_len, block_len):

    print(f"cipher_block_idx {cipher_block_idx} / {secret_text_cipher_len // block_len}")

    for pad_len in range(block_len-1, -1, -1):

        found_pad_block = False

        while not found_pad_block:
            ref_plaintext, ref_ciphertext = encryption_oracle(key, pad_block + b"A" * pad_len)

            if repeating_block in ref_ciphertext:
                found_pad_block = True

        for x in range(256):
            bx = int.to_bytes(x)
            found_pad_block_2 = False

            while not found_pad_block_2:
                plaintext, ciphertext = encryption_oracle(key, pad_block + b"A" * pad_len + found + bx)

                if repeating_block in ciphertext:
                    found_pad_block_2 = True

            block_idx = ciphertext.rfind(repeating_block) + block_len

            """
            print(block_idx)
            print(split_plain(plaintext))
            print(split(ciphertext))

            print()
            print(split_plain(ref_plaintext))
            print(split(ref_ciphertext))
            exit()
            """

            if ciphertext[block_idx:block_idx+block_len] == ref_ciphertext[block_idx:block_idx+block_len]:
                found += bx
                break
    

print(f"Found: {found}")