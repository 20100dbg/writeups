import string
import base64
import time

print("""
____________________________
Detect AES in ECB mode

In this file are a bunch of hex-encoded ciphertexts.

One of them has been encrypted with ECB.

Detect it.

Remember that the problem with ECB is that it is stateless and deterministic; the same 16 byte plaintext block will always produce the same 16 byte ciphertext. 
____________________________
""")

def count_repetitions(ciphertext, block_len = 16):
    blocks = [ciphertext[idx:idx+block_len] for idx in range(0, len(ciphertext), block_len)]
    reps_count = max([blocks.count(block) for block in blocks])
    return reps_count


with open("8-file", "r") as f:

    lines = f.readlines()
    max_rep = 0
    line_rep = ""
    idx_rep = 0
    idx = 0

    for line in lines:
        ciphertext = bytes.fromhex(line)
        nb_rep = count_repetitions(ciphertext)

        if nb_rep > max_rep:
            max_rep = nb_rep
            line_rep = line
            idx_rep = idx

        #print(f"{idx_rep} - {max_rep} - {line_rep[:20]}")
        idx += 1


    print(f"line {idx_rep}: {line_rep[:20]}... contains {max_rep} repeting block")
