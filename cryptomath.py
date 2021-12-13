import math
from sympy import ntheory
from numpy import linalg
import random

class cryptomath:

    def __init__(self):
        pass

    def gcd(a,b):
        """ The great common divisor (GCD) of a and b """
        #Check if a and b are integers
        if not(isinstance(a, int) and isinstance(b, int) and a!=0 and b!=0):
            print('The input variables should be non-zero and integers')
            return

        #Considering absolute values of a and b
        a, b = abs(a), abs(b)
        #Check if a is greater than b
        if a < b: a, b = b, a

        #Euclidean Algorithm
        while True:
            #If b is zero, it found the solution otherwise go to the next step
            if b == 0: return a
            a, b = b, a % b


    def extendedgcd(a, n):
        """ Find X and Y in the equation of aX + nY = 1 """
        # Check if the equation has a solution
        d = abs(cryptomath.gcd(a, n))
        if d != 1:
            print('There is no feasible solution for', str(a)+'X +', str(n)+'Y = 1')
            return
        
        if a == 0: 
            return (n, 0, 1)
        else:
            d, Y, X = cryptomath.extendedgcd(n % a, a)
            return (d, X - (n // a) * Y, Y)
        
        # Find X and Y in the equation of aX+nY=c
        # c = 1
        #Check if the equation has a solution
        # d = abs(cryptomath.gcd(a, n))
        # if (c % d) != 0:
        #     print('There is no feasible solution for', str(a)+'X +', str(n)+'Y =', c)
        #     return
        # else: #Simplifying the equation
        #     a, n, c = int(a/d), int(n/d), int(c/d)
        # r, s, t = [a,n], [1,0], [0,1] # Initialize the remainder and Bézout coefficients
        # while True:
        #     q, rnew = r[0] // r[1], r[0] % r[1] # The new quotient and remainder
        #     if rnew == 0:
        #         n = math.ceil(-c*t[1]/a) #Find the smallest positive value for Y
        #         return r[1], c*s[1]-n*n, c*t[1]+n*a
        #     else:
        #         r, s, t = [r[1], rnew], [s[1], s[0] - q*s[1]], [t[1], t[0] - q*t[1]] #Next step


    def findModInverse(a, n):
        """ The mod inverse of a (mod n) """
        #Check if GCD of a and n 
        d = abs(cryptomath.gcd(a,n))
        if d == 1 and a*n != 0:
            d, s, t = cryptomath.extendedgcd(a, n)
            return s % n
        else:
            print('There is no modular inverse. a and n should be non-zero and coprime.')
            return


    def PrimitiveRoot(a,n):
        """ Verify if 'a' is a primitive root (mod n) """
        #Check if n is prime
        if not(ntheory.isprime(n)):
            print ('p is not a prime number')
            return

        roots = ntheory.primefactors(n-1) #Find the roots of n-1

        #Check if there is a 1 among the residuals of a^(n-1)/q mode n
        for q in roots:
            if pow(a, (n-1)/q, n) == 1:
                return False

        #If there is no 1 among residuals, it is a primitive root
        return True


    def MatInvMod(M,n):
        """ The inverse of matrix M (mod n) """
        #Check if the determinant of matrix M and n are coprime
        detM = round(linalg.det(M))
        if cryptomath.gcd(detM,n) != 1:
            print('The matrix does not have an inverse.')
            return

        #Calculate the invers of determinant mod n
        detMinv = cryptomath.findModInverse(detM,n)

        #Calculate the normal inverse of N and then multiply it with its determinant 
        #and the inverse of determinant mod n and then again calculate mod n of the matrix
        return (detM * detMinv * linalg.inv(M)) % n
    
    
    def is_prime(n):
        """" Test if 'n' is prime or not with Miller-Rabin Primality Test """
        
        if n == 1 or n % 2 == 0: return False # 1 and even numbers are not prime
        if n == 2 or n == 3: return True # 2 and 3 are prime

        # Calculate the initial parameters n-1=(2**k)m
        m = n - 1
        k = 0
        while m % 2 == 0:
            m //= 2
            k += 1
        
        # Iterate the algorithm for 40 different a's   
        for _ in range(40):
            a = random.randrange(2, n - 1) # Choose a random integer a with 1<a<n-1
            
            b = pow(a, m, n) # b0 congruent a**m (mod n)
            if b == 1 or b == n - 1: continue # if b0 congruent +1 or -1, n can be prime
            
            flag = False
            for _ in range(k-1):
                b = pow(b, 2, n) # bi congruent b_(i-1)**2 (mod n)
                if b == 1: return False # If bi congruent +1, n is composite
                if b == n-1: # If bi congruent -1, n can be prime
                    flag = True
                    break
                
            if flag == False: return False # If b_(k-1) is not congruent -1, n is composite
            
        return True # If after 40 different a we cannot conclude n is composite, then n is prime
    
    
    def random_prime(b):
        """ Create a random prime number between 2**(b+1)-1 and 2**b-1 """
        flag = True
        while flag:
            # Create a random integer between 2**(b+1)-1 and 2**b-1
            candidate = random.randrange(2**(b-1)+1, 2**b-1)
            if cryptomath.is_prime(candidate): flag = False # Check if it is prime
            
        return candidate
    
    
    def factor(n, m):
        """ factor number n, with a method of choice m: 
            Fermat's method (m=Fermat)
            Pollard rho (m=rho)
            Pollard p-1 (m=p-1)"""
            
        if cryptomath.is_prime(n): return []
            
        if m == 'Fermat':
            i = 1
            m = n + 1
            # Search to find an integer z such that z**2=n+i**2
            while m != math.isqrt(m) ** 2:
                i += 1
                m = n + i**2
            z = math.sqrt(m)    
            return [z-i, z+i]
        
        elif m == 'rho':
            x, y, d = 2, 2, 1

            while d == 1:
                x = (x**2 + 1) % n
                y = ((y**2 + 1)**2 + 1) % n
                d = cryptomath.gcd(abs(x - y), n)

            if d == n: return []
            else: return [d, n/d]
            
        elif m == 'p-1':
            a, B = 2, 1500 # Choose an integer a and a bound B
            
            b = a % n 
            for i in range(B):
                b = pow(b, i+1, n)
                d = cryptomath.gcd(b-1, n)
                if d > 1: break
            
            if d == 1 or d == n: return []
            else: return [d, n/d]
    
    
    
if __name__ == "__main__":
    # a = 5210644015679228794060694325390955853335898483908056458352183851018372555735221
    # n = 68718821377
    # # n = 5165465619
    # print(cryptomath.factor(n, 'p-1'))
    # print(cryptomath.random_prime(128))
    
    print(cryptomath.findModInverse(9007,211463706672030192))
