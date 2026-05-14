from pwn import *


def extract(txt):

    idx = txt.index('level ') + 6
    idx2 = txt.index(' ', idx) + 1    
    level1 = txt[idx:idx2].strip()

    idx = txt.index('{')+1
    idx2 = txt.index('}')
    categories = txt[idx:idx2].split(',')
    categories = [c.strip() for c in categories]
    
    idx = idx2 + 2
    idx2 = txt.index(' ', idx)
    verb = txt[idx:idx2]

    idx = txt.index('level', idx2) + 6
    idx2 = txt.index(' ', idx+1)
    level2 = txt[idx:idx2].strip()

    idx = txt.index('{', idx)+1
    idx2 = txt.index('}', idx)
    categories2 = txt[idx:idx2].split(',')
    categories2 = [c.strip() for c in categories2]

    return level1, level2, categories, categories2, verb


def compute(levels, level1, level2, categories, categories2, verb):
    
    idx = levels.index(level1)
    idx2 = levels.index(level2)

    if verb == "read":

        if idx > idx2:
            #print(f"{level1} > {level2}")
            return "no"

        if categories2[0] == '':
            #print(f"cat empty : {categories2[0]}")
            return "yes"

        for c in categories2:
            if c not in categories:
                #print(f"lack of cat {c}")
                return "no"

    else:
        
        if idx < idx2:
            #print(f"{level1} > {level2}")
            return "no"
        
        if categories[0] == '':
            return "yes"

        for c in categories:
            if c not in categories2:
                #print(f"lack of cat {c}")
                return "no"
    
    return "yes"

   

p = process("/challenge/run")

p.readuntil(b'Levels').decode()
p.readline()
levels = p.readuntil(b'Categories').decode().split('\n')[:-1]
p.readline()
menu_categories = p.readuntil(b'\nQ 1').decode().split('\n')[:-1]

print(f"levels {levels}")
print(f"categories {menu_categories}")


for i in range(200):
    txt = p.readline().decode()
    print(txt)

    if "Incorrect" in txt:
        print('incorrect !')
        break

    if "Congratulations" in txt:
        print(p.read().decode())
        break
    
    level1, level2, categories, categories2, verb = extract(txt)
    #print(level1)
    check = compute(levels, level1, level2, categories, categories2, verb)

    print(check)
    p.writeline(check.encode())

    x = p.readline().decode()        
    print(x)

