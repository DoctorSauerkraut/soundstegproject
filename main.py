"""
Applying random mapping LSB on a wav file
For regular LSB : put '0' in the key file
"""

import wave
import sys, getopt
from lsb import lsb_apply, lsb_read
from pysndfx import AudioEffectsChain


def decodeKeyFile(keyFile):
    """
    Converting the key into bit mapping
    """
    key = []
    rawKey = open(keyFile, "r").readlines()[0]
    for i in range(0, len(rawKey)-1):
        key = key + [int(rawKey[i])]

    return key


if __name__ == "__main__":
    action = sys.argv[1]
    fileName = sys.argv[2]
    keyFile = sys.argv[3]
    print("Opening "+fileName)

    if(action == 'w' or action == 'r'):
        key = decodeKeyFile(keyFile)
        if(action == 'w'):
            print("---- WRITING ----")
            wmkFile = sys.argv[4]
            lsb_apply(fileName, wmkFile, key)

        if(action == 'r'):
            print("---- READING ----")
            wmk = lsb_read(fileName, key, True)
            print(wmk)

    if(action == 'a'):
        print("--- ATTACKING ----")
        fx = (
            AudioEffectsChain()
            .delay()
        )
        outfile = fileName + "_mod.wav"

        # Apply effects
        fx(fileName + ".wav", outfile)
