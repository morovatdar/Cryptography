from cryptomath import cryptomath

def encrypt(message, e, n):
    
    message.lower()
    
    message_number = ''
    for char in message:
        num = ord(char) - 96
        if num < 10: message_number += '0' + str(num)
        else: message_number += str(num)
    print(message_number)
    return pow(int(message_number), e, n)


def decrypt(ciphernumber, d, n):
    
    message_number = str(pow(ciphernumber, d, n))
    print(message_number)
    if len(message_number) % 2 !=0 : message_number = '0' + message_number
    
    message = ''
    for index in range(0, len(message_number), 2):
        text = chr(int(message_number[index:index+2]) + 96)
        message += text
        
    return message


if __name__ == "__main__":
    p = 885320963
    q = 238855417
    e = 9007
    
    n = p * q
    d = cryptomath.findModInverse(e, (p-1)*(q-1))
    
    message = 'crypto'
    cipher = encrypt(message, e, n)
    print('\nThe encrypted message is:', cipher)
    plain = decrypt(cipher, d, n)
    print('\nThe decrypted message is:', plain)
    
    