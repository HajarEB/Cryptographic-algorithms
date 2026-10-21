# Given: absolute values M and N, with indication of their actual signs: Ms and Ms.
# Return the absolute value of M-N and the sign of M-N.
def signedsubtract(M,Ms,N,Ns,B):
    if Ms==0:
        if M != [0]: raise SystemExit("M is not zero but its sign is.")
        return N, -Ns
    if Ns==0:
        if N != [0]: raise SystemExit("N is not zero but its sign is.")
        return M, Ms
    comparison = compare(M,N)
    if Ms > 0:
        if Ns > 0:
            if comparison == 0:
                return [0], 0
            if comparison > 0:
                return subtract(M,N,B), 1   # M-N > 0
            else:
                return subtract(N,M,B), -1  # -(N-M) < 0
        else:
            return add(M,N,B), 1            # M-(-N) > 0
    else:
        if Ns > 0:
            return add(M,N,B), -1           # -(-M + N) < 0
        else:
            if comparison == 0:
                return [0], 0
            if comparison > 0:
                return subtract(M,N,B), -1  # -(-M-(-N)) < 0
            else:
                return subtract(N,M,B), 1   # -N-(-M) > 0

def EEA(M, N, B):
    x, y, u, v = [0], [1], [1], [0]
    xs, ys, us, vs = 0, 1, 1, 0         # the signs of x, y, u, v
    a = [ i for i in M]
    b = [ i for i in N]
    while a != [0]:
        q, r,_,_ = divide(b, a, B)      # q and r are always non-negative
        uXq = multiply(u, q, B)     
        vXq= multiply(v, q, B)
        if uXq == 0: uXqs = 0
        else:        uXqs = us
        if vXq == 0: vXqs = 0
        else:        vXqs = vs

        m, ms = signedsubtract(x, xs, uXq, uXqs, B)
        n, ns = signedsubtract(y, ys, vXq, vXqs, B)

        b, a = a, r

        x, y = u, v
        xs, ys = us, vs

        u, v = m, n
        us, vs = ms, ns

    gcd = b
    return gcd, x, xs, y, ys
	
# Invert bignum M modulo P in base B, assuming that
# the gcd of M and P equals 1. It would be good, and easy, to 
# check this in the function. Try to do it.
def modinv(M, P, B):
    gcd, x, xs, _, _ = EEA(M,P,B)
    if gcd != [1]:
        raise ValueError("Inverse does not exist")
    if xs < 0:                      # So, X := xs*x = -x < 0. Reduce it mod P:
        _,y,_,_ = divide( x, P, B)      # y := x mod P = -X mod P; Now y is in range 0..P-1.
        x = subtract(P,y,B)         # x := P-y = P - (-X mod P ) = X mod P, in range 0..P-1.
    return x

def divide(M, N, B):
    if N==[0]:
        raise ValueError("Division by zero")
    Q = []              # quotient
    R = normalize(M,B)  # remainder
    N_digit = N[-1] # most significant digit of the divisor
    N_len = len(N)  # divisor length
    countinner=0        # These two counters are for those of you
    countouter=0        # ... who want to study and improve the performance.

    # Repeat as long as the remainder didn't get below divisor
    while compare(R, N) >= 0:
        countouter += 1
        # Estimate the position for the next quotient digit 
        # and get the most significant digit (or two) of the remainder
        if R[-1] >= N_digit:
            estimate = len(R) - N_len 
            R_digit = R[-1]
        else:
            estimate = len(R) - N_len - 1
            R_digit = B * R[-1] + R[-2]

        # Estimate the next digit in the quotient using Python's division
        Q_digit_estimate = min(R_digit // N_digit, B-1)

        # Create a trial divisor
        trial = [0] * estimate + [Q_digit_estimate]

        # Make a (sub)trahend and adjust it and the trial as long as trahend is too big
        trahend = multiply(trial, N, B)
        while compare(trahend, R) > 0:
            countinner += 1
            Q_digit_estimate -= 1
            if Q_digit_estimate == 0: # if this goes to zero, we must move to lower significance
                trial.pop()
                trial[-1] = B-1        # ... and start from the biggest value there
                Q_digit_estimate = B-1
            else:
                trial[-1] = Q_digit_estimate

            trahend = multiply(trial, N, B) # This will be subtracted if looping does not continue

        R = subtract(R, trahend, B)
        Q = add(Q, trial, B)
    if not Q:
        return [0],R , countouter, countinner
    return Q, R , countouter, countinner  # See these two to know where the time was spent.



def reduce(M,P,B):
    if compare(M,P) == -1:
        return M
    else: 
        Q, R = divide(M, P, B)
        return R
        

#Convert a non-negative decimal number N to a bignum in base B
def tentoB(N, B):
    if isinstance(N, str):
        Nlength = len(N)
        N = int(N)
    else: 
        Nlength = len(str(N))
    if N == 0:
        return [0]
    else:
        l =[]
        i = Nlength 
        while i> 0:
            Bexp = B **i
            val = N // Bexp
            N = N - (val*Bexp)
            l.append(val)
            i -= 1
        l.append(N)
        return l[::-1]


def Bto10(N, B):
    return sum(digit * B**i for i, digit in enumerate(N))


def normalize(N, B):
    lenN = len(N)
    for i in range(lenN-1):   # Borrow from more significant side to make all non-negative
        if N[i] < 0:
            borrow = 1 + (-N[i]-1) // B # 
            N[i] += B * borrow
            N[i+1] -= borrow
    if N[-1] < 0:
        # Checking this in the beginning would not help when N[-2] is too far below zero.
        print ("The number is negative (resulting in ", N, ")")
        raise SystemExit

    for i in range(lenN-1, 0, -1): # remove leading zeros: leave N[0].
        if N[i]>0:
            break
        else:
            N.pop()
    carry = 0                   # carry excess values toward more significant side
    for i in range(len(N)): # first within the existing N,...
        N[i] += carry
        carry = N[i] // B
        N[i] %= B
    while carry > 0:        # ...and then extending N if needed
        N.append(carry % B)     # carry may be >= B, and .. 
        carry //= B             # ... then there is more to extend
    return N

#Compare 2 big nums M[] and N[]
def compare(M, N):
    if len(M) == len(N):
        for i, j in zip(M[::-1], N[::-1]): 
            if i > j:
                return 1
            elif j>i:
                return -1
        return 0
    elif len(M) >len(N):
        return 1
    return -1

#add 2 big nums M[] and N[]
def add(M, N, B):
    sum = [] 
    i = 0
    while i < len(M) or i < len(N):
        if i >= len(M) :
            valM = 0
            valN = N[i]
        elif i >= len(N):
            valN = 0 
            valM = M[i]
        else:
            valM = M[i]
            valN = N[i]
        sum.append(valM + valN)
        i += 1
    
    return normalize(sum, B)


def subtract(M, N, B):
    if compare(M,N) == 1 or compare(M,N) == 0:
        subtraction = [] 
        i = 0
        while i < len(M):
            if i >= len(N):
                valN = 0
                valM = M[i]
            else:
                valM = M[i]
                valN = N[i]
            i += 1
            subtraction.append(valM - valN)
        return normalize(subtraction, B)
    assert("M must be geater than N")
    
        

def multiply(M, N, B):
    addList = []
    for j in range(len(N)): 
        mult = [0]*j
        for i in M:
            mult.append(i * N[j])
        addList = add(addList,mult, B)
            
    return normalize(addList, B)


# Bignum N, given in base B1 is returned in base B2.
def convert(N,B1,B2):
    x = [0]
    for digit in reversed(N):
        x = multiply(x, [B1], B2)
        x = add(x, [digit], B2)
    return x

def modsubtract(M, N, P, B):
    if compare(M,N) == 1 or compare(M,N) == 0:
        result = subtract(M,N,B)
    else:
        addition = M
        while compare(addition,N) != 1 and compare(addition,N) != 0:
            addition = add(P,addition, B)
        result = subtract(addition,N,B)
    return result
        

# print(compare([1,0,3],[1,0,2]))
# print(compare([1,0,2], [1,0,3]))
# print(compare([1,0,2,5], [1,0,3]))
# print(compare([1,0,2], [1, 5, 0,2]))
# print(compare([1,0,2], [1,0,2]))
# print(add([3,2,8],[7,0,95],10))

#add
# print("Test 1:", add([1, 2, 3], [4, 5, 6], 10))  # Expected: [5, 7, 9]
# print("Test 2:", add([7, 8, 9], [5, 6, 7], 10))  # Expected: [2, 5, 7, 1]
# print("Test 3:", add([3, 4], [7, 8, 9], 10))    # Expected: [0, 3, 0, 1]
# print("Test 4:", add([10, 15, 20], [5, 10, 5], 30))  # Expected: [15, 25, 25]
# print("Test 5:", add([0], [0], 10))             # Expected: [0]
# print("Test 6:", add([9, 9, 9], [1], 10))       # Expected: [0, 0, 0, 1]
# print("Test 7:", add([1] + [0]*999 + [1], [1] + [0]*999 + [1], 10))  # Expected: [2] + [0]*999 + [2]


#subtract
# print("Test 1:", subtract([5, 7, 9], [1, 2, 3], 10))  # Expected: [4, 5, 6]
# print("Test 2:", subtract([7, 8, 9], [5, 6, 7], 10))  # Expected: [2, 2, 2]
# print("Test 3:", subtract([0, 3, 0, 1], [3, 4], 10))  # Expected: [7, 8, 9]
# print("Test 4:", subtract([15, 25, 25], [5, 10, 5], 30))  # Expected: [10, 15, 20]
# print("Test 5:", subtract([1], [0], 10))              # Expected: [1]
# print("Test 6:", subtract([1, 0, 0, 0], [1], 10))     # check
# print("Test 7:", subtract([0, 0, 0, 1], [1, 0, 0, 0], 10))     # Expected: [ 9, 9, 9]
# print("Test 8:", subtract([2] + [0]*999 + [2], [1] + [0]*999 + [1], 10))  # Expected: [1] + [0]*999 + [1]

#multiply
# print("Test 0:", multiply([3, 2, 1], [6, 5, 4], 10))  # [8, 8, 0, 6, 5]
# print("Test 1:", multiply([1, 2], [3, 4], 10))  # Expected: [3, 0, 9]
# print("Test 2:", multiply([9, 9], [9, 9], 10))  # Expected: [1, 0, 8, 9]
# print("Test 3:", multiply([0], [7, 8, 9], 10))  # Expected: [0]
# print("Test 4:", multiply([1, 2, 3], [4, 5, 6], 10))  # Expected: [4, 3, 9, 9, 0, 2]
# print("Test 5:", multiply([5], [5], 10))       # Expected: [5, 2]
# print("Test 6:", multiply([1, 0, 0], [1, 0, 0], 10))  # Expected: [1, 0, 0, 0, 0]
# print("Test 7:", multiply([1] + [0]*999, [1], 10))  # Expected: [1] + [0]*999
# print("Test 8:", multiply([1, 2], [3, 4], 5))   # Expected: [3, 0, 0, 2]
# print("Test 9:", multiply([15, 25, 20], [2, 3], 30))  # Expected: [0, 6, 28, 3, 2]


#modsubtract
# print("Test 1:", modsubtract([3], [2], [5], 10))  # Expected: [1]
# print("Test 2:", modsubtract([2], [3], [5], 10))  # Expected: [4]
# print("Test 3:", modsubtract([4], [4], [5], 10))  # Expected: [0] 
# print("Test 4:", modsubtract([7, 1], [5], [10], 10))  # Expected: [2, 1]
# print("Test 5:", modsubtract([9, 9], [8, 7], [100], 10))  # Expected: [1, 2]
# print("Test 6:", modsubtract([1], [9], [10], 10))  # Expected: [2]
# print("Test 7:", modsubtract([15, 25, 20], [5, 10], [30], 30))  # Expected: [10, 15, 20]
# print("Test 8:", modsubtract([0], [0], [5], 10))  # Expected: [0] 
# print("Test 9:", modsubtract([0, 0, 1], [9, 9], [1000], 10))  # CHECK: Expected: [1, 0, 0]  
# print("Test 10:", modsubtract([5, 5], [3, 3], [10], 10))  # Expected: [2, 2]

# print(modinv([0, 8, 3, 1], [7, 9, 9], 10) )

#reduce
# print("Test 1:", reduce([5], [10], 10))  # Expected: [5] 
# print("Test 2:", reduce([10], [10], 10))  # Expected: [0] 
# print("Test 3:", reduce([25], [10], 10))  # Expected: [5]
# print("Test 4:", reduce([0,2,5, 2,5, 1], [0,0,1], 10))  # Expected: [20] (because 152520 mod 100 = 20)
# print("Test 5:", reduce([1000], [999], 10))  # Expected: [1] (because 1000 mod 999 = 1)

