from elboutahiri_P13 import*

snum = '153071423'
r1, c1 = ECDSA(snum, '1234567890abcdef', 32)
r2, c2 = ECDSA(snum, '1234567890abcdef', 32)

print(r1,c1)
print(r2,c2)