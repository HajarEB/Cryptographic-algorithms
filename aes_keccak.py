import os  #import os module for file handling

#generate a personalized sbox: P5
class generate_sbox:
    
    @staticmethod
    def showcycles(C):
        if len(C) != 256 or sorted(C) != list(range(256)):
            raise ValueError("Invalid S-box permutation")

        cycles = []
        visited = set()

        for i in range(256):
            if i not in visited:
                cycle = []
                current = i

                while current not in visited:
                    visited.add(current)
                    cycle.append(current)
                    current = C[current]

                cycles.append(cycle)

        cycles.sort(key=len)

        print("\nCycles, ordered by their length")
        for cycle in cycles:
            print([len(cycle), cycle])

        print("\nCycle lengths:")
        print([len(cycle) for cycle in cycles])
        
    @staticmethod
    def fixedPointCycle(c):
        count =0
        fixedList =[]
        for i in range(len(c)):
            if c[i] == i:
                count+=1
                fixedList.append(i)
        if count > 1:
            i=0
            size = len(fixedList)
            while i+1 <size: 
                x1 = fixedList[i]
                x2 = fixedList[i+1]
                c[x1]=x2
                i+=1
            x1 = fixedList[0]
            xk = fixedList[size-1]
            c[xk]= x1
        return c
        
    @staticmethod  
    def isPrime(num):
        if num<2:
            return False
        i= 2
        while i<num:
            if num% i==0:
                return False
            i+=1
        return True
    
    @staticmethod  
    def getPrime (num):
        while generate_sbox.isPrime(num) is False:
            num+=1
        return num

    @staticmethod
    def reorderNum(num):
        r2 = 0
        for i in range(len(str(num))):
            val = num%10
            r2 = r2 *10 +val
            num = num//10
        return r2

    @staticmethod
    def reorderList(l):
        return l[::-1]

    @classmethod
    def generate(cls, snum, show_cycles = False):
        
        snum = int(snum)
        
        #set p1 and p2
        p1 = snum%1000
        
        if p1<11:
            p1 = 11
        else: 
            p1 = (cls.getPrime(p1+1))
        p2 = (cls.getPrime(p1+1))
        p1= p1%256
        p2= p2%256

        # Set q
        q = snum%100000
        q = int(q/1000)
        q = q % 32 +2

        # set r1 and r2
        r1 = snum%10000
        r2= cls.reorderNum(r1)
        r1= r1 % 256
        r2 = r2 % 256

        # set a
        a = list(range(256))
        for i in range(len(a)):
            a[i] = (p1 * a[i] + r1) % 256
            
        # set b
        b=[]
        for i in range(0,len(a), q):
            b = b + cls.reorderList(a[i:i+q])
            
        # set c
        c = [0]*256
        for i in range(len(b)):
            pos = (p2* i + r2) %256
            c[pos] = b[i]

        c = cls.fixedPointCycle(c)
        
        if show_cycles:
            cls.showcycles(c)

        
        #return generated s-box
        return c



#shift Rows AES operation
def shiftRows(S,snum):
    snumRotation = snum[::-1][:4] #reverse snum order and extract the first 4 digits  
    for i in range(1,len(S)): #start looping from row 1, since no shift occurs in row 0 
        # determining the number of rotation steps
        steps = int(snumRotation[i-1]) %5  #get the number of steps 
        if steps == 0:  #if number of calculated steps is 0
            steps= 1    #do 1 rotation
        temp = S[i]     #use a temporary variable to store the current row
        S[i] = temp[steps:] + temp[:steps] #rotate S left with n steps
    return S
                
#Mix Columumns AES operation
def mixColumns(snum, S):
    
    if snum[0].isalpha():  #if first letter of student number is a letter, remove it
        snum = snum[1:]
    
    L= len(snum) #get length of snum
    
    matrix = [ [0]*5 for i in range(5)] #initialize a 5*5 matrix
    
    # fill matrix with student number digits
    index = 0
    for row in range(5): # loop over rows of S
        for col in range(5): #loop over S[row]
            if index == L: #all digits of snum have been copied 
                index = 0   # re initialize the index to 0 (to recopy the digits again)
            matrix[row][col] = int(snum[index])  #fill the matrix position with the adequate snum digit
            index+=1
            
    result = matrixMult(matrix, S) #perform matrix multiplication
    
    return result

#subBytes AES operation
def subBytes(S, snum):
    #get the S-box 
    s_box = generate_sbox.generate(snum)
    
    for row in range(len(S)): #loop over S rows
        for col in range(len(S[row])): #loop over S columns
            S[row][col] = s_box[S[row][col]] #ex: suppose S[1][1] = 2; assign to S[1]|1] the value at SBox[2] (S[1][1] = SBox[2])
    return S
    

#for matrix multiplication
def matrixMult(matrix, S):
    result =  [ [0]*5 for i in range(5)] #initialize a 5*5 matrix where we will be storing the multiplication result
    #multiplication logic
    for row in range(5):  #loop over rows of matrix
        for col in range(5): #loop over columns of S
            sum = 0     #initialize sum variable to 0
            for index in range (5): #loop over columns of matrix and rows of state
                sum += matrix[row][index] * S[index][col]  #perform multiplication and add result to the previously computed one
            result[row][col]= sum % 256   #to ensure the results are within the desired range, do a modulo 256 reduction
    return result

# fill the 2 first rows of the state matrix
def fillS(S, byte_integers):
    for i in range(0,10): # we want to fill 2 first rows: each row of size 5=> 5+5 = 10
        if i < 5: #i defines the column position we want to fill (each row has 5 positions (0,1,2,3,4))
            S[0][i] = ( S[0][i] + byte_integers[i] ) % 256  #fill row 1
        else: #i defines the column position we want to fill (ex: row 2 column 1 => i = 5 => i-5 = 0 , row =1 => so the 1st cell of row 2)
            S[1][i-5] = ( S[1][i-5] + byte_integers[i] ) % 256 #fill row 2
    return S 
    
#Perform AES Permutations
def AESpermutations(S,snum):
    for i in range(6): # AES-style personalized operations for 6 rounds
        S = subBytes(S, snum)
        S = shiftRows(S,snum)
        S = mixColumns(snum, S)
    return S

#squeez the output 
def squeezing(S,snum,outQ):
    if outQ < 0:
        raise ValueError("Output Length must be non-negative")
    out = []    # where to store the results 
    while len(out) < outQ:
        
        # Extract the 2 first rows of S
        for row in S[:2]:
            out.extend(row) 
        
        if len(out) < outQ:   
            S = AESpermutations(S,snum)  #do the 3 AES operations (subBytes, ShiftRows, MixColumns) for 6 rounds
    return bytearray(out[:outQ]).hex() #Truncation

def readFile(fileName, outQ):
    blockSize = 10  #define block size to be read at a time
    S =[ [0]*5 for i in range(5)]  #initialize the State matrix 5*5
    byte_integers = [0] * blockSize #initialize thz byte integers array
    with open(fileName, 'rb') as file:   #open file:  r=read b=binary
        while True:
            data = file.read(blockSize)   #read one block of size 10 at a time 
            #No more bytes to read
            if not data:
                break
            # Pad the last block of input with zeros so that the length = 10
            if len(data)!= blockSize :    #ensure blocksize
                padding = bytes([0]*(blockSize-len(data))) #perform padding: adding 0s
                data += padding  #update data 
            
            #convert bytes to integers
            for i in range(len(data)):
                byte_integers [i] = int(data[i])
                
            S = fillS(S, byte_integers) #fill the 2 first rows of the state matrix
            S = AESpermutations(S,snum)  #do the 3 AES operations (subBytes, ShiftRows, MixColumns) for 6 rounds
    #squeezing the output 
    res = squeezing(S,snum,outQ)
    return res

snum = "22222222222"    # define the student number

if __name__=='__main__': 
    #user Input
    fileName = input("\nPlease Enter the File Name\n")
    if not os.path.isfile(fileName):
        print("\n\t\t**************************************")
        print("\t\t\tError: File Not Found")
        print("\n\t\t**************************************\n")
        exit(1)
    try:
        outQ = int(input("Please Enter the Number of Desired Output Bytes\n"))
    except ValueError:
        print("\n\t\t***********************************************************************")
        print("\t\t\tError: Number of Desired Output Bytes Must be an INTEGER")
        print("\n\t\t***********************************************************************\n")
        exit(1)
        
    print('\n',readFile(fileName,outQ),'\n')
    

                
