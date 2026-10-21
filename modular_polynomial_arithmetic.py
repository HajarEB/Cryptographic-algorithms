# P1-a). Square and multiply
def power(a, e, p):
# a: base, e: power, p: modulo
    r = 1
    while e > 0:
        if e % 2 == 1:         # If e is odd,
            r = (r * a) % p       # multiply the result with a.
        a = (a * a) % p        # Always square a and reduce modulo p
        e //= 2                # Divide e by 2. The // takes the integer part.
    return r


#P1-b) EEA
def gcd(a, b):
   while a != 0:
      a, b = b % a, a
   return b

def modinvert(a, p):
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, p
    while v3 != 0:
      q = u3 // v3
      v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
	  
    # print(u1," :is The value of m")
    # print(u2," :is the value of p")
    # print(u3," :is the value of the gcd")
	
    return u1,u2,u3


# Trim the leading zeros from a polynomial. Leave [0] instead of nothing.
def trim_zero(r):
	while len(r)>1 and r[-1] == 0:
		r.pop()
	return r

# Remainder of polynomial division h/f where coefficients are modulo p.
# Equally (and hence the name):
# Reduce polynomial h with respect to polynomial f, mod p.
def reducepol(h,f,p):
	if f[-1] != 1:
		raise SystemExit("Your modulus polynomial is not monic!")
	# Initialize the remainder r to be h (not to modify h).
	r = h.copy()
	LenR = len(r)-1
	LenF = len(f)-1
	while LenR >= LenF:
		multResult = f.copy()
		if f[LenF]>r[LenR] or r[LenR]%f[LenF]!=0:
			m,n,gcdValue= modinvert(f[LenF],p)     #	a* a^(-1) ≡ 1 mod p
			coeff = (m * r[LenR])
		else:
			coeff = int(r[LenR]/f[LenF])
		degree = LenR-LenF
		g=[0]*(degree+1)
		g[degree]=coeff
		multResult = polmul(f,g,p)
		r =  polsub(r, multResult, p)
		LenR = len(r)-1
	return r

# a + b modulo p
def poladd(a, b, p):
	if len(a) >= len(b):
		res = [ (a[e] + b[e])%p for e in range(len(b)) ]
		res += [a[e]%p for e in range(len(b),len(a))]
	if len(a) < len(b):
		res = [ (a[e] + b[e])%p for e in range(len(a)) ]
		res += [b[e]%p for e in range(len(a),len(b))]
	return trim_zero(res)

# a - b modulo p
def polsub(a, b, p):
	b = [-b[e]%p for e in range(len(b))]	#Note: -x%y is (-x)%y, but z-x%y is z-(x%y), not z+(-x)%y
	return poladd(a,b,p)

# f*g modulo p
def polmul(f,g,p): 
	res = [0 for _ in range(len(f)+len(g)-1)]
	for i in range(len(f)):
		for j in range(len(g)):
			res[i+j] += f[i]*g[j]
	res = [res[i]%p for i in range(len(res))]
	return trim_zero(res)

# Format a polynomial with powers of x, in both directions.
# Doesn't work nicely with negative coefficients.
def pol2str(poly):
	string = gnirts = ""
	for e, c in enumerate(poly): # In this iteration poly[e] equals c.
		if e == 0:
			# Constant term. If it is 0, it is not printed, unless the rest is zero, too, 
			if c == 0 and any(poly):	# as checked by any(poly).
				continue
			string = f"{c}" + string
			gnirts = gnirts + f"{c} "
		elif c == 0:
			continue
		# Cases for x formatting
		elif c == 1 and e != 1:
			string = f"x^{e} + " + string
			gnirts = gnirts + f"+ x^{e}"
		elif c == 1 and e == 1:
			string = f"x + " + string
			gnirts = gnirts + f"+ x "
		elif c != 1 and e == 1:
			string = f"{c}x + " + string
			gnirts = gnirts + f"+ {c}x"
		else:
			string = f"{c}x^{e} + " + string
			gnirts = gnirts + f" + {c}x^{e}"
	if string[-3:] == " + ":
		string = string[:-3]
	if gnirts[:3] == " + ":
		gnirts = gnirts[3:]
	print( string )
	print( gnirts )

#calculate the product of coefficients
def nonModularProductCalc(remainder):
	sum = 0
	product = 1
	for i in remainder:
		if i != 0 :
			product = product*i
			sum = sum+i
	print(sum,"sum")
	if sum == 0:
		return 0
	else:
	    return product

#get constant c value
def getC(p):
    if p == 11:
        return 3
    elif p == 13:
        return 4
    elif p == 17:
        return 3
    elif p == 19:
        return 3
    elif p == 23:
        return 3
    elif p == 29:
        return 1
    elif p == 31:
        return 6
    elif p == 37:
        return 5
    else:
        return 1		

# find p:  smallest prime number >=d+10 
def getPrime (d):
    num= d+10
    while isPrime(num) is False:
        num+=1
        isPrime(num)
    return num

def isPrime(num):
    i= 2
    while i<num:
        if num% i==0:
            return False
        i+=1
    return True

#form f
def formF(c):
	f=[1,0,0,0,1] 
	f= [c]+f
	return f

#form h
def formH(studNum):
	h=[]
	for i in str(studNum) :
		if i.isdigit(): #detect wrong number formatting
			h.append(int(i))
		else:
			raise SystemExit("Invalid Student Number!")
	return h
			

if __name__=='__main__': 
	
	# Entered by the code tester
	studentNum= "22222222"
	d = 10
	if d>31 or d<1:
		raise SystemExit("Invalid date of Birth!")
	
	# generated automatically by the code    
	p = getPrime(d)
	c = getC(p) 
	f = formF(c)
	h = formH(studentNum)
	if len(h)<6: # as in the stimulator, the length of h is min 6 digits
		raise SystemExit("Invalid Student Number!")
	remainder = reducepol(h,f,p)
	r = nonModularProductCalc(remainder)
	
	#results
	print("r =",r,"and p =",p)
	
