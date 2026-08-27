

print("""
____________________________
Fixed XOR

Write a function that takes two equal-length buffers and produces their XOR combination.

If your function works properly, then when you feed it the string:
1c0111001f010100061a024b53535009181c

... after hex decoding, and when XOR'd against:
686974207468652062756c6c277320657965

... should produce:
746865206b696420646f6e277420706c6179
____________________________
""")

def xor(txt, key):
    result = bytearray()

    for i in range(len(txt)):
        x = txt[i] ^ key[i % len(key)]
        result.append(x)

    return bytes(result)


txt = bytes.fromhex("1c0111001f010100061a024b53535009181c")
key = bytes.fromhex("686974207468652062756c6c277320657965")
result = xor(txt, key)

print(f"Raw result : {result}")
print(f"Hex : {result.hex()}")
