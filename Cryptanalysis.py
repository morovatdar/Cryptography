import numpy as np
from SimplifiedDES import SimplifiedDES

def expand(bits):
    """ Expand the 6-bit input to a 8-bit output """
    return np.insert(np.insert(bits,2,bits[3]),5,bits[2])

def sbox(bits,sbox):
    """ Calculating the requested 'sbox' for the input 'bits' """
    # S-boxes
    S1 = [['101','010','001','110','011','100','111','000'],['001','100','110','010','000','111','101','011']]
    S2 = [['100','000','110','101','111','001','011','010'],['101','011','000','111','110','010','001','100']]
    
    # Column of the s-box
    column = int(str(bits[1])+str(bits[2])+str(bits[3]),2)
    # Find the item in the specified row and column of the s-box
    if sbox == 'S1':
        F = np.array(list(S1[bits[0]][column]), dtype=int)
    elif sbox == 'S2':
        F = np.array(list(S2[bits[0]][column]), dtype=int)
    return F

def possible_keys(L1_prime, L4, R4, L4s, R4s):
    """ Finding all possible first 4 bits and all possible last 4 bits of the key
        Args: L1_prime: XOR of L1 (the left bits of the first plain text) and L1* (the left bits of the second plain text).
              L4, R4: The left 6 bits and right 6 bits of the first cipher text.
              L4s, R4s: The left 6 bits and right 6 bits of the second cipher text.
        Returns: A list containing 2 numpy arrays. The first array represents the possible first 4 bits of the key in its rows,
                 and the second array represents the possible last 4 bits of the key in its rows.
    """
    # Calculating E(L4') = E(L4) XOR E(L4*)
    EL4 = expand(L4)
    Sbox_input = EL4 ^ expand(L4s)
    # The input to S1 and S2
    S1_input, S2_input = Sbox_input[:4], Sbox_input[4:]
    
    # Calculating R4' XOR L1' which is (R4 XOR R4*) XOR (L1 XOR L1*)
    Sbox_output = (R4 ^ R4s) ^ (L1_prime)
    # The output XOR from S1 and S2
    S1_output, S2_output = Sbox_output[:3], Sbox_output[3:]
    
    
    first_bits, last_bits = [], [] # Initialize the possible first/ last 4 bits
    # Considering the 16 different cases that can make the input to S1 (S1_input) and S2 (S2_input)
    for index in np.ndindex(2, 2, 2, 2):
        S1_pair, S2_pair = index ^ S1_input, index ^ S2_input # Finding the other pair of index
        
        # Find those indices and their pairs that can make S1_output and S2_output
        if np.array_equal(S1_output, sbox(index,'S1') ^ sbox(S1_pair,'S1')): 
            first_bits.append(index)
        if np.array_equal(S2_output, sbox(index,'S2') ^ sbox(S2_pair,'S2')): 
            last_bits.append(index)
    
    # XOR of E(L4) with the key (the 4th key)
    if first_bits != []: first_bits = EL4[:4] ^ first_bits
    if last_bits != []: last_bits = EL4[4:] ^ last_bits
    
    return [first_bits, last_bits] 


def Cryptanalysis3(plain, cipher):
    """ The Differential Cryptanalysis for three rounds of simplified DES
        Args: plain: A numpy matrix of different plain text messages. Each row represent one 12-bit message.
              cipher: A numpy matrix of related cipher text. Each row represent one 12-bit encrypted message.
        Returns: The 9-bit key.
    """
    # Iterating between different pairs of plain texts and cipher texts
    for i in range(len(plain)-1):    
        # Making the inputs of the possible_keys function
        L1_prime = plain[i,:6] ^ plain[i+1,:6] # L1' = L1 XOR L1*
        L4, L4s = cipher[i,:6], cipher[i+1,:6] # The left 6 bits of the first and second cipher texts
        R4, R4s = cipher[i,6:], cipher[i+1,6:] # The right 6 bits of the first and second cipher texts
        p_keys = possible_keys(L1_prime, L4, R4, L4s, R4s) # Possible keys
        
        if i == 0:
            # Initialize the candidates for the first and the last 4 bits of the 4th key
            left_candidates, right_candidates = p_keys[0], p_keys[1] 
        else:
            # Compare the new possible first 4 bits of the key with the previous set of candidates and keep only the common items
            p0set = set([tuple(x) for x in p_keys[0]])
            lset = set([tuple(x) for x in left_candidates])
            left_candidates = np.array([x for x in p0set & lset])
            # Compare the new possible last 4 bits of the key with the previous set of candidates and keep only the common items
            p1set = set([tuple(x) for x in p_keys[1]])
            rset = set([tuple(x) for x in right_candidates])
            right_candidates = np.array([x for x in p1set & rset])
            
        # Break the for loop, if only one candidate for the first 4 bits and one candidate for the last 4 bits remain
        if left_candidates.ndim * right_candidates.ndim == 1: break
    
    key = np.append(left_candidates, right_candidates) # The exact 4th Key
    
    # There are two possible cases for the complete key
    key = np.roll(np.insert(key,0,0), 2) # Make a possible complete key with 0 bit
    if not(np.array_equal(SimplifiedDES(plain[0,:], np.roll(key, -1), 3, 'encrypt'), cipher[0,:])):
        key[2] = 1 # If the previous complete key cannot make the cipher text, then change the bit to 1
        
    return key


def Cryptanalysis4():
    """ The Differential Cryptanalysis for four rounds of simplified DES
        This function randomly generates many plain binary arrays and calls an encryption function to encrypt them.
        This function does not have any access to the key of DES.
        Args: There is no argument. 
        Returns: The 9-bit key.
    """
    #Since L0'R0'=011010001100 then with the probability of 3/8 L1'R1'=001100000000
    L1_prime = np.array([0,0,1,1,0,0])
    
    left_candidates, right_candidates = [], [] # Initialize the candidates for the first and the last 4 bits of the 4th key
    
    # Repeat 3 rounds cryptanalysis 200 times
    for i in range(200):
        # Random pair of inputs L0R0 and L0*R0* in a way that L0'R0'=011010001100
        L0R0 = np.random.randint(2, size=12) 
        L0sR0s = L0R0 ^ [0,1,1,0,1,0,0,0,1,1,0,0]
        
        L4R4, L4sR4s = encrypt(L0R0), encrypt(L0sR0s) # Calculate the cipher array L4R4 and L4*R4*
        # Call the possible_keys function to find all possible first and last 4 bits of the 4th key
        p_keys = possible_keys(L1_prime, L4R4[:6], L4R4[6:], L4sR4s[:6], L4sR4s[6:])
        
        # Stack the new candidates to the previous possible first 4 bits of the key
        if np.array_equal(left_candidates, []):
            left_candidates = p_keys[0]
        else:
            if not(np.array_equal(p_keys[0], [])): left_candidates = np.vstack((left_candidates, p_keys[0]))
        # Stack the new candidates to the previous possible last 4 bits of the key
        if np.array_equal(right_candidates, []): 
            right_candidates = p_keys[1] 
        else:
            if not(np.array_equal(p_keys[1], [])): right_candidates = np.vstack((right_candidates, p_keys[1]))
                        
    l_unq, l_cnt = np.unique(left_candidates, axis=0, return_counts=True) # Unique candidates for the first 4 bits and their counts
    r_unq, r_cnt = np.unique(right_candidates, axis=0, return_counts=True) # Unique candidates for the last 4 bits and their counts
    
    key = np.append(l_unq[np.argmax(l_cnt),:], r_unq[np.argmax(r_cnt),:]) # Find the most frequent key
    
    # There are two possible cases for the complete key
    key = np.roll(np.insert(key,0,0), 2) # Make a possible complete key with 0 bit
    if not(np.array_equal(SimplifiedDES(L0R0, key, 4, 'encrypt'), L4R4)):
        key[2] = 1 # If the previous complete key cannot make the cipher text, then change the bit to 1
    
    return key


if __name__ == "__main__":
    ###################### Three rounds cryptanalysis ######################
    # 3-round cryptanalysis inputs
    plaintext = ['000111011011','101110011011','010111011011']
    ciphertext = ['000011100101','100100011000','001011001010']
    
    # Converting the inputs to two 2-dimension numpy arrays C and M, each row represents a plaintext or ciphertext
    M = np.array(list(plaintext[0]), dtype=int)
    C = np.array(list(ciphertext[0]), dtype=int)
    for i in range(1,len(plaintext)):
        M = np.vstack([M, np.array(list(plaintext[i]), dtype=int)])
        C = np.vstack([C, np.array(list(ciphertext[i]), dtype=int)])
    
    # Find the key to the simplified DES by 3-round cryptanalysis and show the results
    key = Cryptanalysis3(M, C)
    print('\nThe key found from 3-round cryptanalysis is:', key)

    ###################### Four rounds cryptanalysis ######################        
    # Encrypting the message by the selected four_round_key
    def encrypt(message):
        # Choose a key for 4-round cryptanalysis
        four_round_key = '101110000'
        four_round_key = np.array(list(four_round_key), dtype=int) # Convert the key to a numpy array
        #four_round_key = key # Select the key from the 3-round cryptanalysis and try to find it again with 4-round cryptanalysis
        
        return SimplifiedDES(message, four_round_key, 4, 'encrypt')
    
    # Find the key to the simplified DES by 4-round cryptanalysis and show the results
    keys = Cryptanalysis4()
    print('\nThe key found from 4-round cryptanalysis is:', keys)
        