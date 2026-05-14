from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad


def chose_plaintext(p, plain):
    p.read()
    p.write("1\n".encode())
    p.write(plain.encode() + b"\n")

    ret = p.readline()
    ret = ret[14:].decode().strip()
    return ret

def encrypt_flag(p, idx, length):
    p.read()
    p.write("2\n".encode())

    p.write(f"{idx}\n".encode())
    p.write(f"{length}\n".encode())

    ret = p.readline()
    ret = ret[22:].decode().strip()
    return ret


p = process('/challenge/run')
"""
plaintext = "pwn.college"
print(f"{plaintext} - {len(plaintext)}")
"""

#Find block size

block_size = 0

for i in range(2,64):

    ret = chose_plaintext(p, "a" * i)
    tmp_size = len(bytes.fromhex(ret))

    if tmp_size != block_size:
        if block_size == 0:
            block_size = tmp_size
        else:
            block_size = tmp_size - block_size
            break

print(f"block size = {block_size}")


#Find offset
offset = 0

for i in range(block_size * 2):
    ret = chose_plaintext(p, "a" * i)
    ret = bytes.fromhex(ret)

    found = False

    for j in range(0, len(ret) - block_size, block_size):
        if ret[j:j+block_size] == ret[j+block_size:j+(block_size*2)]:
            found = True
            offset = j
            break

    if found:
        break
    
print(f"Offset : {offset}")


#bf one byte

#block_size
#offset

#payload = 


"""
ret = encrypt_flag(p, 0, 11)
print(ret)
"""
