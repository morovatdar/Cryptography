import numpy as np

def SimplifiedDES(message, key, round, action):
    """ Encrypting/ decrypting a message by simplified DES
        Args: message: A 12-bit numpy array to encrypt or decrypt.
              key: A 9-bit numpy array as the key.
              rounds: The number of rounds for the encryption or decryption.
              action: A string equals to 'encrypt' or 'decrypt'
        Returns: The encrypted or decrypted message as a numpy binary array.
    """ 
    # S-boxes
    S1 = [['101','010','001','110','011','100','111','000'],['001','100','110','010','000','111','101','011']]
    S2 = [['100','000','110','101','111','001','011','010'],['101','011','000','111','110','010','001','100']]
    
    # Dividing the message into two 6-bit parts (left and right)
    if action == 'encrypt':
        L, R = message[:6], message[6:] 
    elif action == 'decrypt':
        R, L = message[:6], message[6:]

    for i in range(round):
        ER = np.insert(np.insert(R,2,R[3]),5,R[2]) # Expander function

        # Making round-i key
        if action == 'encrypt': 
            keyi = np.roll(key, -i)[:8] # Making the key for encryption
        elif action == 'decrypt':
            keyi = np.roll(key, -round+i+1)[:8] # Making the key for decryption
            
        ER = ER ^ keyi # XOR the extended R with the ith key
        
        # Calculating F(R_(i-1),K_i) through S-box calculation
        column1 = int(str(ER[1])+str(ER[2])+str(ER[3]),2)
        column2 = int(str(ER[5])+str(ER[6])+str(ER[7]),2)
        F = np.array(list(S1[ER[0]][column1] + S2[ER[4]][column2]), dtype=int)

        L, R = R, L ^ F # Assign the ith round left and right bits
    
    if action == 'encrypt':    
        return np.append(L, R)
    elif action == 'decrypt':
        return np.append(R, L)


if __name__ == "__main__":
    
    round = 4
    key = '011001010'
    message = '011100100110'
    
    # Convert inputs to numpy arrays
    key = np.array(list(key), dtype=int)
    message = np.array(list(message), dtype=int)
    
    # Encrypt the message and decrypt it again and show the results
    cipher = SimplifiedDES(message, key, round, 'encrypt')
    print('\nThe encrypted array is:', cipher)
    text = SimplifiedDES(cipher, key, round, 'decrypt')
    print('\nThe decrypted array is:', text)
