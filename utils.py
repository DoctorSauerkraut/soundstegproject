import sys
import time
import threading

from dbgprint import *

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
    s = bytes(int(bits[i : i + 8], 2) for i in range(0, len(bits), 8))
    return s
    #n = int(''.join(map(str, bits)), 2)
    #return (n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()[2:])[:-2]



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
    dprint("Watermark written in "+fileName, VER)


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
    if(keyFile == None):
        return [0]
    key = []
    rawKey = open(keyFile, "r").readlines()[0]
    for i in range(0, len(rawKey)-1):
        key = key + [int(rawKey[i])]

    return key


class Progress(threading.Thread):
    """
    Progress bar management thread
    """

    chronoStart = 0
    chronoEnd = 0
    bar_len = 60
    task = ""
    count = 0
    total = 0
    isrunning = True
    suffix = ''

    def __init__(self, task):
        threading.Thread.__init__(self)
        self.chronoStart = 0
        self.chronoEnd = 0
        self.task = task
        self.count = 0
        self.total = 0
        self.isrunning = True
        self.start()

    def run(self):
        while(self.isrunning is True):
            while(self.count != self.total or self.total != 0):
                filled_len = int(round(self.bar_len * self.count / float(self.total)))

                percents = round(100.0 * self.count / float(self.total), 1)
                bar = '#' * filled_len + '-' * (self.bar_len - filled_len)

                if(self.chronoStart != 0 and self.chronoEnd != 0):
                    delta = int((self.chronoEnd - self.chronoStart)/10000000)/100
                    self.chronoEnd = 0
                    self.chronoStart = 0
                    sys.stdout.write(str(self.task)+":\t"+'[%s] %s%s ...%s Done in %s secs\n' % (bar, percents, '%', self.suffix, delta))
                    self.isrunning = False
                    break
                else:
                    sys.stdout.write(str(self.task)+":\t"+'[%s] %s%s ...%s\r' % (bar, percents, '%', self.suffix))
                    sys.stdout.flush()
                time.sleep(0.1)

    def progress(self, count, total, suffix=''):
        if(count == 0):
            self.chronoStart = time.time_ns()
            self.chronoEnd = 0
            
        if(count == total):
            self.chronoEnd = time.time_ns()
        
        self.count = count
        self.total = total
        self.suffix = suffix

       
