import numpy as np

class Frequency:

    def __init__(self):
        pass

    def SingleFrequency(text):
        #This function calculates the frequency of the different characters in the text
        text = text.lower()

        freqlist = np.zeros((26,2))
        totalcount = len(text)

        for i in range(26):
            freqlist[i,:] = [text.count(chr(i + 97)) / totalcount , i]

        return freqlist
    
        #return [[text.count(chr(i + 97)) / totalcount , i] for i in range(26)]


    def PairFrequency(text):
        #This function calculates the frequency of character pairs in the text

        freqlist = np.zeros((26,26))
        totalcount = len(text) - 1

        for i in range(26):
            for j in range(26):
                freqlist[i,j] = text.count(chr(i+97)+chr(j+97)) / totalcount

        return freqlist   

    
    def Reference():
        #This function shows the frequency of the different characters in English

        reference1 = np.loadtxt('1frequency.txt')
        reference1 = np.vstack((reference1, np.linspace(0, 25, num=26)))
        reference1 = np.transpose(reference1)

        return reference1
