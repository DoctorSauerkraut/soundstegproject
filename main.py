"""
Applying random mapping LSB on a wav file
For regular LSB : put '0' in the key file
"""

import sys 
import time
import wave

from pysndfx import AudioEffectsChain

from utils import compareFiles, decodeKeyFile
from lsb import lsb_apply, lsb_read, getnframes, lsb_decode
from spreadspectrum import dss_apply, dss_read


#
if __name__ == "__main__":
    startTime = time.time_ns()

    action = sys.argv[1]
    algo = sys.argv[2]
    fileName = sys.argv[3]
  
    if(action == 'r'):
        print("---- READING WITH "+algo+" ----")
        wmk = ""
        if(algo == "DSS"):
            wmk = dss_read(fileName, 42, 4136)
        elif(algo == "LSB"):
            keyFile = sys.argv[4]
            key = decodeKeyFile(keyFile)
            wmk = lsb_read(fileName, key, 0, True)
        # print(wmk)

    elif(action == 'w'):
        print("---- WRITING WITH "+algo+" ----")
        wmkFile = sys.argv[4]
        if(algo == "DSS"):
            a = dss_apply(fileName, wmkFile, 42, 4096)
        elif(algo == "LSB"):
            keyFile = sys.argv[5]
            key = decodeKeyFile(keyFile)
            lsb_apply(fileName, wmkFile, key)

    elif(action == 'a'):
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

    elif(action == 'cmp'):
        fileNameB = sys.argv[3]
        print("Comparing ratio :"+str(compareFiles(fileName, fileNameB)))

    elif(action == 'e'):
        charsize = 1000
        print("--- EVALUATING REQUIRED TIME TO BRUTEFORCE "+str(charsize)+" CHARACTERS FOR ALGO "+algo+" ----")
        if(algo == "DSS"):
            i = charsize * 8 
            evalTimeStart = time.time_ns()
            try:
                dss_read(fileName, 42, i)
            except UnicodeDecodeError:
                print("Unicode Error")

            evalTimeEnd = time.time_ns()
            evalTimeDelta = evalTimeEnd - evalTimeStart
            estimatedTime = (evalTimeDelta * i)/1000000000

            strETime = str(estimatedTime)

        elif(algo == "LSB"):
            keyFile = sys.argv[4]
            key = decodeKeyFile(keyFile)
            
            fileInput = fileName + '.wav'
            sound = wave.open(fileInput, 'r')  # lecture d'un fichier audio
            sound.setpos(0)
            print("Opening "+fileInput)

            for i in range(0, 10):
                evalTimeStart = time.time_ns()
                # Decoding 1 bit
                watermark = lsb_decode(1, sound, key)
                evalTimeEnd = time.time_ns()

            print("Key length:"+str(len(key)))
            print("Key maximal bit:"+str(max(key)))
            evalTimeDelta = (evalTimeEnd - evalTimeStart)/10
            evalTimeDelta = evalTimeDelta*(4**(len(key)*max(key)))/1000000000
            
            strETime = str(evalTimeDelta)

        print("Estimated required time : "+strETime+" seconds")    
        
    print("---- DONE ----")
    endTime = time.time_ns()
    delta = (endTime - startTime)/1000000000

    print("Done in "+str(delta)+" s")