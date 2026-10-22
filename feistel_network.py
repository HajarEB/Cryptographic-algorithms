def fromletterstoNumbers(words):
    letters=[]
    for i in words:
        if  'a'<= i<= 'z' or 'A'<= i <= 'Z':
            i = i.upper()
            letters.append(i)
    return [ord(x) - 65 for x in letters] 


def toLetters(Nums):
    letters=[]
    for i in Nums:
        letters.append(chr(i+65))
    return letters
            

def processWord(plainTList, index, resultKey, mult):
    ROUNDS = 16
    result= []
    leftHalfWord = plainTList[index:index+8] 
    rightHalfWord =  plainTList[index+8:index+16]
    for round in range(ROUNDS):
        print("\nInput to Round: ",round)
        print(''.join(toLetters(leftHalfWord)),''.join(toLetters(rightHalfWord)) )
        keyRound =[]
        for row in resultKey:       # get the keyround 
            keyRound.append(row[round%4])
        val =[]
        newLeftHalfWord = rightHalfWord
        for i in range(len(leftHalfWord)):
            index = (mult[round]*rightHalfWord[i] + keyRound[i])%26
            val.append((leftHalfWord[i]+ index)%26)
        newRightHalfWord = val
        leftHalfWord =  newLeftHalfWord
        rightHalfWord = newRightHalfWord 
    result.extend(rightHalfWord) #final round we don't swap
    result.extend(leftHalfWord)
    listLetters = toLetters(result)
    return ''.join(listLetters)
      
      
def hexToDecimal(val):
    return [int(i, 16) for i in val] 


def hexaToBinary(hexa):
    hxarray=[]
    l=[]
    for i in hexa:
        binString = bin(int(i, 16))[2:].zfill(4)
        hxarray.append([int(elmt) for elmt in binString])
    return hxarray


def matrixMult(matrixA, matrixB):
    result = [[sum(a * b for a, b in zip(A_row, B_col)) %26
                        for B_col in zip(*matrixB)]
                                for A_row in matrixA]
    return result


if __name__=='__main__':
    personalBit = "5647a87b98e6005eb23d7a39"
    key = "KEYSAREESSENTIAL" 
    numlist = fromletterstoNumbers(key)
    matrix4by4 =  [numlist[i:i+4] for i in range(0, 16, 4)] 
    matrix8by4 = hexaToBinary(personalBit[16:16+8]) 
    scheduleKey = matrixMult(matrix8by4, matrix4by4)
    plainText = "ITISNOTTOOTRICKY" 
    plainTList = fromletterstoNumbers(plainText)
    while len(plainTList)%16 != 0:
        plainTList =  plainTList + [0]  
    decimals = hexToDecimal(personalBit[:16])  
    mult = [i+1 for i in decimals]   
    for i in range(0,len(plainTList), 16):
        res = processWord(plainTList, i, scheduleKey, mult)
    
    print("\n **************** Encryption Results ****************")
    print(f"\nPlaintext: {plainText}")
    print(f"\nKey: {key}")
    print(f"\nCiphertext: {res}")

 
            
