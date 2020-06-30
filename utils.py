
def wmkToBin(wmkFile: str, sound):
    """
    Transforms watermark input file into binary stream
    """
    watermark_bin = ''
    wmk_bytes = bytearray(str(open(wmkFile, "r").readlines()), encoding='utf-8')

    for i in range(0, sound.getnframes()):
        for j in range(0, 8):
            # The watermark is repeated all along to avoid snipping attack
            wmk_bit = wmk_bytes[i % len(wmk_bytes)]

            # Logical and to determine the bit value
            watermark_bin += '1' if ((wmk_bit << j) & 128) > 0 else '0'
    # Padding
    watermark_bin += '00000000'

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