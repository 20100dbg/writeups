import base64
import random
import string
from Crypto.Cipher import AES

print("""
____________________________
ECB cut-and-paste

Write a k=v parsing routine, as if for a structured cookie. The routine should take:

foo=bar&baz=qux&zap=zazzle

... and produce:

{
  foo: 'bar',
  baz: 'qux',
  zap: 'zazzle'
}

(you know, the object; I don't care if you convert it to JSON).

Now write a function that encodes a user profile in that format, given an email address. You should have something like:

profile_for("foo@bar.com")

... and it should produce:

{
  email: 'foo@bar.com',
  uid: 10,
  role: 'user'
}

... encoded as:

email=foo@bar.com&uid=10&role=user

Your "profile_for" function should not allow encoding metacharacters (& and =). Eat them, quote them, whatever you want to do, but don't let people set their email address to "foo@bar.com&role=admin".

Now, two more easy functions. Generate a random AES key, then:

    Encrypt the encoded user profile under the key; "provide" that to the "attacker".
    Decrypt the encoded user profile and parse it.

Using only the user input to profile_for() (as an oracle to generate "valid" ciphertexts) and the ciphertexts themselves, make a role=admin profile. 
____________________________
""")

def xor(x, y):
    result = bytearray()
    for idx in range(min(len(x), len(y))):
        result.append(x[idx] ^ y[idx])
    return result

def pad(plaintext, block_len=16):
    pad_len = block_len - (len(plaintext) % block_len)
    pad_char = int.to_bytes(pad_len)
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

def encryption_oracle(key, plaintext):
    plaintext = pad(plaintext)
    ciphertext = ecb_encrypt(key, plaintext)
    return ciphertext

def params_to_dict(params):
    final_dict = {}
    arr = params.split("&")

    for elmt in arr:
        key,value = elmt.split("=")
        final_dict[key] = value

    return final_dict

def profile_for(email):
    uid = 45
    role = "user"
    #email = email.replace("&","").replace("=","")
    return f"email={email}&uid={uid}&role={role}"

def split(data, as_hex=False, size=16):

    blocks = [data[idx:idx+size] for idx in range(0, len(data), size)]

    if as_hex:
        blocks = [block.hex() for block in blocks]

    return blocks

"""
obj_parse = params_to_dict("foo=bar&baz=qux&zap=zazzle")
print(f"obj_parse {obj_parse}")
"""

profile = profile_for("foo@bar.com")
#print(f"profile    : {profile}")

block_len = 16
key = random.randbytes(16)

#find pad_first_block

last_ciphertext = None
for l in range(1,40):

    payload = "A" * l
    profile = profile_for(payload).encode()
    ciphertext = encryption_oracle(key, profile)

    if last_ciphertext and ciphertext[0:block_len] == last_ciphertext[0:block_len]:
        pad_first_block_len = l - 1
        break

    last_ciphertext = ciphertext

print(f"Found pad_first_block_len {pad_first_block_len}")

pad_first_block = "A" * pad_first_block_len


payload = "foo@bar.com"
profile = profile_for(payload).encode()
real_ciphertext = encryption_oracle(key, profile)


# craft a custom encrypted block

plaintext = b"admin" + b"\x0b" * 11
payload = pad_first_block + plaintext.decode()
profile = profile_for(payload).encode()
ciphertext = encryption_oracle(key, profile)

block_admin = ciphertext[16:32]



plaintext = b"admin@lol.com"
payload = plaintext.decode()
profile = profile_for(payload).encode()
ciphertext = encryption_oracle(key, profile)

ciphertext = ciphertext[0:32] + block_admin



print()

print(f"ciphertext: {ciphertext.hex()}")

plaintext = unpad(ecb_decrypt(key, ciphertext)).decode()
print(f"plaintext: {plaintext}")

print(f"params_to_dict {params_to_dict(plaintext)}")