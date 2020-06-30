
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
            # Nous faisons un & binaire entre le MSB et "128" pour savoir si nous écrivons un 1 ou 0
            # (Decalage de j pour s'occuper de chaque bit de l'octet)
            watermark_bin += '1' if ((i << j) & 128) > 0 else '0'

    print("Binary Watermark: " + watermark_bin)

    return watermark_bin


def compareFiles(inputFileA, inputFileB):
    """
    Generical file comparison
    Used to compare the number of common bits between two watermarks
    """
    fileA = open(inputFileA, "r")
    fileB = open(inputFileB, "r")

    diff = 0
    total = 0

    while 1:
        cA = fileA.read(1)
        cB = fileB.read(1)

        if(cA != cB):
            diff += 1
        total += 1

        if(cA == '' or cB == ''):
            break

    return (diff*100/total)


def decodeKeyFile(keyFile):
    """
    Converting the key into bit mapping
    """
    key = []
    rawKey = open(keyFile, "r").readlines()[0]
    for i in range(0, len(rawKey)-1):
        key = key + [int(rawKey[i])]

    return key