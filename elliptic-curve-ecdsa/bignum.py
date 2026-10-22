global p

#subtract(M, N, B)
#add(M, N, B):
#subtract(M, N, B)
#multiply(M, N, B)
#modsubtract(M, N, P, B)
#normalize(N, B)
#compare(M, N)
#divide(M, N, B)
#reduce(M,P,B)
#EEA(M, N, B)
#scalarMultiply(scalar, a, p, B)
#Bto10(N, B)


def convert(N,B1,B2):
    x = [0]
    for digit in reversed(N):
        x = multiply(x, [B1], B2)
        x = add(x, [digit], B2)
    return x

def double_addECbig(A,k, c, Base):
    r = [[0], [0]] #r =[x0,x1]
    while compare(k, [0]) == 1:
        if compare(reduce(k, [2], Base),[1]) == 0:         # If e is odd
            r = addECbig(r,A,c, Base)
        A = doublECbig(A,c, Base)  
        k,_,_,_ = divide(k, [2], Base)               # Divide e by 2. The // takes the integer part.
    return r


# def scalarMultiply(scalar,a, c, B):
#     r = [[0], [0]] #r =[x0,x1]
#     while compare(scalar, [0]) == 1:
#         if compare(reduce(scalar, [2], B),[1]) == 0:         # If e is odd
#             r = addECbig(r,a,c, B)
#         a = doublECbig(a,c, B)  
#         scalar,_,_,_ = divide(scalar, [2], B)               # Divide e by 2. The // takes the integer part.
#     return r




def addECbig(x,y,c, B):
    global p
    p = c[0]

    if compare(reduce(x[0], p, B), [0]) == 0  and compare(reduce(x[1], p, B), [0])== 0 : #if (x[0]%c[0] == x[1]%c[0]  and x[1]%c[0]== 0):
        return [reduce(y[0],p,B), reduce(y[1],p,B)] #return [y[0]%c[0], y[1]%c[0]]
    elif compare(reduce(y[0], p, B), [0]) == 0  and compare(reduce(y[1], p, B), [0]) == 0: # elif (y[0]%c[0] == y[1]%c[0] and y[1]%c[0]== 0):
        return [reduce(x[0],p,B), reduce(x[1],p,B)] # return [x[0]%c[0], x[1]%c[0]]
    elif compare(reduce(add(y[1], x[1], B), p, B), [0]) == 0 and compare(modsubtract(y[0], x[0], p, B), [0]) == 0: #elif (y[1]%c[0]==-x[1]%c[0] and x[0]%c[0] == y[0]%c[0]):
        return [[0], [0]] # return [0,0]
    
    numerator = modsubtract(x[1],y[1], p, B) #(x[1]-y[1] ) 
     
    denominator = modsubtract(x[0],y[0], p, B) # x[0] - y[0]
    
    denominatorInverse = modinv(denominator, p, B)
    
    s =  multiply(numerator, denominatorInverse, B)  #(numerator/ denominator)
    s = reduce(s,p,B)  # s = s % c[0]
    return getXandY(p, s, x[0], y[0], x[1], B)

def getXandY(p,s, x1,x2, y1, B):

    s_2 = multiply(s, s, B)
    addition = add(x1,x2, B)
    x3 = modsubtract(s_2, addition, p, B)   # x3  =(s*s - (x[1] +x2) )% p

    sub = subtract(x1, x3, B)
    mult = multiply(s, sub, B)
    y3 = modsubtract(mult, y1,p,B) #y3 = (s*(x[1] -x3) -y[1])%p
    return [x3,y3]
    
def big_num_set_up(x, B):
    x = tentoB(x, B)
    return normalize(x, B)

def doublECbig(x,c, B):
    # print(c[0])
    global p
    p = c[0]
    a = c[1]
    # x[0] = big_num_set_up(x[0], B)
    # x[1] = big_num_set_up(x[1], B)
    # p = tentoB(c[0], B)
    # a = tentoB(c[1], B)
    if compare( reduce(x[0], p, B), [0]) == 0  and compare(reduce(x[1], p, B), [0]) == 0: #if (x[0]%c[0] == x[1]%c[0] and x[1]%c[0]== 0):
        return [[0], [0]] #return [0, 0]  

    mult_1 = multiply(x[0], x[0], B)

    mult_2 = multiply([3], mult_1, B)

    numerator = add(mult_2, a, B) #3*(x[0]**2) + c[1]

    denominator = multiply([2], x[1], B)  #2* x[1]

    denominatorInverse = modinv(denominator,p, B)
    s = multiply(numerator, denominatorInverse, B) #(numerator/ denominator)
    s = reduce(s,p,B) # s = s % c[0]
    return getXandY(p, s, x[0], x[0], x[1], B)


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
        return normalize(l[::-1], B)



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
    else:   
        return modsubtract(M,N, p, B) 
       
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

def multiply(M, N, B):
    addList = []
    for j in range(len(N)): 
        mult = [0]*j
        for i in M:
            mult.append(i * N[j])
        addList = add(addList,mult, B)
    return normalize(addList, B)


def modsubtract(M, N, P, B):
    if compare(M,N) == 1 or compare(M,N) == 0:
        result = subtract(M,N, B)
    else:
        addition = M
        while compare(addition,N) != 1 and compare(addition,N) != 0:
            addition = add(P,addition, B)
        result = subtract(addition,N, B)
    return reduce(result, P, B)

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
        Q, R,_,_ = divide(M, P, B)
        return R
    

  
    
# def test():
#     B = 10
#     point1 = [[8,1,9], [1,3,4]]
#     output = point1
#     c = [[7,9,9], [7,8,1], [8,5,6]]
#     for i in range(2):
#         output = doublECbig(output,c, B)
#         # print("double",i+1,  res)
#         i +=1
#     # output = addECbig(point1,res, c, B)
    # print("add",output)
    # print("output", scalarMultiply([4],[[8,1,9], [1,3,4]], [[7,9,9], [7,8,1], [8,5,6]], B )) 
    # print(f"doublECbig([918, 431], [997, 187, 658], {B}) = {doublECbig([[8,1,9], [1,3,4]],[[7,9,9], [7,8,1], [8,5,6]], B)}  # Expected: [580,560]")
    # print(f"doublECbig([895, 33], [997, 641, 72], {B}) = {doublECbig([[5,9,8], [3,3]], [[7,9,9], [1,4,6], [2,7]], B)}   # Expected: [631,760]")
    # print(f"doublECbig([351, 99], [997, 449, 85], {B}) = {doublECbig([[1,5,3], [9,9]], [[7,9,9],[9,4,4], [5,8]], B)}  # Expected: [268,801]")
    # print(f"doublECbig([251, 445], [1009, 506, 186], {B}) = {doublECbig([[1,5,2], [5,4,4]], [[9,0,0,1], [6,0,5], [6,8,1]], B)}  # Expected: [426,651]")
    # print(f"doublECbig([887, 690], [997, 812, 126], {B}) = {doublECbig([[7,8,8], [0,9,6]], [[7,9,9], [2,1,8], [6,2,1]], B)}  # Expected: [12,98]")
    # print(f"doublECbig([459, 851], [1009, 273, 538], {B}) = {doublECbig([[9,5,4], [1,5,8]], [[9,0,0,1], [3,7,2], [8,3,5]], B)}  # Expected: [380,492]")
    
    # print(f"addECbig([918, 431], [259, 116], [997, 187, 658], {B}) = {addECbig([[8,1,9], [1,3,4]], [[9,5,2], [6,1,1]], [[7,9,9], [7,8,1], [8,5,6]], B)}  # Expected: [954,104]")
    # print(f"addECbig([895, 33], [179, 724], [997, 641, 72], {B}) = {addECbig([[5,9,8], [3,3]], [[9,7,1], [4,2,7]], [[7,9,9], [1,4,6], [2,7]], B)}  # Expected: [124,316]")
    # print(f"addECbig([351, 99], [861, 209], [997, 449, 85], {B}) = {addECbig([[1,5,3], [9,9]], [[1,6,8], [9,0,2]], [[7,9,9], [9,4,4], [5,8]], B)}  # Expected: [48,25]")
   
# test()
