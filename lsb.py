import wave
import time
from utils import *

masks = {0: 0xFE, 1: 0xFD, 2: 0xFB, 3: 0xF7}
ENDTAG = "00000000"


def lsb_apply(file: str, wmkFile: str, key: list, repeat: bool, outputFile: str, sound):
    """
    Hides a watermark inside an input wav file
    :param file: input audio file
    :param watermark: watermark string
    """
    watermark_bin = wmkToBin(wmkFile, sound) + ENDTAG
    nframes = sound.getnframes()

    sound.setpos(0)
    water_cursor = 0
    modifiedFrames = 0

    sound_new = wave.open(outputFile, 'w')
    sound_new.setparams(sound.getparams())

    for i in range(0, nframes):
        # Reads current sound frame
        currentFrame = sound.readframes(1)

        if water_cursor < len(watermark_bin):
            bit = 1 if watermark_bin[water_cursor] == "1" else 0
            # Mapping the bit to add with the corresponding bit in the sample
            keyvalue = i % len(key)
            modifiedFrames += 1
            sound_new.writeframes(mapping(currentFrame, bit, key[keyvalue])) 
        else:
            sound_new.writeframes(currentFrame)

        # At the end of the string : stop or repeat
        water_cursor = (water_cursor + 1)
        if repeat:
            water_cursor = water_cursor % len(watermark_bin)

    print("---- STATS ----")
    nbchannels = sound.getparams()[0]
    ratio = 8*nbchannels
    print("Carriage:\t" + str(len(watermark_bin)) + " bits")
    print("Max carriage:\t1 bit/" + str(ratio) + "=" + str(nframes)+ " bits")
    print("Mod. frames:\t" + str(modifiedFrames))
    print("Mod. bits:\t" + str(modifiedFrames*nbchannels)) 
    diffRatio = (modifiedFrames*100/(nframes*8))
    compareFiles(file + '.wav', outputFile)  

    return watermark_bin

def mapping(sample, wmk, keyval):
    """
    Transforms regular sample into watermarked sample
    """
    bit = wmk << (keyval)

    sample_new = [((sample[0] & masks[keyval]) | bit),
                  sample[1],
                  ((sample[2] & masks[keyval]) | bit),
                  sample[3]]

    return bytes(sample_new)


def getnframes(file: str):
    fileInput = file + '.wav'
    sound = wave.open(fileInput, 'r')
    return sound.getnframes()


def lsb_decode(limit: int, sound, key: list):
    bin_str = ''
    watermark = ""
    if(limit == 0):
        limit = sound.getnframes()

    for i in range(0, limit):
        currentFrame = sound.readframes(1)
        keyval = i % len(key)
        
        # We get the random mapped bit using the same mask
        bit = (currentFrame[0] >> key[keyval]) % 2
        bin_str += str(bit)
        
        if bin_str[-8:] == ENDTAG:
            break

    # Bin to STRING:
    byte_list = []
    for i in range(0, len(bin_str)//8):
        byte_list.append(0)
        for j in range(0, 8):
            # Binary to int
            if bin_str[i*8 + j] == '1':
                byte_list[-1] += 2**(7-j)

    # Recreating the watermark
    watermark = bytes(byte_list)
    return watermark


def lsb_read(file: str, key: list, limit: int):
    """
    Decoding watermark with the given key
    """
    fileInput = file + '.wav'
    sound = wave.open(fileInput, 'r')  # lecture d'un fichier audio
    sound.setpos(0)
    print("Opening "+fileInput)

    # Recreating the watermark
    watermark = lsb_decode(limit, sound, key)
    writeBinaryWmkFile(watermark, file)

    return watermark
