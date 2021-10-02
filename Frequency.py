def LetterFrequency(text):

    count = [0] * 26
    #Count the letters
    for i in range(26):
        count[i] = text.count(chr(i+97))

    frequency = [0] * 26
    #Calculate the frequency of letters
    for i in range(26):
        frequency[i] = count[i] / sum(count)

    return frequency

if __name__ == "__main__":
    
    print('**************************************************************')
    print('This program calculates the frequency of all letters in a text')
    print('**************************************************************')
    
    flag = False
    while flag == False:
        text = input("What is the text? ")
        
        #Check if the input text contains any letter
        lettercount = 0
        for char in text:
            if char.isalpha():
                lettercount += 1
        if lettercount != 0:
            flag = True
            text = text.lower()
        else:
            print('The text should contain at least some letters!')

    #Call the letter frequency function
    frequency = LetterFrequency(text)

    #Print the result
    print('The frequency of letters is as follows: ')
    for i in range(26):
        print(chr(i+97), round(frequency[i],2))

