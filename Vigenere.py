from Frequency import Frequency
import numpy as np

class Vigenere:

    def __init__(self):
        pass
    
    def AskKey():
        #Input the cipher key
        flag = False
        while flag == False:
            key = input("\nPlease enter the cipher key (either as a word or a vector of numbers separated with commas): ")

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

        return key


    def Encode(key, text):
        
        text = np.array([ord(ch) for ch in text]) #Convert the text to ASCII values
        text = text -97 #Rescale values to be between 0 and 25

        KeyLength = len(key)
        TextLength = len(text)
        result = ''

        #Add the key value to the text value on mod 26, then convert it to letters
        for i in range(TextLength):
            value = (text[i] + key[i % KeyLength]) % 26
            result = result + chr(value + 97)

        return result


    def Decode(key, text):
        
        key = -key
        text = np.array([ord(ch) for ch in text]) #Convert the text to ASCII values
        text = text -97 #Rescale values to be between 0 and 25

        #Call the encoder function based on the negative key
        return Vigenere.Encode(key, text)


    def Attack(text):

        textint = np.array([ord(ch) for ch in text]) #Convert the text to ASCII values
        textint = textint -97 #Rescale values to be between 0 and 25

        TextLength = len(text)
        MaxShift = 10
        count = np.zeros(MaxShift+1)
        for i in range(1, MaxShift+1):
            count[i] = np.count_nonzero(textint[:TextLength-i] == textint[i:])

        keyLength = np.argmax(count)
        key = np.zeros(keyLength)
        A0 = np.transpose(Frequency.Reference())
        A0 = A0[0,:]

        for i in range(keyLength):
            selecttext = text[i::keyLength]

            W = Frequency.SingleFrequency(selecttext)
            W = W[:,0]

            weights = np.zeros(26)
            for j in range(26):
                weights[j] = np.matmul(np.roll(A0, j), W)

            key[i] = np.argmax(weights)

        return key


if __name__ == "__main__":
    text = 'VVHQWVVRHMUSGJGTHKIHTSSEJCHLSFCBGVWCRLRYQTFSVGAHWKCUHWAUGLQHNSLRLJSHBLTSPISPRDXLJSVEEGHLQWKASSKUWEPWQTWVSPGOELKCQYFNSVWLJSNIQKGNRGYBWLWGOVIOKHKAZKQKXZGYHCECMEIUJOQKWFWVEFQHKIJRCLRLKBIENQFRJLJSDHGRHLSFQTWLAUQRHWDMWLGUSGIKKFLRYVCWVSPGPMLKASSJVOQXEGGVEYGGZMLJCXXLJSVPAIVWIKVRDRYGFRJLJSLVEGGVEYGGEIAPUUISFPBTGNWWMUCZRVTWGLRWUGUMNCZVILE'
    print(Vigenere.Attack(text))
