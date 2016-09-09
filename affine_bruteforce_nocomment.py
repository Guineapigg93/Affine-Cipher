#Aaron Guillen
#8 September 2016

from string import ascii_uppercase
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
    sys.stdout.write("usage: python affine.py [ciphertext text file]")
    sys.exit(0)

def checkInput():
    if len(sys.argv) == 1:
        sys.stdout.write("It seems you have not provided me with a ciphertext file.\n\n")
        usage()

    if len(sys.argv) > 2:
        sys.stdout.write("You've provided me with too much input!\n\n")
        usage()

def openFile():
    try:
        fin = open(sys.argv[1])
    except IOError:
        print("It seems that " + sys.argv[1] + " does not exist.")
        sys.exit(0)
    return fin

def compMMInverse(a, m):
    for i in range(1, m):
        if ((a * i) % m) == 1:
            return i

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

def decAffine(ciphText, aValues, modulus):
    c = 1
    for a in aValues:
        mmi = compMMInverse(a, modulus)
        for b in range(0, modulus):
            sys.stdout.write("Attempt #" + str(c) + "\n")
            sys.stdout.write("Key Pair: (" + str(a) + ", " + str(b) + ")\n")
            for x in ciphText:
                if x in alph:
                    x = alph[x]
                    d = mmi * (x - b) % m
                    sys.stdout.write(str(alph[d]))
                else:
                    try:
                        sys.stdout.write(x)
                    except UnicodeEncodeError:
                        sys.stdout.write("")
            sys.stdout.write("\n\n")
            c += 1

checkInput()
fin = openFile()

ctext = ""

for i in fin:
    ctext += i
ctext = ctext.upper()

fin.close()

alph = instDict()

m = 26

a = findLegalA(m)

decAffine(ctext, a, m)
