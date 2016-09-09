#Aaron Guillen
#8 September 2016

from string import ascii_uppercase
import sys

#We can *simply* use the below function to instantiate our dictionary
def instDict(): #easy way to get our dict
    ret = {}
    c = 0
    for i in ascii_uppercase:
        ret[i] = c
        c += 1
    for i in range(0, 26):
        ret[i] = ascii_uppercase[i]
    return ret

#Usage
def usage():
    sys.stdout.write("usage: python affine.py [ciphertext text file]")
    sys.exit(0)

#Check proper input
def checkInput():
    if len(sys.argv) == 1:
        sys.stdout.write("It seems you have not provided me with a ciphertext file.\n\n")
        usage()

    if len(sys.argv) > 2:
        sys.stdout.write("You've provided me with too much input!\n\n")
        usage()

#File I/O
def openFile():
    try:
        fin = open(sys.argv[1])
    except IOError:
        print("It seems that " + sys.argv[1] + " does not exist.")
        sys.exit(0)
    return fin

#Modular Multiplicative Inverse Calculator
def compMMInverse(a, m):
    for i in range(1, m):
        if ((a * i) % m) == 1:
            return i

#Rough factoring 
def factor(x):
    ret = [] #An empty set of factors
    for i in range(1, x):
        if ((x // i) - (x / i)) == 0:
            ret.append(i)
    return ret

#Find legal values for A
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

#Our decryption algorithm
def decAffine(ciphText, aValues, modulus):
    c = 1
    for a in aValues: #We get our a
        mmi = compMMInverse(a, modulus) #We get our modular multiplicative inverse a mod m
        for b in range(0, modulus): #We get our b
            sys.stdout.write("Attempt #" + str(c) + "\n")
            sys.stdout.write("Key Pair: (" + str(a) + ", " + str(b) + ")\n")
            for x in ciphText: #We check the ciphertext for each combination of a and b
                #Remember:
                #D(x) = a^-1 (x - b) mod m
                #Or, here
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

#Empty string for cipher text
ctext = ""

#Get our file into one long string
for i in fin:
    ctext += i
#To uppercase
ctext = ctext.upper()

#File close
fin.close()

#Get our (uppercase) English aplhabet mapped to numbers 0 - 25
alph = instDict()

#Modulus is 26
m = 26

#Pass legal a values to a list
a = findLegalA(m)

#Run Brute Force
decAffine(ctext, a, m)
