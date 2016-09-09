# Affine-Cipher
Just some stuff playing around with the Affine Cipher. Not the most elegant code, but, functional.

The affine_bruteforce.py script simply brute forces its way through encrypted Affine text. It's a pretty comment-heavy file, as I walk the reader through what I'm doing at each step and why. affine_bruteforce_clean.py is a cleaner version, and affine_bruteforce_nocomment.py is a commentless version. 

The script affine_encrypt.py allows you to encrypt a plaintext using the Affine algorithm. I'm sure you can figure out the purpose of affine_encrypt_clean.py and affine_encrypt_nocomment.py.

The folder example contains an encrypted text file called sample_input.txt to be used, yes, as a sample input. It also contains a text file called instructions.txt where I (poorly) explain how to use the scripts with the sample input.

It should be noted I coded all of this in Python 3.5.2 and tested it on Windows 10 Enterprise. I also did some light testing with Python 2.7.12. I feel as though it should work with older version of Python and other operating systems, but should it not, this may be the problem.

