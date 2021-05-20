import array
from BUFRConstants import *

def packLength(lengthToPack):

    MAX_SIZE = 2**23 - 1

    lengthString = array.array('B', 3*[0])

    if lengthToPack <= MAX_SIZE:
        lengthString[0] = lengthToPack >> 16
        lengthString[1] = (lengthToPack >> 8) % MAX_BYTE
        lengthString[2] = lengthToPack % MAX_BYTE

    return lengthString

def splitBytes(shortInt):

    twoBytes = array.array('B', 2*[0])

    if shortInt <= MAX_BYTE*MAX_BYTE:
        twoBytes[0] = shortInt//MAX_BYTE
        twoBytes[1] = shortInt % MAX_BYTE

    return twoBytes

def string2ByteArray(string):

    byteArray = array.array('B')
    for i in range(len(string)):
        byteArray.append(ord(string[i]))

    return byteArray

def byteArray2String(byteArray):

    string = ''
    for i in byteArray:
        string += chr(i)

    return string

def shortArray2String(shortArray):

    string = ''
    for i in shortArray:
        string += chr(i >> 8) + chr(i % MAX_BYTE)
    
    return string
