# Basic Algorithms for Cryptography

Following files cover different parts of the project:

cryptomath.py : functions for GCD, ExtendedGCD, and ModInverse  
AffineCiphers.py : encode, decode, and attack with affine ciphers  
VigenereCipher.py : encode and decode with Vigenere cipher  
Frequency.py : letter frequency calculation of a text  

## Classical Cryptosystems (Classical.py)
This module is connected to the classical cipher modules like Affine and Vigenere. The user has the option to choose the cipher method and then select the action they want to do (Encode, Decode, Attack).

### Affine Ciphers (Affine.py)
The affine cipher is a monoalphabetic substitution cipher, where each letter in an alphabet is mapped to its numeric equivalent, encrypted using a simple mathematical function, and converted back to a letter.  
Other than encryption and decryption some affine cipher attacks are covered (Chosen plaintext, chosen-ciphertext, known plaintext, and Ciphertext only attacks).
 
### Vigenere Cipher (Vigenere.py)
In the Vigenere cipher, each plaintext letter is shifted along different shift numbers in sequence.  
Encryption, decryption, and frequency attack is implemented for this module.

### Frequency Calculation (Frequency.py)
The frequency tables of single letters (1frequency.txt) and letters pairs (2frequency.txt) in English text are considered for different attacks.

