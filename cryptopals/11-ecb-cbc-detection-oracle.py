import random
from Crypto.Cipher import AES

print("""
____________________________
An ECB/CBC detection oracle

Now that you have ECB and CBC working:

Write a function to generate a random AES key; that's just 16 random bytes.

Write a function that encrypts data under an unknown key --- that is, a function that generates a random key and encrypts under it.

The function should look like:

encryption_oracle(your-input)
=> [MEANINGLESS JIBBER JABBER]

Under the hood, have the function append 5-10 bytes (count chosen randomly) before the plaintext and 5-10 bytes after the plaintext.

Now, have the function choose to encrypt under ECB 1/2 the time, and under CBC the other half (just use random IVs each time for CBC). Use rand(2) to decide which to use.

Detect the block cipher mode the function is using each time. You should end up with a piece of code that, pointed at a block box that might be encrypting ECB or CBC, tells you which one is happening. 
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


def count_repetitions(ciphertext, block_len = 16):
    blocks = [ciphertext[idx:idx+block_len] for idx in range(0, len(ciphertext), block_len)]
    reps_count = max([blocks.count(block) for block in blocks])
    return reps_count


def encryption_oracle(plaintext):
    key = random.randbytes(16)
    iv = random.randbytes(16)

    before = random.randbytes(random.randint(5,10))
    after = random.randbytes(random.randint(5,10))

    plaintext = pad(before + plaintext + after)

    if random.randint(0,100) % 2 == 0:
        cipher = 'ECB'
        ciphertext = ecb_encrypt(key, plaintext)
    else:
        cipher = 'CBC'
        ciphertext = cbc_encrypt(iv, key, plaintext)

    return cipher, ciphertext


conveniently_long_user_input = 'A' * 50

for _ in range(5):
    cipher, ciphertext = encryption_oracle(conveniently_long_user_input.encode())
    reps_count = count_repetitions(ciphertext)
    guess = "ECB" if reps_count > 1 else "CBC" 

    print(f"guess={guess} - cipher={cipher}")

