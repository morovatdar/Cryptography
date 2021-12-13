import numpy as np

def dec2bin(number,length):
    """ Convert a decimal 'number' to a numpy binary array with a minimum 'length' """
    nparray = np.array(list(bin(number)[2:]), dtype=int)
    
    # Padding the left side of the binary number if it is shorter than 'length'
    L = length - len(nparray)
    if L > 0: nparray = np.append(np.zeros(L), nparray)
    return nparray

def permutate(bits, table):
	""" Permutate the 'bits' by using the provided 'table' """
	return np.array(list(map(lambda x: bits[x], table)))
    
    
def FullDES(message, key, action):
    """ Encrypting/ decrypting a message by full 64-DES
        Args: message: A 64-bit numpy array to encrypt or decrypt.
              key: A 64-bit numpy array as the key.
              action: A string equals to 'encrypt' or 'decrypt'
        Returns: The encrypted or decrypted message as a numpy binary array.
    """
    # Initial permutation
    IP = [57, 49, 41, 33, 25, 17, 9,  1, 59, 51, 43, 35, 27, 19, 11, 3,
		  61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7,
		  56, 48, 40, 32, 24, 16, 8,  0, 58, 50, 42, 34, 26, 18, 10, 2,
		  60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6]
    
    # Expansion permutation
    EP = [31,  0,  1,  2,  3,  4, 3,  4,  5,  6,  7,  8,
          7,  8,  9, 10, 11, 12, 11, 12, 13, 14, 15, 16,
          15, 16, 17, 18, 19, 20, 19, 20, 21, 22, 23, 24,
          23, 24, 25, 26, 27, 28, 27, 28, 29, 30, 31,  0]
    
    # Key permutation 1
    KP1 = [56, 48, 40, 32, 24, 16,  8, 0, 57, 49, 41, 33, 25, 17,
          9,  1, 58, 50, 42, 34, 26, 18, 10,  2, 59, 51, 43, 35,
          62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21,
          13,  5, 60, 52, 44, 36, 28, 20, 12,  4, 27, 19, 11,  3]
    
    # Key bits shift
    KS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    
    # Key permutation 2
    KP2 = [13, 16, 10, 23,  0,  4,  2, 27, 14,  5, 20,  9,
		   22, 18, 11,  3, 25,  7, 15,  6, 26, 19, 12,  1,
		   40, 51, 30, 36, 46, 54, 29, 39, 50, 44, 32, 47,
		   43, 48, 38, 55, 33, 52, 45, 41, 49, 35, 28, 31]
    
    # S-boxes
    Sbox = [
		# S1
		[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
	     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
		 [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
		 [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
		# S2
		[[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
		 [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
		 [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
		 [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]], 
		# S3
		[[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
		 [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
		 [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
		 [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
		# S4
		[[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
		 [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
		 [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
		 [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
		# S5
		[[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
		 [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
		 [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
		 [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
		# S6
		[[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
		 [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
		 [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
		 [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
		# S7
		[[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
		 [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
		 [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
		 [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
		# S8
		[[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
		 [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
		 [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
		 [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]
    
    # S-box permutation
    SP = [15, 6, 19, 20, 28, 11, 27, 16, 0, 14, 22, 25, 4, 17, 30, 9, 
          1, 7, 23, 13, 31, 26, 2, 8, 18, 12, 29, 5, 21, 10, 3, 24]
    
    # Final permutation
    FP = [39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30,
		  37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28,
		  35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26,
		  33, 1, 41,  9, 49, 17, 57, 25, 32, 0, 40,  8, 48, 16, 56, 24]
    
    # Initial permutation of the message
    message = permutate(message, IP)
    L, R = message[:32], message[32:] # Dividing the message into two 32-bit left and right parts
    
    # Permutating the key which includes deleting the parity bits
    # The input is 64-bit and the output is 56-bit
    key = permutate(key, KP1)
    C, D = key[:28], key[28:] # Dividing the message into two 32-bit left and right parts

    for i in range(16):
        ER = permutate(R, EP) # Expander function
        
        # Making round-i key
        # Instead of using the previous round key, each key is made by the cumulative shift in the original permuted Key
        if action == 'encrypt': 
            # Making the key for encryption
            CiDi = np.append(np.roll(C, -sum(KS[:i+1])), np.roll(D, -sum(KS[:i+1])))
        elif action == 'decrypt':
            # Making the key for decryption
            CiDi = np.append(np.roll(C, -sum(KS[:16-i])), np.roll(D, -sum(KS[:16-i])))
        # Final permutation of the key. The input is 56-bit and the output is 48-bit
        keyi = permutate(CiDi, KP2) 
        
        ER = ER ^ keyi # XOR the extended R with the ith key
        
        # Calculating F(R_(i-1),K_i) through S-box calculation
        F = np.zeros(32, dtype=int)
        for j in range(8):
            row = int(str(ER[6*j])+str(ER[6*j+5]),2)
            column = int(str(ER[6*j+1])+str(ER[6*j+2])+str(ER[6*j+3])+str(ER[6*j+4]),2)
            F[4*j:4*j+4] = dec2bin(Sbox[j][row][column], 4)
        F = permutate(F, SP) # S-box permutation

        L, R = R, L ^ F # Assign the ith round left and right bits
        
    return permutate(np.append(R, L), FP) # Final permutation


if __name__ == "__main__":
    
    message = '0123456789ABCDEF'
    key = '133457799BBCDFF1'
    
    def hex2array(text):
        """ Convert a hexadecimal string to a binary numpy array """
        binarray = np.array(list(bin(int(text, 16))[2:]), dtype=int)
        # Padding zero to the start of the array
        for elem in text:
            if elem == '0': 
                binarray = np.append(np.zeros(4, int), binarray)
            else:
                elem_len = len(bin(int(elem, 16))[2:])
                binarray = np.append(np.zeros(4-elem_len, int), binarray)
                break
        return binarray
    
    def array2hex(binarray):
        """ Convert a binary numpy array to a hexadecimal string """
        text = ''.join([str(elem) for elem in binarray])
        text = hex(int(text, 2))[2:].upper()
        # Padding zero to the start of the string
        for i in range(len(text)):
            if np.sum(binarray[4*i:4*(i+1)]) == 0: 
                text = '0' + text
            else: break
        return text
    
    # Encrypt the message and decrypt it again and show the results
    cipher = FullDES(hex2array(message), hex2array(key), 'encrypt')
    print('\nThe encrypted message is:', array2hex(cipher))
    
    text = FullDES(cipher, hex2array(key), 'decrypt')
    print('\nThe decrypted cipher is:', array2hex(text))