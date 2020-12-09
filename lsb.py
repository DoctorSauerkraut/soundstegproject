import wave
import time
from utils import *

masks = {0: 0xFE, 1: 0xFD, 2: 0xFB, 3: 0xF7}
STATAG = "010100110101010001000001" #STA 
ENDTAG = "010001010100111001000100" #END

def lsb_apply(file: str, wmkFile: str, key: list, repeat: bool, outputFile: str, sound):
    """
    Hides a watermark inside an input wav file
    :param file : Raw name (without extension)
    :param wmkFile : watermark string
    :param key : 0
    :param repeat : should the tag be repeated
    :param outputFile : output audio file
    :param sound : sound object
    """
    watermark_bin = STATAG + wmkToBin(wmkFile, sound) + ENDTAG
    nframes = sound.getnframes()

    sound.setpos(0)
    water_cursor = 0
    modifiedFrames = 0

    sound_new = wave.open(outputFile, 'w')
    sound_new.setparams(sound.getparams())
    p = Progress("Applying tag")
    p.progress(0, nframes)
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
        p.progress(i, nframes)
    p.progress(nframes, nframes)

    dprint("\n---- STATS ----", VER)
    nbchannels = sound.getparams()[0]
    ratio = 8*nbchannels
    dprint("Carriage:\t" + str(len(watermark_bin)) + " bits", VER)
    dprint("Max carriage:\t1 bit/" + str(ratio) + "=" + str(nframes)+ " bits", VER)
    dprint("Mod. frames:\t" + str(modifiedFrames), VER)
    dprint("Mod. bits:\t" + str(modifiedFrames*nbchannels), VER) 
    diffRatio = (modifiedFrames*100/(nframes*8))

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
    p = Progress("Decoding tag")
    p.progress(0, limit)

    for i in range(0, limit):
        currentFrame = sound.readframes(1)
        keyval = i % len(key)
        
        # We get the random mapped bit using the same mask
        bit = (currentFrame[0] >> key[keyval]) % 2
        
        bin_str += str(bit)
        
        if bin_str[-len(ENDTAG):] == ENDTAG:
            break
        p.progress(i, limit)
    p.progress(limit, limit)

    limit = len(bin_str)
    ps = Progress("Seeking")
    ps.progress(0, limit)
    while(bin_str[0:len(STATAG)] != STATAG):
        bin_str = bin_str[1:]
        ps.progress(limit-len(bin_str), limit)
    
        if(len(bin_str) < len(STATAG)):
            return bytes([])
    ps.progress(limit, limit)  

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
    dprint("Opening "+fileInput, VER)

    # Recreating the watermark
    watermark = lsb_decode(limit, sound, key)
    writeBinaryWmkFile(watermark, file)

    return watermark
