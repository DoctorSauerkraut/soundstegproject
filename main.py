#!/usr/bin/env python3
# TODO : Solving diff problems

import time
import wave
import argparse
import os

from diff import *
from utils import *
from lsb import lsb_apply, lsb_read, getnframes, lsb_decode
from spreadspectrum import dss_apply, dss_read
from echohiding import *

def apply_tag(algo: str, fileName, wmkFile, keyFile=None):
    sound = wave.open(fileName + '.wav', 'r')  # lecture d'un fichier audio

    path = fileName[0:fileName.rfind("/")+1]
    dprint(path, DBG)
    fileraw = fileName[fileName.rfind("/")+1:]
    dprint(fileraw, DBG)

    outputFile = path + "output/" + fileraw + "_watermarked_"+algo+".wav"
    dprint("---- WRITING WITH "+algo+" ----", VER)
    dprint("Input file:\t"+fileName+".wav", VER)
    dprint("Output file:\t"+outputFile, VER)    
    dprint("Watermark file:\t"+wmkFile, VER)
    
    if(algo == "DSS"):
        a = dss_apply(fileName, wmkFile, 42, outputFile, sound, 500)
    elif(algo == "LSB"):
        if(keyFile is None):
            key = [0]
        else:
            key = decodeKeyFile(keyFile)
        lsb_apply(fileName, wmkFile, key, False, outputFile, sound)
    elif(algo == "ECHO"):
        echo_single_apply(fileName, wmkFile, outputFile, 0.1, 128, 256, 1024, False)
    else:
        dprint("No algo specified or algorithm not recognized", ERR)
        return


def read_tag(algo, fileName, keyFile=None):
    dprint("---- READING WITH "+algo+" ----", VER)

    if(algo == "DSS"):
        wmk = dss_read(fileName, 42, 4136)
    elif(algo == "LSB"):
        if(keyFile is None):
            dprint("No key specified, running LSB basic mode", VER)
        key = decodeKeyFile(keyFile)
        wmk = lsb_read(fileName, key, 0)
    elif(algo=="ECHO"):
        wmk = echo_decode(fileName, 128, 256, 1024)
    return wmk

def attack_signal(inputFile, outputFile, atkType):
    """
    Applies a specific effect on a music file
    :param inputFile : file to apply effect on
    :param outputFile : modified file
    """
    attackList = ["trim"]
    if(atkType not in attackList):
        dprint("Unknown attack. Please choose among these available attacks:"+str(attackList), ERR)
        return

    dprint("---- Attacking signal with "+str(atkType)+ " ----", VER)
    dprint("Input file:\t"+inputFile, VER)
    dprint("Output file:\t"+outputFile, VER)

    #atk = "echo 0.1 0.1 1 0.1"
    if(atkType == "trim"):
        dprint("Trimming 3:00", VER)
        atk = "trim 0 3:00"
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
    parser.add_argument("-t", "--type", help="Attack type (atk mode)")
    args = parser.parse_args()

    action = args.action
    algo = args.algo

    if(action == 'r'):
        if(not args.algo):
            dprint("Please specify algorithm to use with -a", ERR)
            return 
        if(not args.input):
            dprint("Please specify input file raw name with -i", ERR)
            return
        wmk = ""
        if(args.key):
            read_tag(args.algo, args.input, args.key)
        else:
            read_tag(args.algo, args.input)

    elif(action == 'w'):
        if(not args.algo):
            dprint("Please specify algorithm to use with -a", ERR)
            return 
        if(not args.watermark):
            dprint("Please specify watermark file with -w", ERR)
            return 
        if(not args.input):
            dprint("Please specify input file raw name with -i", ERR)
            return
        else:    
            if (args.key):
                apply_tag(args.algo, args.input, args.watermark, args.key)   
            else:
                apply_tag(args.algo, args.input, args.watermark)

    elif(action == 'cmp'):
        if(not args.filea or not args.fileb):
            errprint("Please specify files to compare with --fa and --fb")
            return 

        rate = compareFiles(args.filea, args.fileb)
        logResult(str(rate)+"\t")

    elif(action == 'atk'):
        if(not args.input):
            errprint("Please specify input file raw name with -i")
            return
        if(not args.type):
            errprint("Please specify an attack type with -t")
            return
        inputFile = args.input + '.wav'
        outputFile = args.input + "_atk.wav"

        attack_signal(inputFile, outputFile, args.type)
    
    elif(action == 'brute'):
        charsize = 1000
        dprint("--- EVALUATING REQUIRED TIME TO BRUTEFORCE "+str(charsize)+" CHARACTERS FOR ALGO "+algo+" ----", VER)
        if(algo == "DSS"):
            i = charsize * 8 
            evalTimeStart = time.time_ns()
            try:
                dss_read(fileName, 42, i)
            except UnicodeDecodeError:
                errprint("Unicode Error")

            evalTimeEnd = time.time_ns()
            evalTimeDelta = evalTimeEnd - evalTimeStart
            estimatedTime = (evalTimeDelta * i)/1000000000

            strETime = str(estimatedTime)

        elif(algo == "LSB"):
            if(not args.key):
                errprint("Please specify keyfile with -k")
                return
            key = decodeKeyFile(keyFile)
            
            fileInput = fileName + '.wav'

            # Input audio file reading
            sound = wave.open(fileInput, 'r')  
            sound.setpos(0)
            dprint("Opening "+fileInput, VER)

            for i in range(0, 10):
                evalTimeStart = time.time_ns()
                # Decoding 1 bit
                watermark = lsb_decode(1, sound, key)
                evalTimeEnd = time.time_ns()

            dprint("Key length:"+str(len(key)), VER)
            dprint("Key maximal bit:"+str(max(key)), VER)
            evalTimeDelta = (evalTimeEnd - evalTimeStart)/10
            evalTimeDelta = evalTimeDelta*(4**(len(key)*max(key)))/1000000000
            
            strETime = str(evalTimeDelta)

        dprint("Estimated required time : "+strETime+" seconds", NOR)    
        
    dprint("---- DONE ----", VER)
    endTime = time.time_ns()
    delta = (endTime - startTime)/1000000000

    dprint("Done in "+str(delta)+" s", VER)

if __name__=="__main__":
    main()