# Basic Algorithms for Cryptography

I implemented the basic and fundamental algorithms required for cryptography.

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

  

## Basic Number Theory (cryptomath.py)
Most of the essential number theory tools needed for Cryptography are implemented:
- GCD: The great common divisor can be calculated easily by using the Euclidian algorithm. 
- Extended GCD: By the extended Euclidean algorithm, the GCD can be expressed as a sum of two numbers each multiplied by an integer. 
- Mod Inverse: A modular multiplicative inverse of an integer a is an integer x such that the product ax is congruent to 1 (mod m). 
- Primitive Root: It determines if an integer is a primitive root mod n.
- Matrix Inverse Mod: It calculates the inverse of matrix M mod n.
- is prime: It tests the primality of integer n. 
- Random Prime: It generates a random prime number between $2^{b+1}-1$ and $2^b-1$.
- Factor: Three methods are used for factorizing an integer n: Fermat's method, Pollard rho, and Pollard p-1.

  

## Data Encryption Standard
Data Encryption Standard (DES) is a symmetric key data encryption method. I implemented a simplified version of DES, Differential Cryptanalysis for the simplified DES, and finally the full 64-bit DES.

### Simplified DES (SimplifiedDES.py)
Like DES, the simplified DES algorithm is a block cipher. It works with 12-bit blocks of plaintexts and ciphertext, and the key size is 9-bit. There is no limitation on the number of rounds, but four rounds are typical to use.

### Differential Cryptanalysis (Cryptanalysis.py)
Differential cryptanalysis is a general form of cryptanalysis applicable primarily to block ciphers. In the broadest sense, it is the study of how differences in information input can affect the resultant difference at the output. I implemented 3-round and 4-round differential cryptanalysis to attack the simplified DES, which are simple forms of full cryptanalysis. 

### Full 64bit DES (FullDES.py)
DES is a 64-bit block cipher with 16 rounds of encryption and a 64-bit key. 

  

## RSA (RSA.py) 
RSA (Rivest–Shamir–Adleman) is an asymmetric and public key cryptographic algorithm. 


