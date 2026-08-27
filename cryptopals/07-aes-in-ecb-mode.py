from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
import base64


print("""
____________________________
AES in ECB mode

The Base64-encoded content in this file has been encrypted via AES-128 in ECB mode under the key
"YELLOW SUBMARINE".

(case-sensitive, without the quotes; exactly 16 characters; I like "YELLOW SUBMARINE" because it's exactly 16 bytes long, and now you do too).

Decrypt it. You know the key, after all.
____________________________
""")

key = b"YELLOW SUBMARINE"

with open("7-file", "r") as f:

    ciphertext = base64.b64decode(f.read())

    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)

    print(f"Decrypting {ciphertext[0:10]}...")
    print(f"With key {key}")
    print()
    print(plaintext.decode())
