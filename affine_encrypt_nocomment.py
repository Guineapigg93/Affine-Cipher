#Aaron Guillen
#9 September 2016

from string import ascii_uppercase
from random import randint
import sys

def instDict():
    ret = {}
    c = 0
    for i in ascii_uppercase:
        ret[i] = c
        c += 1
    for i in range(0, 26):
        ret[i] = ascii_uppercase[i]
    return ret

def usage():
    sys.stdout.write("usage: python affine.py [plaintext text file] [a] [b]")
    sys.stdout.write("\n\ta and b are optional. If not provided, they will be generated randomly\n")
    sys.exit(0)

def checkInput():
    if len(sys.argv) == 1:
        sys.stdout.write("It seems you have not provided me with a plaintext file.\n\n")
        usage()

    elif len(sys.argv) == 4:
        sys.stdout.write("You've provided key (" + sys.argv[2] + ", " + sys.argv[3] +")\n")

    elif len(sys.argv) > 2:
        sys.stdout.write("You've provided me with improper input!\n\n")
        usage()

def openFile():
    try:
        fin = open(sys.argv[1])
    except IOError:
        print("It seems that " + sys.argv[1] + " does not exist.")
        sys.exit(0)
    return fin

def factor(x):
    ret = []
    for i in range(1, x):
        if ((x // i) - (x / i)) == 0:
            ret.append(i)
    return ret

def findLegalA(m):
    factors = factor(m)
    ret = []
    for i in range(2, m):
        append = True
        for j in factors[1:]:
            if i % j == 0:
                append = False
        if append:
            ret.append(i)
    return ret
   
def randA(modulus):
    t = 0
    while t not in findLegalA(modulus):
        t = randint(2, modulus)
    return t

def randB(modulus):
    return randint(0, modulus)

def encAffine(plainText, a, b, modulus):
    for x in plainText:
        if x in alph:
            x = alph[x]
            e = ((a * x) + b) % 26
            sys.stdout.write(str(alph[e]))
        else:
            sys.stdout.write(x)
    sys.stdout.write("\n\n")

checkInput()
fin = openFile()

ptext = ""

for i in fin:
    ptext += i
ptext = ptext.upper()

fin.close()

alph = instDict()

m = 26

if len(sys.argv) == 4:
    try:
        a = int(sys.argv[2])
    except ValueError:
        sys.stdout.write("You've provided me with improper input!\n")
        sys.stdout.write("Input: " + sys.argv[2] + "\n\n")
        usage()
    try:
        b = int(sys.argv[3])
    except ValueError:
        sys.stdout.write("You've provided me with improper input!\n")
        sys.stdout.write("Input: " + sys.argv[3] + "\n\n")
        usage()
    temp = b
    b = b % 26
    if temp != b:
        sys.stdout.write("Your input "+ str(temp) + " was modded by 26 and has become " + str(b) + ".\n")
        sys.stdout.write("This is for simplification purposes and will have no effect on the outcome of encryption.\n\n")
    if a not in findLegalA(m):
        sys.stdout.write("Provided a value is not in legal set of values:\n")
        sys.stdout.write(str(findLegalA(m)) + "\n\n")
        usage()
else:
    a = randA(m)
    b = randB(m)

encAffine(ptext, a, b, m)

print("Your text was encrypted with key (" + str(a) + ", " + str(b) + ")")
