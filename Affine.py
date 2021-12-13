from cryptomath import cryptomath
from Frequency import Frequency
import numpy as np

class Affine:

    def __init__(self):
        pass
    
    def AskKey():
        while True:
            (alpha, beta) = eval(input("\nPlease enter the cipher keys ('alpha', 'beta'): "))
            
            #Check if the cipher keys are integers
            if isinstance(alpha, int) and isinstance(alpha, int):
                #Check if alpha is not zero and coprime with 26
                if cryptomath.gcd(alpha,26) == 1 and alpha != 0:
                    return (alpha, beta)
                else:
                    print('ERROR: Alpha should be non-zero and coprime with 26!')
            else:
                print('ERROR: Alpha and beta should be integers!')


    def Encode(alpha, beta, text):
        #Convert the text string to a list
        textnum = list(text)
        
        #Do the calculations on each item of the list with map() function
        #First convert each letter to ASCII number and then to the scale of 0 to 26
        #Puting the result in the statement: alpha * X + beta (mod 26)
        #The getting back the ASCII scale and convert them to characters
        result = list(map(lambda x: chr((alpha * (ord(x)-97) + beta)%26 + 97), textnum))
        
        #Join all the list items (letters) to one string
        return ''.join(result)


    def Decode(alpha, beta, text):
        #Calculate the inversion of alpha and the new beta
        alpha = cryptomath.findModInverse(alpha,26)
        beta = - alpha * beta
        
        #Call the encoder function based on the calculated alpha and beta
        return Affine.Encode(alpha, beta, text)


    def Solve(plain,cipher):

        plaindiff = ord(plain[0])-ord(plain[1])
        cipherdiff = ord(cipher[0])-ord(cipher[1])
        n = 26
        if plaindiff == 0 or cipherdiff == 0:
            raise ValueError("Try two different characters in both plain and cipher texts")

        d = cryptomath.gcd(plaindiff,26)
        if d > 1:
            if (cipherdiff % d) != 0:
                raise ValueError("It is not solvable")
            else:
                plaindiff, cipherdiff, n = int(plaindiff/d), int(plaindiff/d), int(n/d)

        alpha = (cryptomath.findModInverse(plaindiff, n) * cipherdiff) % 26
        beta = ((ord(cipher[0]) -97) - alpha * (ord(plain[0]) - 97)) % 26
        return (alpha, beta)


    def CipherOnlyAttack(ciphertext):

        freqlist1 = Frequency.SingleFrequency(ciphertext)
        freqlist1 = np.flipud(freqlist1[np.argsort(freqlist1[:,0])])

        reference1 = Frequency.Reference()
        reference1 = np.flipud(reference1[np.argsort(reference1[:,0])])

        #freqlist2 = Frequency.PairFrequency(ciphertext)
        #reference2 = np.loadtxt('2frequency.txt')
        #reference2 = reference2 / np.sum(reference2)
        #assignlist = np.concatenate((freqlist1, reference1), axis=1)

        # epsilon = 0.02
        # for i in range(26):
        #     for j in range(26):
        #         if i!=j and abs(freqlist1[i,0] - freqlist1[j,0]) < epsilon:
        #              freqlist2[i,j]*reference2[i,j] + freqlist2[j,i]*reference2[j,i]

        flag = False
        for i in range(26):
            for j in range(i+1, 26):
                try:
                    plain = chr(int(reference1[i,3])+97)+chr(int(reference1[j,3])+97)
                    cipher = chr(int(freqlist1[i,1])+97)+chr(int(freqlist1[j,1])+97)
                    (alpha, beta) = Affine.Solve(plain,cipher)
                    flag = True
                    break
                except:
                    pass
            if flag == True: break
        if flag == False:
            print('ERROR: The provided cipher text is not solvable. Please try to add more letters')

        return alpha, beta


    def KnownPlainAttack(plaintext, ciphertext):
        plaintext = list(plaintext)
        ciphertext = list(ciphertext)
        plainlength = len(plaintext)
        cipherlength = len(ciphertext)

        if plainlength > 1 and cipherlength > 1 and plainlength == cipherlength:
            flag = False
            for i in range(plainlength):
                for j in range(i+1, plainlength):
                    try:
                        (alpha, beta) = Affine.Solve(plaintext[i]+plaintext[j],ciphertext[i]+ciphertext[j])
                        flag = True
                        break
                    except:
                        pass
                if flag == True: break
            if flag == False:
                print('ERROR: The provided plain text and cipher text are not solvable. Please try to add more letters')
        else:
            print('ERROR: The plain text and the cipher text should have equal and more than one letters')

        return alpha, beta
