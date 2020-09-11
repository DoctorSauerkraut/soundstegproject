"""
Applying random mapping LSB on a wav file
For regular LSB : put '0' in the key file
"""

import sys
from pysndfx import AudioEffectsChain

from utils import compareFiles, decodeKeyFile
from lsb import lsb_apply, lsb_read
from spreadspectrum import dss_apply, dss_read


if __name__ == "__main__":
    action = sys.argv[1]
    fileName = sys.argv[2]
    print("Opening "+fileName)

    if(action == 'lw' or action == 'lr'):
        if(action == 'lw'):
            print("---- WRITING WITH DSS----")
            wmkFile = sys.argv[3]
            a = dss_apply(fileName, wmkFile, 42, 4096)
            b = dss_read(fileName+"_watermarked_dss", 42, len(a))
            error = 0
            for i in range(0, min(len(a), len(b))):
                if b[i] != a[i]:
                    error += 1
            error /= min(len(a), len(b))
            print('Error rate: ', error)

        if(action == 'lr'):
            print("---- READING WITH DSS----")
            wmk = dss_read(fileName, 42, 7*8)
            print(wmk)

    if(action == 'w' or action == 'r'):
        keyFile = sys.argv[3]
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
            .reverb()
            .delay()
            .phaser()
            .delay()
        )
        outfile = fileName + "_del.wav"

        # Apply effect
        fx(fileName + ".wav", outfile)

    if(action == 'cmp'):
        fileNameB = sys.argv[3]
        print("Comparing ratio :"+str(compareFiles(fileName, fileNameB)))
