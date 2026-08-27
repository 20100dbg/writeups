import string

print("""
____________________________
Single-byte XOR cipher

The hex encoded string:
1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736

... has been XOR'd against a single character. Find the key, decrypt the message.

You can do this by hand. But don't: write code to do it for you.

How? Devise some method for "scoring" a piece of English plaintext. Character frequency is a good metric. Evaluate each output and choose the one with the best score. 
____________________________
""")

def sounds_english(txt):
    #result = len([c for c in txt if chr(c) in string.ascii_letters]) / len(txt)
    result = len([c for c in txt if chr(c) in string.ascii_lowercase]) / len(txt)
    return result > 0.7


def xor(txt, key):
    result = bytearray()

    for i in range(len(txt)):
        x = txt[i] ^ key
        result.append(x)

    return bytes(result)


txt = bytes.fromhex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")

for i in range(256):
    result = xor(txt, i)
    is_english = sounds_english(result)

    if is_english:
        print(f"key {i} sounds english")
        print(f"{result}")
        print()
