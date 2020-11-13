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

    
def text_from_bits(bits):
    n = int(''.join(map(str, bits)), 2)
    return (n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()[2:])[:-2]

def evaluateBrute(file: str, skey: int):
    """ Evaluate the required time to perform a bruteforce
    attack on a given file encoded with dss"""



def writeBinaryWmkFile(wmk, outputFile):
    """
    Writes the binary content of a wmk to a file
    """
    fileName = outputFile+".wmk"
    f = open(fileName, "wb+")
    f.write(wmk)
    f.close()
    print("Watermark written in "+fileName)


def compareFiles(inputFileA, inputFileB):
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

    while (cA and cB):  
        print(hex(int.from_bytes(cA, "little")))
        print(hex(int.from_bytes(cB, "little")))
        difference = (int.from_bytes(cA, "little") - int.from_bytes(cB, "little")) % 256
        print(str(difference))
        if(cA != cB):
            diff += 1
        total += 1
        
        cA = fileA.read(1)
        cB = fileB.read(1)

    print(total)
    return ((total-diff)*100/total)


def decodeKeyFile(keyFile):
    """
    Converting the key into bit mapping
    """
    key = []
    rawKey = open(keyFile, "r").readlines()[0]
    for i in range(0, len(rawKey)-1):
        key = key + [int(rawKey[i])]

    return key
