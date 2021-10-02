import math
class cryptomath:

    def __init__(self):
        fff = 2

    def gcd(a,b):
        #This function finds the great common divisor of a and be

        #Check if a and b are integers
        if not(isinstance(a, int) and isinstance(b, int)):
            print('The input variables should be integers')
            return
        
        #Check if a is greater than b
        if a < b:
            a, b = b,a

        #Euclidean Algorithm
        while True:

            #Check if b is zero which finds the solution
            if b == 0:
                return a

            #Calculate the remainder and go to the next step
            r = a % b
            a, b = b, r


    def extendedgcd(a,b,c):
        #This functions find X and Y in the equation of aX+bY=c
        
        #Check if the equation has a solution
        d = abs(cryptomath.gcd(a,b))
        if (c % d) != 0:
            print('There is no feasible solution')
            return
        else: #Simplifying the equation
            a, b, c = int(a/d), int(b/d), int(c/d)

        r = [a,b]
        s = [1,0]
        t = [0,1]

        while True:

            #Calculate the quotient, remainder, and Bézout coefficients
            q = r[0] // r[1]
            rnew = r[0] % r[1]

            if rnew == 0:
                #print (c*s[1], c*t[1])
                #Find the smallest positive value for Y
                n = math.ceil(-c*t[1]/a)
                return r[1], c*s[1]-n*b, c*t[1]+n*a
            else:
                #Next step
                r = [r[1], rnew]
                s = [s[1], s[0] - q*s[1]]
                t = [t[1], t[0] - q*t[1]]


    def findModInverse(a,n):
        #This function finds the mod inverse of a
        d, s, t = cryptomath.extendedgcd(a,n,1)
        return s


    def PrimitiveRoot(a,n):
        return


    def SquareRoot(a,n):
        return

    #(a, b) = eval(input('enter two numbers: '))
    #print(gcd(a,b))

    #(a, b, c) = eval(input('enter three numbers: '))
    #print(extendedgcd(a,b,c))