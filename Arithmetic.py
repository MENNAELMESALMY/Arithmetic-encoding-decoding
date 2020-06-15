import cv2
import numpy as np
pathname = input("Input the image directory: ")

#:width
n = int(input("Image Width: "))

#:height
m = int(input("Image Height: "))

# Read the image in GRAYSCALE
imgbefore = cv2.imread(pathname, 0)
#
# # # Flaten the image to 1d array
#
flattened = imgbefore.flatten()

slidingWindow = int(input("Siding window : "))
lookAhead = int(input("lookAhead : "))

# search buffer pointer0
sPointer = 0
# Look Ahead pointer
lPointer = 1
matchfor = 1


encodedArr = [0, flattened[0]]

def findMatch(sp,lp,match,start,tempstart,maxmatch,MatchFlag):
    if sp >= lp or lp == len(flattened) or sp == len(flattened):
        j = 1
        if(maxmatch==0):
            encodedArr.append(0)
            if lp == len(flattened):
                encodedArr.append(flattened[lp-1])
            else:
                encodedArr.append(flattened[lp])
        else:
            j = maxmatch+1
            encodedArr.append(matchfor - start)
            encodedArr.append(maxmatch)
            if lp+j < len(flattened):
                encodedArr.append(flattened[lp + j -1])
            else:
                encodedArr.append(flattened[len(flattened) - 1])
        return (j)
    if flattened[sp] == flattened[lp]:
        if not MatchFlag:
            MatchFlag = True
            tempstart = sp
            if start == 0:
                start = tempstart
        return findMatch(sp + 1, lp+1, match + 1,start,tempstart, maxmatch,MatchFlag)
    else:
        if MatchFlag:
            MatchFlag = False
            lp = lp - match
            if match >= maxmatch:
                maxmatch = match
                start = tempstart
                match = 0
        return findMatch(sp + 1, lp,match, start,tempstart, maxmatch,MatchFlag)


while lPointer <= len(flattened)-1:
    jump = 0
    matchfor = lPointer
    #lookAhead is equivelent to GoBack
    #first zero is the match len ,the second is the max match len
    (jump) = findMatch(sPointer, lPointer, 0, 0, 0, 0, False)
    lPointer += int(jump)
    if lPointer >= (slidingWindow - lookAhead):
        sPointer = lPointer - (slidingWindow - lookAhead)
    if lPointer >= len(flattened):
        break

if(slidingWindow <256):
    encoded = np.array(encodedArr, dtype= np.uint8)
    np.save("encoded",encoded)
else:
    jumpMatch=[]
    symbol=[]
    i = 0
    while i<len(encodedArr):
        if(encodedArr[i]==0):
            jumpMatch.append(0)
            symbol.append(encodedArr[i+1])
            i += 2
        else:
            jumpMatch.append(encodedArr[i])
            jumpMatch.append(encodedArr[i + 1])
            symbol.append(encodedArr[i + 2])
            i+=3
    jumpMatch = np.array(jumpMatch, dtype=np.uint16)
    np.save("jumpMatch", jumpMatch)
    symbol = np.array(symbol, dtype=np.uint8)
    np.save("symbol", symbol)

#begining of decoding algorithm
curpos = 2
decodedcount = 1

decodedArr =[encodedArr[1]]
while curpos < len(encodedArr):
    if encodedArr[curpos] == 0:
        decodedArr.append(encodedArr[curpos + 1])
        decodedcount += 1
        curpos += 2
    else:
        lenMatched = 0
        endMatch = encodedArr[curpos + 1]
        itr = decodedcount - encodedArr[curpos]
        curpos += 3
        while lenMatched < endMatch:
            decodedArr.append(decodedArr[itr])
            lenMatched += 1
            decodedcount += 1
            itr += 1
        decodedArr.append(encodedArr[curpos-1])
        decodedcount += 1


decodedArr = np.array(decodedArr, dtype=np.uint8).reshape(m, n)

cv2.imshow('imgbefore', imgbefore)
cv2.imshow('imageafter', decodedArr)
# # user presses a key
cv2.waitKey(0)
# Destroying present windows on screen
cv2.destroyAllWindows()

