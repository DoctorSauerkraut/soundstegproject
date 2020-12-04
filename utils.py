import hashlib
import sys

def wmkToBin(wmkFile: str, sound):
    """
    Transforms watermark input file into binary stream
    """
    watermark_bin = ''
    wmkStream = open(wmkFile, "r")
    wmk_bytes = bytearray(str(wmkStream.readlines()), encoding='utf-8')

    watermark_bin = ''
    for i in wmk_bytes:
        for j in range(0, 8):
            # Nous faisons un & binaire entre le MSB et "128" pour savoir si
            #  nous écrivons un 1 ou 0
            # (Decalage de j pour s'occuper de chaque bit de l'octet)
            watermark_bin += '1' if ((i << j) & 128) > 0 else '0'

    return watermark_bin

    
def bytes_from_bits(bits):    
    n = int(''.join(map(str, bits)), 2)
    return (n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()[2:])[:-2]

def evaluateBrute(file: str, skey: int):
    """ Evaluate the required time to perform a bruteforce
    attack on a given file encoded with dss"""

def getSize(fileobject):
    fileobject.seek(0,2) # move the cursor to the end of the file
    size = fileobject.tell()
    return size

def writeBinaryWmkFile(wmk, outputFile):
    """
    Writes the binary content of a wmk to a file
    """
    fileName = outputFile+".wmk"
    f = open(fileName, "wb+")
    f.write(wmk)
    f.close()
    print("\nWatermark written in "+fileName)


def compareFiles(inputFileA, inputFileB):
    print("Comparing "+inputFileA+" and "+inputFileB)
    sha1a = hashlib.sha1()
    sha1b = hashlib.sha1()

    """
    Generical file comparison
    Used to compare the number of common bits between two watermarks
    """
    fileA = open(inputFileA, "rb")
    fileB = open(inputFileB, "rb")

    diff = 0
    total = 0
    cA = fileA.read(1)
    cB = fileB.read(1)

    # Difference by number of bits
    bitdiff = 0
    # Total number of bytes
    byteTot = 1
    # Total weight
    weightTot = 1
    # Difference by weight of bits
    weightDiff = 0

    while (cA and cB):
        byteTot = byteTot + 1
        weightTot = weightTot + 511  # Max weight on 8 bits
        nbDiff = numberofBitsDiff(cA, cB)
        bitdiff = bitdiff + nbDiff[0]
        weightDiff = weightDiff + nbDiff[1]

        cA = fileA.read(1)
        cB = fileB.read(1)
        sha1a.update(cA)
        sha1b.update(cB)

    ratio = bitdiff * 100 / (byteTot*8)
    ratioWght = weightDiff * 100 / weightTot

    print(str(ratio)+" % bits difference ratio")
    print(str(ratioWght)+" % weighted difference ratio")
    print("SHA1 input file:\t"+str(sha1a.hexdigest()))
    print("SHA1 output file:\t"+str(sha1b.hexdigest()))

    return ratio

def numberofBitsDiff(byteA, byteB):
    """
    Returns the number of different bits between two bytes
    """
    bitdiff = 0
    weightDiff = 0

    difference = (int.from_bytes(byteA, "little") - int.from_bytes(byteB, "little")) % 256

    if (difference != 0):
        for i in range(8,-1,-1):
            if (difference >= 2**i):
                difference = difference - 2**i
                bitdiff = bitdiff + 1
                weightDiff = weightDiff + (2**i)

    return (bitdiff, weightDiff)


def decodeKeyFile(keyFile):
    """
    Converting the key into bit mapping
    """
    key = []
    rawKey = open(keyFile, "r").readlines()[0]
    for i in range(0, len(rawKey)-1):
        key = key + [int(rawKey[i])]

    return key

def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()
