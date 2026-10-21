global p

def convert(N,B1,B2):
    x = [0]
    for digit in reversed(N):
        x = multiply(x, [B1], B2)
        x = add(x, [digit], B2)
    return x

def scalarMultiply(scalar, a, p, B):
    r = [0, 0] #r =[x0,x1]
    scalar = Bto10(scalar, B)
    while scalar > 0:
        if scalar % 2 == 1:         # If e is oddd
            r = addEC(r,a,p, B)
        a = doublEC(a,p, B)  
        scalar //= 2                # Divide e by 2. The // takes the integer part.
    return r



def addEC(x,y,c, B):
    global p
    p = tentoB(c[0], B)

    
    x[0] = big_num_set_up(x[0], B)
    x[1] = big_num_set_up(x[1], B)
    y[0] = big_num_set_up(y[0], B)
    y[1] = big_num_set_up(y[1], B)

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

def doublEC(x,c, B):
    # print(c[0])
    global p
    x[0] = big_num_set_up(x[0], B)
    x[1] = big_num_set_up(x[1], B)
    p = tentoB(c[0], B)
    a = tentoB(c[1], B)
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

def Bto10(N, B):
    return sum(digit * B**i for i, digit in enumerate(N))

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



def test_suite():
    # Test modular inverse (correct)
    print(f"modinv([7], [11], {B}) = {modinv([7], [1,1], B)}")  # Expected: 8
    print(f"modinv([3], [26], {B}) = {modinv([3], [6,2], B)}")  # Expected: 9
    
    # # Test multiplication (correct)
    print(f"multiply([3], [4], {B}) = {multiply([3], [4], B)}")  # Expected: [2,1]
    print(f"multiply([7], [11], {B}) = {multiply([7], [1,1], B)}")  # Expected:[7,7]
    
    # Test subtraction (correct)
    print("Test 2:", subtract([7, 8, 9], [5, 6, 7], 10))  # Expected: [2, 2, 2]
    print("Test 3:", subtract([0, 3, 0, 1], [3, 4], 10))  # Expected: [7, 8, 9]
    
    # Test addition(correct)
    print("Addition:", add([7, 8, 9], [5, 6, 7], 10))  # Expected: [2, 5, 7, 1]
    print("Addition", add([3, 4], [7, 8, 9], 10))    # Expected: [0, 3, 0, 1]
    print("Addition", add([2], [0, 5], 10))             # Expected: [2, 5]
    
    #Test division (correct)
    print(f"divide([80], [40], {B}) = {divide([0,8], [0,4], B)}")  # Expected: [2],[0]
    print(f"divide([15], [5], {B}) = {divide([5,1], [5], B)}")  # Expected: [3],[0]
    print(f"divide([13], [2], {B}) = {divide([3,1], [2], B)}")  # Expected: [6],[1]
    
    #Test Reduction
    print("Test 1:", reduce([5], [0,1], 10))  # Expected: [5] 
    print("Test 2:", reduce([3,2], [0,1], 10))  # Expected: [3] 
    print("Test 3:", reduce([5,2], [0,1], 10))  # Expected: [5]
    print("Test 4:", reduce([5,1], [9], 10))
    
    # Test big number setup
    B = 10  # Elliptic curve modulus
    print(f"big_num_set_up([7, 9], {B}) = {big_num_set_up([7, 9], B)}")  # Big number setup test
    print(f"big_num_set_up([59], {B}) = {big_num_set_up([59], B)}")  #NO convert from num to list 
    
    print("\n Test elliptic curve point addition")
# Test suite for addEC(x, y, c, B)
    print(f"addEC([0, 0], [0, 0], [997, 187, 658], {B}) = {addEC([0, 0], [0, 0], [997, 187, 658], B)}  # Expected: [0,0]")
    print(f"addEC([0, 0], [259, 116], [997, 187, 658], {B}) = {addEC([0, 0], [259, 116], [997, 187, 658], B)}  # Expected: [259,116]")
    print(f"addEC([918, 431], [0, 0], [997, 187, 658], {B}) = {addEC([918, 431], [0, 0], [997, 187, 658], B)}  # Expected: [918,431]")
    print(f"addEC([918, 431], [918, 566], [997, 187, 658], {B}) = {addEC([918, 431], [918, 566], [997, 187, 658], B)}  # Expected: [0,0]")
    # print(f"addEC([918, 431], [259, 116], [997, 187, 658], {B}) = {addEC([918, 431], [259, 116], [997, 187, 658], B)}  # Expected: [954,104]")
    # print(f"addEC([895, 33], [179, 724], [997, 641, 72], {B}) = {addEC([895, 33], [179, 724], [997, 641, 72], B)}  # Expected: [124,316]")
    # print(f"addEC([351, 99], [861, 209], [997, 449, 85], {B}) = {addEC([351, 99], [861, 209], [997, 449, 85], B)}  # Expected: [48,25]")
    # print(f"addEC([887, 690], [989, 842], [997, 812, 126], {B}) = {addEC([887, 690], [989, 842], [997, 812, 126], B)}  # Expected: [865,27]")
    # print(f"addEC([251, 445], [23, 981], [1009, 506, 186], {B}) = {addEC([251, 445], [23, 981], [1009, 506, 186], B)}  # Expected: [525,801]")
    # print(f"addEC([459, 851], [109, 928], [1009, 273, 538], {B}) = {addEC([459, 851], [109, 928], [1009, 273, 538], B)}  # Expected: [615,717]")
    # print(f"addEC([472, 594], [709, 484], [1009, 761, 603], {B}) = {addEC([472, 594], [709, 484], [1009, 761, 603], B)}  # Expected: [831,654]")
    # print(f"addEC([136, 943], [16, 70], [1009, 391, 602], {B}) = {addEC([136, 943], [16, 70], [1009, 391, 602], B)}  # Expected: [652,449]")
    # print(f"addEC([893, 9], [868, 790], [1013, 742, 812], {B}) = {addEC([893, 9], [868, 790], [1013, 742, 812], B)}  # Expected: [638,534]")
    # print(f"addEC([910, 565], [950, 449], [1013, 507, 388], {B}) = {addEC([910, 565], [950, 449], [1013, 507, 388], B)}  # Expected: [610,591]")
    # print(f"addEC([880, 603], [184, 684], [1013, 936, 282], {B}) = {addEC([880, 603], [184, 684], [1013, 936, 282], B)}  # Expected: [157,697]")
    # print(f"addEC([797, 515], [90, 498], [1013, 139, 838], {B}) = {addEC([797, 515], [90, 498], [1013, 139, 838], B)}  # Expected: [373,587]")
    # print(f"addEC([787, 47], [37, 382], [1019, 53, 581], {B}) = {addEC([787, 47], [37, 382], [1019, 53, 581], B)}  # Expected: [461,609]")
    # print(f"addEC([963, 403], [570, 436], [1019, 397, 550], {B}) = {addEC([963, 403], [570, 436], [1019, 397, 550], B)}  # Expected: [347,82]")
    # print(f"addEC([486, 764], [744, 680], [1019, 300, 858], {B}) = {addEC([486, 764], [744, 680], [1019, 300, 858], B)}  # Expected: [656,808]")
    # print(f"addEC([798, 700], [211, 557], [1019, 569, 886], {B}) = {addEC([798, 700], [211, 557], [1019, 569, 886], B)}  # Expected: [364,916]")
    # print(f"addEC([305, 689], [665, 145], [1021, 141, 798], {B}) = {addEC([305, 689], [665, 145], [1021, 141, 798], B)}  # Expected: [800,59]")
    # print(f"addEC([515, 111], [981, 210], [1021, 292, 323], {B}) = {addEC([515, 111], [981, 210], [1021, 292, 323], B)}  # Expected: [193,251]")
    # print(f"addEC([860, 208], [490, 479], [1021, 939, 907], {B}) = {addEC([860, 208], [490, 479], [1021, 939, 907], B)}  # Expected: [893,277]")
    # print(f"addEC([624, 54], [177, 637], [1021, 773, 243], {B}) = {addEC([624, 54], [177, 637], [1021, 773, 243], B)}  # Expected: [952,488]")


    ##TEST DOUBLE EC
    print(f"doublEC([0, 0], [0, 0], [997, 187, 658], {B}) = {doublEC([0, 0], [997, 187, 658], B)}  # Expected: [0,0]")
    print(f"doublEC([918, 431], [997, 187, 658], {B}) = {doublEC([918, 431], [997, 187, 658], B)}  # Expected: [580,560]")
    print(f"doublEC([895, 33], [997, 641, 72], {B}) = {doublEC([895, 33], [997, 641, 72], B)}  # Expected: [631,760]")
    print(f"doublEC([351, 99], [997, 449, 85], {B}) = {doublEC([351, 99], [997, 449, 85], B)}  # Expected: [268,801]")
    print(f"doublEC([251, 445], [1009, 506, 186], {B}) = {doublEC([251, 445], [1009, 506, 186], B)}  # Expected: [426,651]")
    # print(f"doublEC([887, 690], [997, 812, 126], {B}) = {doublEC([887, 690], [997, 812, 126], B)}  # Expected: [12,98]")
    # print(f"doublEC([459, 851], [1009, 273, 538], {B}) = {doublEC([459, 851], [1009, 273, 538], B)}  # Expected: [380,492]")
    # print(f"doublEC([472, 594], [1009, 761, 603], {B}) = {doublEC([472, 594], [1009, 761, 603], B)}  # Expected: [906,946]")
    # print(f"doublEC([136, 943], [1009, 391, 602], {B}) = {doublEC([136, 943], [1009, 391, 602], B)}  # Expected: [45,902]")
    # print(f"doublEC([893, 9], [1013, 742, 812], {B}) = {doublEC([893, 9], [1013, 742, 812], B)}  # Expected: [452,764]")
    # print(f"doublEC([910, 565], [1013, 507, 388], {B}) = {doublEC([910, 565], [1013, 507, 388], B)}  # Expected: [554,363]")
    # print(f"doublEC([880, 603], [1013, 936, 282], {B}) = {doublEC([880, 603], [1013, 936, 282], B)}  # Expected: [103,194]")
    # print(f"doublEC([797, 515], [1013, 139, 838], {B}) = {doublEC([797, 515], [1013, 139, 838], B)}  # Expected: [438,136]")
    # print(f"doublEC([787, 47], [1019, 53, 581], {B}) = {doublEC([787, 47], [1019, 53, 581], B)}  # Expected: [776,979]")
    # print(f"doublEC([963, 403], [1019, 397, 550], {B}) = {doublEC([963, 403], [1019, 397, 550], B)}  # Expected: [132,812]")
    # print(f"doublEC([486, 764], [1019, 300, 858], {B}) = {doublEC([486, 764], [1019, 300, 858], B)}  # Expected: [214,638]")
    # print(f"doublEC([798, 700], [1019, 569, 886], {B}) = {doublEC([798, 700], [1019, 569, 886], B)}  # Expected: [390,283]")
    # print(f"doublEC([305, 689], [1021, 141, 798], {B}) = {doublEC([305, 689], [1021, 141, 798], B)}  # Expected: [646,231]")
    # print(f"doublEC([515, 111], [1021, 292, 323], {B}) = {doublEC([515, 111], [1021, 292, 323], B)}  # Expected: [117,50]")
    # print(f"doublEC([860, 208], [1021, 939, 907], {B}) = {doublEC([860, 208], [1021, 939, 907], B)}  # Expected: [8,938]")
    # print(f"doublEC([624, 54], [1021, 773, 243], {B}) = {doublEC([624, 54], [1021, 773, 243], B)}  # Expected: [342,591]")



test_suite()

