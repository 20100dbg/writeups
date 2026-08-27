
print("""
____________________________
Implement PKCS#7 padding

A block cipher transforms a fixed-sized block (usually 8 or 16 bytes) of plaintext into ciphertext. But we almost never want to transform a single block; we encrypt irregularly-sized messages.

One way we account for irregularly-sized messages is by padding, creating a plaintext that is an even multiple of the blocksize. The most popular padding scheme is called PKCS#7.

So: pad any block to a specific block length, by appending the number of bytes of padding to the end of the block. For instance,
"YELLOW SUBMARINE"

... padded to 20 bytes would be:
"YELLOW SUBMARINE\x04\x04\x04\x04"
____________________________
""")

def pad(plaintext, block_len=16):
    pad_len = block_len - (len(plaintext) % block_len)
    pad_char = int.to_bytes(pad_len )
    return plaintext + pad_char * pad_len


def unpad(ciphertext, block_len=16):
    pad = ciphertext[-1]
    return ciphertext[:-pad]


block_len = 16
plaintext = b"YELLOW SUBMARINE"

print(f"Plaintext {plaintext} - {len(plaintext)}")

plaintext = pad(plaintext, block_len)
print(f"Padded {plaintext} - {len(plaintext)}")

ciphertext = unpad(plaintext, block_len)
print(f"Unpadded {ciphertext} - {len(ciphertext)}")
