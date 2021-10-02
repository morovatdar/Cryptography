from cryptomath import cryptomath

def AskKey():
    while True:
        (alpha, beta) = eval(input("Please enter the cipher keys ('alpha', 'beta'): "))
        
        #Check if the cipher keys are integers
        if isinstance(alpha, int) and isinstance(alpha, int):
            #Check if alpha and 26 are coprime
            if cryptomath.gcd(alpha,26) == 1:
                return (alpha, beta)
            else:
                print('Alpha and 26 should be coprime!')
        else:
            print('Alpha and beta should be integers!')


def AskText(entry):
    while True:
        if entry == '1':
            text = input("What is the plain text? ")
        elif entry == '2':
            text = input("What is the cipher text? ")
        elif entry == '3':
            text = input("What is the cipher text for 'ab'? ")
        elif entry == '4':
            text = input("What is the plain text for 'AB'? ")

        #Check if all characters of the text are letters
        if text.isalpha():
            return text.lower()
        else:
            print('The plain text should contain only letters!')


def AffineEncode(alpha, beta, text):
    #Convert the text string to a list
    textnum = list(text)
    
    #Do the calculations on each item of the list with map() function
    #First convert each letter to ASCII number and then to the scale of 0 to 26
    #Puting the result in the statement: alpha * X + beta (mod 26)
    #The getting back the ASCII scale and convert them to characters
    result = list(map(lambda x: chr((alpha * (ord(x)-97) + beta)%26 + 97), textnum))
    
    #Join all the list items (letters) to one string
    return ''.join(result)


def AffineDecode(alpha, beta, text):
    #Calculate the inversion of alpha and the new beta
    alpha = cryptomath.findModInverse(alpha,26)
    beta = - alpha * beta
    
    #Call the encoder function based on the calculated alpha and beta
    return AffineEncode(alpha, beta, text)


def solve(plain,cipher):
    
    alpha = cryptomath.findModInverse(ord(plain[0])-ord(plain[1]), 26) * (ord(cipher[0])-ord(cipher[1]))
    alpha = alpha % 26
    beta = (ord(cipher[0]) -97) - alpha * (ord(plain[0]) - 97)
    beta = beta % 26
    return (alpha, beta)


if __name__ == "__main__":
    
    print('****************************************************************')
    print('This program encodes, decodes or attacks based on Affine Ciphers')
    print('****************************************************************')

    #Find out what the user wants to do
    flag = False
    while flag == False:
        print('1: Encode')
        print('2: Decode')
        print('3: Attack')
        print('4: Quit')
        action = input("Please enter the action number from the above list: ")

        #Check if the input command includes 'encode' or 'decode' commands
        if action in ['1','2','3','4']:
            flag = True

    if action == '1':
        #Input the cipher keys
        (alpha, beta) = AskKey()

        #Input the text to be encrypted
        text = AskText('1')

        #Call the function of encoding or decoding based on user's entry
        resulttext = AffineEncode(alpha, beta, text)

        #And, show the result.
        print('The encoded text is: ' + resulttext.upper()) #Convert the cipher text to uppercase


    elif action == '2':
        #Input the cipher keys
        (alpha, beta) = AskKey()

        #Input the text to be decrypted
        text = AskText('2')

        #Call the function of encoding or decoding based on user's entry
        resulttext = AffineDecode(alpha, beta, text)

        #And, show the result.
        print('The decoded text is: ' + resulttext.upper()) #Convert the cipher text to uppercase

    elif action == '3':
        #Find out the user wants to encode or decode the text
        flag = False
        while flag == False:
            print('1: Ciphertext only')
            print('2: Known plaintext')
            print('3: Chosen plaintext')
            print('4: Chosen ciphertext')
            print('5: Quit')
            attack = input("Please enter the attack method number from the above list: ")

            #Check if the input command includes 'encode' or 'decode' commands
            if attack in ['1','2','3','4','5']:
                flag = True

        if attack == '1':
            print('later')

        elif attack == '2':
            flag = False
            while flag == False:
                plaintext = list(AskText('1'))
                ciphertext = list(AskText('2'))
                plainlength = len(plaintext)
                cipherlength = len(ciphertext)

                if plainlength > 1 and cipherlength > 1 and plainlength == cipherlength:
                    flag2 = False
                    for i in range(plainlength):
                        for j in range(i+1, plainlength):
                            try:
                                (alpha, beta) = solve(plaintext[i]+plaintext[j],ciphertext[i]+ciphertext[j])
                                flag = True
                                flag2 = True
                            except:
                                pass
                    if flag2 == False:
                        print('The provided plain text and cipher text are not solvable. Please try to add more letters')
                else:
                    print('The plain text and the cipher text should have equal and more than one letters')

            print('The cipher key is: alpha='+str(alpha),' beta='+str(beta))

        elif attack == '3':
            flag = False
            while flag == False:
                text = AskText('3')
                if len(text) == 2:
                    (alpha, beta) = solve('ab',text)
                    flag = True
                else:
                    print('The cipher text should contain only two letters')
            print('The cipher key is: alpha='+str(alpha),' beta='+str(beta))

        elif attack == '4':
            flag = False
            while flag == False:
                text = AskText('4')
                if len(text) == 2:
                    (alpha, beta) = solve(text,'ab')
                    flag = True
                else:
                    print('The cipher text should contain only two letters')
            print('The cipher key is: alpha='+str(alpha),' beta='+str(beta))

        else:
            quit()

    else:
        quit()