import string
import base64

print("""
____________________________
Break repeating-key XOR
It is officially on, now.

This challenge isn't conceptually hard, but it involves actual error-prone coding. The other challenges in this set are there to bring you up to speed. This one is there to qualify you. If you can do this one, you're probably just fine up to Set 6.

There's a file here. It's been base64'd after being encrypted with repeating-key XOR.

Decrypt it.

Here's how:

Let KEYSIZE be the guessed length of the key; try values from 2 to (say) 40.
Write a function to compute the edit distance/Hamming distance between two strings. The Hamming distance is just the number of differing bits. The distance between:

    this is a test

and

    wokka wokka!!!

is 37. Make sure your code agrees before you proceed.

For each KEYSIZE, take the first KEYSIZE worth of bytes, and the second KEYSIZE worth of bytes, and find the edit distance between them. Normalize this result by dividing by KEYSIZE.
The KEYSIZE with the smallest normalized edit distance is probably the key. You could proceed perhaps with the smallest 2-3 KEYSIZE values. Or take 4 KEYSIZE blocks instead of 2 and average the distances.
Now that you probably know the KEYSIZE: break the ciphertext into blocks of KEYSIZE length.
Now transpose the blocks: make a block that is the first byte of every block, and a block that is the second byte of every block, and so on.
Solve each block as if it was single-character XOR. You already have code to do this.
For each block, the single-byte XOR key that produces the best looking histogram is the repeating-key XOR key byte for that block. Put them together and you have the key.

This code is going to turn out to be surprisingly useful later on. Breaking repeating-key XOR ("Vigenere") statistically is obviously an academic exercise, a "Crypto 101" thing. But more people "know how" to break it than can actually break it, and a similar technique breaks something much more important. 
____________________________
""")

def ascii_ratio(txt):
    #charset = string.ascii_letters + " "
    charset = string.ascii_lowercase + string.digits + " "
    return sum([c in charset for c in txt]) / len(txt)


def is_ascii(txt, min_ratio):
    return ascii_ration(txt) > min_ratio


def xor(txt, key):
    result = ""

    for i in range(len(txt)):
        result += chr(txt[i] ^ ord(key[i % len(key)]))

    return result


def bf_xor(txt):
    best_ratio = 0
    best_key = 0

    for key in range(1, 256):

        res = ''.join([chr(ord(c) ^ key) for c in txt])
        ratio = ascii_ratio(res)

        if ratio > best_ratio:
            best_ratio = ratio
            best_key = key

    return best_key, best_ratio


def transpose(txt, chunksize):
    probable_key = ""
    chunks = [""] * chunksize
    
    for i in range(chunksize):
    
        for j in range(i, len(txt), chunksize):
            chunks[i] += chr(txt[j])

    for chunk in chunks:
        key, ratio = bf_xor(chunk)
        probable_key += chr(key)

    return probable_key


def find_keysize(txt, min=2, max=40):

    smallest_dist = -1
    smallest_keysize = 0

    for size in range(min, max+1):
        dist = try_keysize(txt, size)

        if smallest_dist == -1 or smallest_dist > dist:
            smallest_dist = dist
            smallest_keysize = size

    return smallest_keysize


def try_keysize(txt, keysize):
    idx = 0
    total_dist = 0
    nb_chunks = 0

    while idx+(keysize*2) < len(txt):
        c1 = txt[idx:idx+keysize]
        c2 = txt[idx+keysize:idx+(keysize*2)]

        total_dist += hamming(c1, c2)
        nb_chunks += 1
        idx += keysize

    return total_dist / keysize / nb_chunks


def hamming(str1, str2):

    str1 = ''.join(format(x, '08b') for x in str1)
    str2 = ''.join(format(x, '08b') for x in str2)
    dist = 0

    for idx in range(len(str1)):
        if str1[idx] != str2[idx]:
            dist += 1

    return dist


with open("6-file", "r") as f:

    txt = base64.b64decode(f.read())

    keysize = find_keysize(txt)
    print(f"Prob keysize : {keysize}")

    key = transpose(txt, keysize)
    print(f"Prob key : {key}")
    print()

    print("Trying to decrypt :")
    plaintext = xor(txt, key)
    print(plaintext)


