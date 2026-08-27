import string

print("""
____________________________
Detect single-character XOR

One of the 60-character strings in this file has been encrypted by single-character XOR.

Find it.

(Your code from #3 should help.) 
____________________________
""")

def sounds_english(txt, limit=0.7):
    result = len([c for c in txt if chr(c) in string.ascii_lowercase]) / len(txt)
    return result > limit


def xor(txt, key):
    result = bytearray()

    for i in range(len(txt)):
        x = txt[i] ^ key
        result.append(x)

    return bytes(result)


with open("4-file", "r") as f:

    lines = f.readlines()

    for line in lines:
        txt = bytes.fromhex(line)
        #print(f"{line} - {txt}")

        for i in range(256):
            result = xor(txt, i)
            is_english = sounds_english(result,limit=0.75)

            if is_english:
                print(f"cipher={line.strip()} - key={i} - plain={result}")
