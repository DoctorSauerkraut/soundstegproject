#!/usr/bin/env python3
# TODO : Solving diff problems

import time
import wave
import argparse
import os

from utils import compareFiles, decodeKeyFile
from lsb import lsb_apply, lsb_read, getnframes, lsb_decode
from spreadspectrum import dss_apply, dss_read


def apply_tag(algo: str, fileName, wmkFile, keyFile=None):
    sound = wave.open(fileName + '.wav', 'r')  # lecture d'un fichier audio
    outputFile = fileName + "_watermarked_"+algo+".wav"
    print("---- WRITING WITH "+algo+" ----")
    print("Input file:\t\t"+fileName+".wav")
    print("Output file:\t"+outputFile)    
    print("Watermark file:\t"+wmkFile)
    
    if(algo == "DSS"):
        a = dss_apply(fileName, wmkFile, 42, outputFile, sound, 500)
    elif(algo == "LSB"):
        if(keyFile is None):
            key = "0"
        key = decodeKeyFile(keyFile)
        lsb_apply(fileName, wmkFile, key, False, outputFile, sound)
    else:
        print("No algo specified or algorithm not recognized")
        return


def read_tag(algo, fileName, keyFile=None):
    if(algo == "DSS"):
        wmk = dss_read(fileName, 42, 4136)
    elif(algo == "LSB"):
        if(keyFile is None):
            print("Please specify keyfile with -k")
            return
        key = decodeKeyFile(keyFile)
        wmk = lsb_read(fileName, key, 0)

    return wmk

def attack_signal(inputFile, outputFile):
    """
    Applies a specific effect on a music file
    :param inputFile : file to apply effect on
    :param outputFile : modified file
    """
    print("---- Attacking signal with echo effect ----")
    print("Input file:\t\t"+inputFile)
    print("Output file:\t"+outputFile)

    atk = "echo 0.1 0.1 1 0.1"

    cmd = "sox "+inputFile+" "+outputFile+" "+atk
    os.system(cmd)


# Entry point
def main():
    startTime = time.time_ns()
    parser = argparse.ArgumentParser()
    parser.add_argument("action", help="write mode(w), read mode(r), compare mode(cmp)")
    parser.add_argument("-i", "--input", help="Input sound file to tag")
    parser.add_argument("-w", "--watermark", help="Text file containing the tag message")
    parser.add_argument("-a", "--algo", help="Stegano algorithm to use")
    parser.add_argument("-k", "--key", help="Keyfile (for LSB)")
    parser.add_argument("-fa", "--filea", help="First file to compare (cmp mode)")
    parser.add_argument("-fb", "--fileb", help="Second file to compare (cmp mode)")
    args = parser.parse_args()

    action = args.action
    algo = args.algo

    if(action == 'r'):
        if(not args.algo):
            print("Please specify algorithm to use with -a")
            return 
        if(not args.input):
            print("Please specify input file raw name with -i")
            return
        print("---- READING WITH "+algo+" ----")
        wmk = ""
        if(args.key):
            read_tag(args.algo, args.input, args.key)
        else:
            read_tag(args.algo, args.input)

    elif(action == 'w'):
        if(not args.algo):
            print("Please specify algorithm to use with -a")
            return 
        if(not args.watermark):
            print("Please specify watermark file with -w")
            return 
        if(not args.input):
            print("Please specify input file raw name with -i")
            return
        else:    
            if (args.key):
                apply_tag(args.algo, args.input, args.watermark, args.key)   
            else:
                apply_tag(args.algo, args.input, args.watermark)

    elif(action == 'cmp'):
        if(not args.file or not args.fileb):
            print("Please specify files to compare with --fa and --fb")
            return 
        compareFiles(args.filea, args.fileb)
    elif(action == 'atk'):
        if(not args.input):
            print("Please specify input file raw name with -i")
            return
        inputFile = args.input + '.wav'
        outputFile = args.input + "_atk_echo.wav"

        attack_signal(inputFile, outputFile)

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
            if(not args.key):
                print("Please specify keyfile with -k")
                return
            key = decodeKeyFile(keyFile)
            
            fileInput = fileName + '.wav'

            # Input audio file reading
            sound = wave.open(fileInput, 'r')  
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

if __name__=="__main__":
    main()