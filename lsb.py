import wave
from utils import wmkToBin
import binascii
masks = {0: 0xFE, 1: 0xFD, 2: 0xFB, 3: 0xF7}


def lsb_apply(file: str, wmkFile: str, key: list):
    """
    Cache un watermark dans un fichier audio par methode LSB
    :param file: Le nom du fichier a  watermarke ( Ne pas mettre l'extension)
    :param watermark: Le Watermark a appliquer (String)
    """
    sound = wave.open(file + '.wav', 'r')  # lecture d'un fichier audio
    sound_new = wave.open(file + '_watermarked_lsb.wav', 'w')
    sound_new.setparams(sound.getparams())

    watermark_bin = wmkToBin(wmkFile, sound)

    # print("Binary Watermark: " + watermark_bin)

    print(sound.getparams())
    print("Total frames:"+str(sound.getnframes()))
    print("Ratio : 1/"+str(sound.getparams()[1]*8)+" bits")

    sound.setpos(0)
    water_cursor = 0
    for i in range(0, sound.getnframes()):

        bit = 1 if watermark_bin[water_cursor] == "1" else 0

        # At the end of the string : repeat
        water_cursor = (water_cursor + 1) % len(watermark_bin)

        byte_4 = sound.readframes(1)

        # Mapping the bit to add with the corresponding bit in the sample
        keyvalue = i % len(key)
        sound_new.writeframes(mapping(byte_4, bit, key[keyvalue])) 


def mapping(sample, wmk, keyval):
    """
    Transforms regular sample into watermarked sample
    """
    bit = wmk << (keyval)
    # print("OLD:\t"+sample.hex()+"\t"+str(bit)+"\t"+str(hex(masks[keyval]))+"\t"+str(keyval))

    # Regular LSB : two modifications (stereo signal)
    # print(sample)
    sample_dbg = [((sample[0] & masks[keyval])),
                  sample[1],
                  ((sample[2] & masks[keyval])),
                  sample[3]]
    # print(sample_dbg)

    sample_new = [sample_dbg[0] + bit,
                  sample_dbg[1],
                  sample_dbg[2] + bit,
                  sample_dbg[3]]
    # print(sample_new)

    byte_new = bytes(sample_new)
    # print("NEW:\t"+byte_new.hex())
    return byte_new


def lsb_read(file: str, key: list, stop_on_end: bool = True):
    """
    Decoding watermark with the given key
    """
    sound = wave.open(file + '.wav', 'r')  # lecture d'un fichier audio
    sound.setpos(0)

    bin_str = ''
    watermark = ""

    for i in range(0, sound.getnframes()):
        byte_4 = sound.readframes(1)
        keyval = i % len(key)

        # We get the random mapped bit using the same mask
        bit = (byte_4[0] >> key[keyval]) % 2

        bin_str += str(bit)
        # Unpadding (unstable)
        #if bin_str[-8:] == '00000000' and stop_on_end:
            #break
    # print(bin_str)

    # Bin to STRING:
    byte_list = []
    for i in range(0, len(bin_str)//8):
        byte_list.append(0)
        for j in range(0, 8):
            # Binary to int
            if bin_str[i*8 + j] == '1':
                byte_list[-1] += 2**(7-j)

    # Conversion to binary for benchmarking purposes
    binwmk = ""
    for b in byte_list:
        binwmk += bin(b)[2:].zfill(8)

    f = open(file+".wmk", "w+")
    f.write(binwmk)
    f.close()

    # Recreating the watermark
    watermark = bytes(byte_list)

    try:
        watermark = watermark.decode("utf-8")
    except:
        print("Watermark corrupted")

    return watermark
