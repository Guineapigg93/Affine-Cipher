from string import ascii_uppercase
from random import randint
import sys

#This program is used to encode an Affine Cipher
#I'll reuse a fair amount of code from the decryption program

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

#Gotta have a usage
def usage():
    sys.stdout.write("usage: python affine.py [plaintext text file]")
    sys.exit(0)

#First thing's first, gotta get our plaintext. Command line input
def checkInput():
    if len(sys.argv) == 1:
        sys.stdout.write("It seems you have not provided me with a plaintext file.\n\n")
        usage()

    if len(sys.argv) > 2:
        sys.stdout.write("You've provided me with too much input!\n\n")
        usage()

#Get our File I/O out of the way ...
def openFile():
    try:
        fin = open(sys.argv[1])
    except IOError:
        print("It seems that " + sys.argv[1] + " does not exist.")
        sys.exit(0)
    return fin

checkInput()
fin = openFile()

#Empty string for plain text ..
ptext = ""

#Get our file into one long string ..
for i in fin:
    ptext += i
#Make sure we have all uppercase letters ..
ptext = ptext.upper()

#DON'T YOU DARE FORGET TO CLOSE THAT FILE YOU ROTTEN SCOUNDREL
fin.close()

#Get our (uppercase) English aplhabet mapped to numbers 0 - 25
alph = instDict()

#Remember our cipher, CipherCharacter = (ax + b) % 26 where x is a plaintext character
#and a and b are our key values
#We are going to brute force all possible keys a and b
#Now, a SHOULD be chosen such that a and m are coprime
#Coprime, meaning that the only common positive factor of the two numbers is 1
#Bear in mind that with English, m is 26
#Since 26 = 2 * 13, a should not be a number divisible by 2 or 13.
#Thus, a is likely 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, or 25

#Our legal values for a
#a = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
#Or, rather, we find legal values for a dynamically

#Rough factoring ...
def factor(x):
    ret = [] #An empty set of factors
    for i in range(1, x):
        if ((x // i) - (x / i)) == 0:
            ret.append(i)
    return ret

#Perhaps not the most elegant implementation, but ..
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

#Randomly choose a and b
def randA(modulus):
    t = 0
    while t not in findLegalA(modulus):
        t = randint(2, modulus)
    return t

def randB(modulus):
    return randint(0, modulus)

#Our modulus, m, which, again, is 26
m = 26

#Get a and b
a = randA(m)
b = randB(m)

#Our encryption algorithm
def encAffine(plainText, a, b, modulus):
    for x in plainText:
        if x in alph:
            x = alph[x]
            e = ((a * x) + b) % 26
            sys.stdout.write(str(alph[e]))
        else:
            sys.stdout.write(x)
    sys.stdout.write("\n\n")

#RUN THAT ALGORITHM
encAffine(ptext, a, b, m)

print("Your text was encrypted with key (" + str(a) + ", " + str(b) + ")")
