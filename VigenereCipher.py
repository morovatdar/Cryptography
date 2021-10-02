from cryptomath import cryptomath
import numpy as np

def VigenereEncode(key, text):
    
    KeyLength = len(key)
    TextLength = len(text)
    result = ''

    #Add the key value to the text value on mod 26, then convert it to letters
    for i in range(TextLength):
        value = (text[i] + key[i % KeyLength]) % 26
        result = result + chr(value + 97)

    return result

def VigenereDecode(key, text):
    
    key = -key
    
    #Call the encoder function based on the negative key
    return VigenereEncode(key, text)

if __name__ == "__main__":
    
    print('**************************************************************')
    print('This program encode and decode a given text by Vigenere Cipher')
    print('**************************************************************')

    #Find out whether the user wants to encode or decode the text
    flag = False
    while flag == False:
        action = input("Do you want to 'encode' or 'decode'? ")

        #Check if the input command includes 'encode' or 'decode' commands
        if action != None and ('encode' in action or 'decode' in action):
            flag = True
        else:
            print("Command not found!")

    #Input the cipher key
    flag = False
    while flag == False:
        key = input("Please enter the cipher key (either as a word or a vector of numbers): ")

        #Check if the cipher key is a word or vector
        if ',' in key:
            #Check if the cipher vector elements are all numbers
            try:
                key = np.array(eval(key))
                #Check if the cipher vector elements are all integers between 0 and 25
                if all(x >= 0 and x <= 25 for x in key) and all(isinstance(x, np.int32) for x in key):
                    flag = True
                else:
                    print('The inetgers in the key vector should be integers between 0 and 25!')
            except:
                print('The key vector should include only numbers separated with commas!')
        else:
            key = key.lower()
            #Check if the cipher key charaters are all alphabet letters
            if key.isalpha():
                key = np.array([ord(ch) for ch in key])
                key = key - 97
                flag = True
            else:
                print('The key word should include only English letters!')


    #Input the text to be encrypted or decrypted
    flag = False
    while flag == False:
        if 'encode' in action:
            text = input("What is the plain text? ")
        else:
            text = input("What is the cipher text? ")
        #Check if all characters of the text are alphabet letters
        if text.isalpha():
            flag = True
            text = text.lower() #Convert the input text to lowercase
            text = np.array([ord(ch) for ch in text]) #Convert the text to ASCII values
            text = text -97 #Rescale values to be between 0 and 25
        else:
            print('The text should contain only letters!')

    #Call the function of encoding or decoding based on the user's entry
    #And, show the result.
    if 'encode' in action:
        resulttext = VigenereEncode(key, text)
        print('The encoded text is: ' + resulttext.upper()) #Convert the cipher text to uppercase
    else:
        resulttext = VigenereDecode(key, text)
        print('The decoded text is: ' + resulttext)