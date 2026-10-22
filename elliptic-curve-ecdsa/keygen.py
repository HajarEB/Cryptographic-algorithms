from bignum import*

p = 'DB7C2ABF62E35E668076BEAD208B'
a = 'DB7C2ABF62E35E668076BEAD2088'
b = '659EF8BA043916EEDE8911702B22'
Gx = '9487239995A5EE76B55F9C2F098'
Gy = 'A89CE5AF8724C0A23E0E0FF77500'
q = 'DB7C2ABF62E35E7628DFAC6561C5'



def hexto16(N):
    return [int(h,16) for h in N[::-1]] # reverse order of the argument string

# A bignum N in base 16 into a string of hexadecimals
def from16tohex(N):
    return ''.join([hex(i)[2].upper() for i in N[::-1]])


def get_pub_key(prvkey): #get public key from the private key
    Gx_16 = hexto16(Gx)
    Gy_16 = hexto16(Gy)
    p_16 = hexto16(p)
    a_16 = hexto16(a)
    b_16 = hexto16(b)
    d = hexto16(prvkey)
    G = [Gx_16,Gy_16]
    c_16 = [p_16,a_16, b_16]
    A =  double_addECbig(G,d, c_16, 16)   
    pubkey = [from16tohex(A[0]), from16tohex(A[1])] #public key
    return pubkey

