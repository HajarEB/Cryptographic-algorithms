
pubkey = ['AF4DA60C5F2C9386200997AEA1F3', '76E716D95601A8D4E7265EC36A14'] #base 16
snum = '222222222' 

from bignum import*
from elliptic_curve import scalarMultiply
import random as rand



# A string N of hexadecimals (without initial 0x) into a bignum in base 16
def hexto16(N):
    return [int(h,16) for h in N[::-1]] # reverse order of the argument string

# A bignum N in base 16 into a string of hexadecimals
def from16tohex(N):
    return ''.join([hex(i)[2].upper() for i in N[::-1]])

# Convert a string of hexadecimals H (without initial 0x) to its representation in base B.
def hextoB(H,B):
    if B == 16:
        return hexto16(H)
    else:
        return convert(hexto16(H),16,B)

# Convert a bit string K to its representation in base B, via hexadecimals.
def bitstoB(K,B):
    res = ''
    while len(K) % 4 != 0:  # Pad K to a length that is a multiple of 4.
        K = '0'+K
    for i in range(0, len(K), 4): # Convert each chunk of four bits to an integer.
        chunk = K[i:i + 4]
        dec = int(chunk, 2)    
        res += hex(dec)[2:].upper()  # join them into a hex string
    return hextoB(res,B)

def get_privkey(snum):
    i=0
    while i <len(snum):   # loop over snum
        if not snum[i].isdigit():   #check if character in snum is digit
            snum = snum[:i]+snum[i+1:]   #if not, remove this character
        else:
            i+=1                         #increment the counter
    return snum

# Return the decimal value of bignum N in base B 
def Bto10(N, B):
    return sum(digit * B**i for i, digit in enumerate(N))
def get_Ke(B):
    global q_B
        #get ke
    q_bin = bin(Bto10(q_B, B)) # convert q to base 10 then to binary
    length = len(q_bin) - 2 # get the binary number length and remove the starting 0b
    l = rand.randint(0, length) #get a random value between 1 and length 0 < ke < q
    eph_key = ""  #initialize an empty string
    for _ in range(l):  # for l random times
        eph_key += str(rand.randint(0,1))  # generate a random bit
    eph_key = bitstoB(eph_key ,B)  # convert the bits string to a bignum in base B
    return eph_key
def ECDSA(privkey, hash, B):

    privkey = hextoB(privkey, B) #convert private key to base B
    hash_B = hextoB(hash,B)       #convert hash to base B
    
    gcd = 0  #initialize gcd variable
    comp = 0  #initialize comp variable
    eph_key = [0,1]
    while gcd != [1] or comp!= -1: #KE< q and gcd(Ke,q) = 1 
        eph_key = get_Ke(B) #get the gcd(ke,q) and value of Ke
        eph_key = normalize(eph_key, B) # normalize the resulting Ke           #normalize(N, B)
        if any(val != 0 for val in eph_key): # ensure the eph_key !=[0]
            gcd,_,_,_,_= EEA(eph_key, q_B, B)  # compute the gcd(ke,q)         #EEA(M, N, B)
            comp = compare(eph_key, q_B) #compare Ke and q                     #compare(M, N)
    eph_key_inverse = modinv(eph_key,q_B,B) #compute ke^(-1)                   #modinv(M,P,B)

    R = scalarMultiply(G, eph_key, c_B, B)  # R = kE* G                       #double_addECbig(A, k, c, Base)
    r = R[0] #extract xr

    product = multiply(privkey, r,B)   # d * r                                 #multiply(M, N, B)
    addition = add(product, hash_B , B)  # h(x)+ d*r                              #add(M, N, B)
    s = multiply(addition, eph_key_inverse,B) # (h(x)+ d*r)*Ke^(-1)            #multiply(M, N, B)
    s = reduce (s, q_B, B)  # (h(x)+ d*r)*Ke^-1 mod q                          #reduce(M,P,B)
    
    return from16tohex(convert(r,B,16)),from16tohex(convert(s,B,16))

def convertParams(param, B):#from hexa to base B
    if len(param)>1 and param[0] == '0' and param[1]=='x':      #remove the starting 0x
        param = param[2:]
        
    param_B = hextoB(param,B) #convert the parameter to our base B
    return param_B


#given parameters 
    #input as strings
p = '0xDB7C2ABF62E35E668076BEAD208B'
a = '0xDB7C2ABF62E35E668076BEAD2088'
b = '0x659EF8BA043916EEDE8911702B22'
Gx = '0x9487239995A5EE76B55F9C2F098'
Gy = '0xA89CE5AF8724C0A23E0E0FF77500'
q = '0xDB7C2ABF62E35E7628DFAC6561C5'
    #Hash
hash = 'ABD48D239E35FAE3'


# convert params to the base

B = 5
p_B = convertParams(p, B)
Gx_B = convertParams(Gx, B)
Gy_B = convertParams(Gy, B)
a_B = convertParams(a, B)
b_B = convertParams(b, B)
q_B = convertParams(q, B)
G = [Gx_B,Gy_B]  #generator coordinates
c_B = [p_B,a_B, b_B] #curve parameters c =[p,a,b]

d = get_privkey(snum) #get private key


r,s = ECDSA(d, hash, B)  #call ECDSA signing function  

print(r,s) #print the result


