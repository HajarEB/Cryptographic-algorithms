
# Compute a^e mod p using square-and-multiply
def power_mod(a, e, p):
# a: base, e: power, p: modulo
    r = 1
    while e > 0:
        if e % 2 == 1:         # If e is odd,
            r = (r * a) % p       # multiply the result with a.
        a = (a * a) % p        # Always square a and reduce modulo p
        e //= 2                # Divide e by 2. The // takes the integer part.
    return r

# Return Bézout coefficients x, y such that ax + by = gcd(a, b)
def modified_EEA(a, b):
    if b == 0:
        return 1, 0
    else:
        x, y = modified_EEA(b, a%b)
        return y, x - (a//b) * y

# Probabilistic Miller-Rabin primality test
def miller_rabin(pp, s): #pp: value, s: num of rounds
    from random import randrange    # like randint but works like range()
    if pp < 2:
        return False
    if pp in (2, 3):
        return True
    if pp % 2 == 0:
        return False
    u = 0              # exponent of highest power of 2 dividing pp-1
    r = pp - 1
 
    while r % 2 == 0:   # as long as r is even
        u += 1
        r //= 2
        
    # Now pp = 2^u * r
    for _ in range(s):      # k rounds with a dummy index _
        a = randrange(2, pp - 1)  # the highest choice is pp-2
        z = power_mod(a, r, pp)      # z = (a**r)%pp
        if z == 1 or z == pp - 1:
            continue                # pick new 'a' (if there are still rounds)
        for _ in range(u - 1):      # u-1 squarings
            z = power_mod(z,2, pp)   
            if z == pp - 1:          
                break           # stop squaring, ... pick new 'a'
        else:               # this associates with the last 'for', and
            return False    # ... leads here if the loop did not 'break' 
    return True
    
    
# Find the smallest probable prime greater than or equal to N   
def findPrime(N):
    
    if N <= 2:
        return 2

    smallp = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
    
    sieve = [ (-N) % p for p in smallp]
    i = 0
  
    while True:
        if N + i in smallp:
            return N + i

        prime = 1
        for p in range(len(smallp)):
            if i % smallp[p] == sieve[p]: 
                prime = 0 
                
                break
        
        if prime ==1:
            isPrime = miller_rabin(N + i, 10)
            if isPrime:
                return N+i
        i += 1
        
# Find the smallest primitive root modulo prime p
def find_prim_root(powers,p):
    i = 2
    while True: 
        ok = 1
        for power in powers:
            val = power_mod(i, power, p)
            if val == 1:
                ok = 0
                break
        if ok == 1:
            return i
        i+= 1
 

# solves  c ≡ u (mod p) and c ≡ v (mod q)
def chinese_remainder (u, v, p, q):
    x, y = modified_EEA(p,q)
    
    if x * p + y * q !=1:
        raise ValueError("p and q must be coprime")
    
    return  (v * x * p + u * y * q) % (p*q)

if __name__ == "__main__":

    # P8 - Prime search
    print("Next probable prime:",  findPrime(1000000))
            
    # P9 - Primitive root
    p = 1009
    prime_factors = [2, 3, 7]  # Distinct factors of 1008
    powers = [(p - 1) // factor for factor in prime_factors]
    print("Primitive root:", find_prim_root(powers, p))

    # P9 - Chinese Remainder Theorem
    print("CRT result:", chinese_remainder(123, 456, 1009, 1013))

   
        



        
            
    
    
