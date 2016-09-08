from string import ascii_uppercase
import sys

#Our English Alphabet, mapped to numbers (uppercase)
#alph = {'A' : 0, 'B' : 1, 'C' : 2, 'D' : 3, 'E' : 4, 'F' : 5, 'G' : 6, 'H' : 7, 'I' : 8, 'J' : 9, 'K' : 10, 'L' : 11, 'M' : 12, 'N' : 13, 'O' : 14, 'P' : 15, 'Q' : 16, 'R' : 17, 'S' : 18, 'T' : 19, 'U' : 20, 'V' : 21, 'W' : 22, 'X' : 23, 'Y' : 24, 'Z' : 25, ' ' : ' '}

#For testing purposes, we have the following code:
#TEST --------------------------------------------------
#NOTE: This code is stolen from Wikipedia
#Prints a transposition table for an aphine cipher

#def transpAffine(a, b):
#    for i in range(26):
#        print(chr(i + 65) + ": " + chr(((a * i + b) % 26 ) + 65))

#transpAffine(5, 8)
#Using the table for transpAffine(5, 8), HELLO WORLD is encoded:
#helwoenc = "RCLLA\nOAPLX ;;n~~<><><><()*&^%$#@!-=_+:\";'{}[]|?.,`"
#ENDTEST -----------------------------------------------

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

#So I know that was a lot of preamble; let's get going, then.

#Gotta have a usage
def usage():
    sys.stdout.write("usage: python affine.py [ciphertext text file]")
    sys.exit(0)

#First thing's first, gotta get our ciphertext. Command line input
if len(sys.argv) == 1:
    sys.stdout.write("It seems you have not provided me with a ciphertext file.\n\n")
    usage()

if len(sys.argv) > 2:
    sys.stdout.write("You've provided me with too much input!\n\n")
    usage()

#Get our File I/O out of the way ...
try:
    fin = open(sys.argv[1])
except IOError:
    print("It seems that " + sys.argv[1] + " does not exist.")
    sys.exit(0)

#Empty string for cipher text ..
ctext = ""

#Get our file into one long string ..
for i in fin:
    ctext += i
#Make sure we have all uppercase letters ..
ctext = ctext.upper()

print(ctext)

#DON'T YOU DARE FORGET TO CLOSE THAT FILE YOU ROTTEN SCOUNDREL
fin.close()

#Get our (uppercase) English aplhabet mapped to numbers 0 - 25
alph = instDict()

#We also need to get the same thing reverses (that is, for 'A': 0, we need 0: 'A')


#Remember our cipher, CipherCharacter = (ax + b) % 26 where x is a plaintext character
#and a and b are our key values
#We are going to brute force all possible keys a and b
#Now, a SHOULD be chosen such that a and m are coprime
#Coprime, meaning that the only common positive factor of the two numbers is 1
#Bear in mind that with English, m is 26
#Since 26 = 2 * 13, a should not be a number divisible by 2 or 13.
#Thus, a is likely 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, or 25
#We will check these values for a first.
#a can be 1, but in this case we are dealing with a simple ceasar cipher
#For b, we will be checking 0 through 25
#Bear in mind also our decryption function
#D(x) = a^-1 (x - b) % m
#Where again, with English, m = 26. a^-1, then, is the modular multiplicative inverse
#of a mod 26. Finding this number is trivial with small integers such as we are using here
#say we are searching for y, the multiplicative modular inverse of a mod m
#We then say that y = a^-1 % m
#Or, y = 1/a % m (That is, "y equals (1 divided by a) mod m")
#thus, ay = 1 % m
#We then check every value for 0 < y < m until we find a value that satisfies this equation

#The function below computes a multiplicative modular inverse
#Bear in mind that for the purposes of this program, m will always be 26.
#Also bear in mind that if you supply this function with two numbers that are NOT
#coprime, it will simply return the first value it finds such that ay % m = 1, if it exists
def compMMInverse(a, m):
    for i in range(1, m):
        if ((a * i) % m) == 1:
            return i
        
#Now that we can find our multiplicative modular inverse, let's define
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

#Let's run the above methods... passing in our modulus, m, which, again, is 26
#And we assign it to a list
m = 26
a = findLegalA(m)

#Now, we have a list of possible a values, a list of possible b values (0 - (m - 1)),
#m (of course), and a way to computer a^-1 % m. We are ready to brute force our ciphertext
#Since a = 1 (the caesar cipher) will not be in our list of legal values for a,
#We'll have to be sure to check for that later

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
                    sys.stdout.write(x)
            sys.stdout.write("\n\n")
            c += 1

#RUN THAT ALGORITHM
decAffine(ctext, a, m)
