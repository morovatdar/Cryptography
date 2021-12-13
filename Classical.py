from Affine import Affine
from Vigenere import Vigenere

def AskText(entry):
    while True:
        if entry == '1':
            text = input("\nWhat is the plain text? ")
        elif entry == '2':
            text = input("\nWhat is the cipher text? ")
        elif entry == '3':
            text = input("\nWhat is the cipher text for 'ab'? ")
        elif entry == '4':
            text = input("\nWhat is the plain text for 'AB'? ")

        #Check if all characters of the text are letters
        if text.isalpha():
            return text.lower()
        else:
            print('ERROR: The text should contain only letters!')


if __name__ == "__main__":
    
    print("""
    ************************************************************************
    This program encodes, decodes or attacks based on your choice of ciphers
    ************************************************************************""")

    #Find out the cipher
    flag = False
    while flag == False:
        print('\n1: Affine \n2: Vigenere \n9: Quit')
        cipherno = input("Please enter the cipher number from the above list: ")

        #Check if the input command includes 'encode' or 'decode' commands
        if cipherno in ['1','2','9']: flag = True
        if cipherno == '9': exit()

    #Find out what the user wants to do
    flag = False
    while flag == False:
        print('\n1: Encode \n2: Decode \n3: Attack \n9: Quit')
        action = input("Please enter the action number from the above list: ")

        #Check if the input command includes 'encode' or 'decode' commands
        if action in ['1','2','3','9']: flag = True
        if action == '9': exit()
        
    if action == '1':
        #Input the text to be encrypted
        text = AskText('1')

        if cipherno == '1':
            (alpha, beta) = Affine.AskKey()
            resulttext = Affine.Encode(alpha, beta, text)

        elif cipherno == '2':
            key = Vigenere.AskKey()
            resulttext = Vigenere.Encode(key, text)

        print('\nThe encoded text is:', resulttext.upper()) 


    elif action == '2':
        #Input the text to be decrypted
        text = AskText('2')

        if cipherno == '1':
            (alpha, beta) = Affine.AskKey()
            resulttext = Affine.Decode(alpha, beta, text)

        elif cipherno == '2':
            key = Vigenere.AskKey()
            resulttext = Vigenere.Decode(key, text)

        print('\nThe decoded text is:', resulttext.lower()) 


    elif action == '3':

        if cipherno == '1':    
            #Find out the type of attack
            flag = False
            while flag == False:
                print('\n1: Ciphertext only \n2: Known plaintext \n3: Chosen plaintext \n4: Chosen ciphertext \n9: Quit')
                attack = input("Please enter the attack method number from the above list: ")

                #Check if the input command includes 'encode' or 'decode' commands
                if attack in ['1','2','3','4','9']: flag = True
                if attack == 9: exit()

            if attack == '1': 
                text = AskText('2')
                (alpha, beta) = Affine.CipherOnlyAttack(text)
            elif attack == '2':
                plaintext = AskText('1')
                ciphertext = AskText('2')
                (alpha, beta) = Affine.KnownPlainAttack(plaintext, ciphertext)
            elif attack == '3':
                text = AskText('3')
                (alpha, beta) = Affine.Solve('ab',text[:2])
            elif attack == '4':
                text = AskText('4')
                (alpha, beta) = Affine.Solve(text[:2],'ab')

            print('\nThe cipher key is: alpha='+str(alpha),'beta='+str(beta))

        elif cipherno == '2':
            text = AskText('2')
            key = Vigenere.Attack(text)

            print('\nThe cipher key is:', str(key))