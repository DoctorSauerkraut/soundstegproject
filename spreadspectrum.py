import wave
import matplotlib.pyplot as plt
import numpy as np
import random
import sys

from utils import wmkToBin, writeBinaryWmkFile, text_from_bits


def correlation(x, y):
    """
    Computes the correlation between x and y
    """
    # print("x :"+str(x))
    # sprint("y :"+str(y))
    sumx = 0
    sumy = 0
    sumx_square = 0
    sumy_square = 0
    sum_product = 0
    nvalues = min(len(x), len(y))
    for i in range(0, nvalues):
        sumx += x[i]
        sumy += y[i]
        sumx_square += x[i]**2
        sumy_square += y[i]**2
        sum_product += x[i] * y[i]

    prod = nvalues * sum_product - (sumx * sumy)
    sumX = nvalues * sumx_square - sumx**2
    sumY = nvalues * sumy_square - sumy**2

    # print("SumX :"+str(sumX))
    # print("SumY :"+str(sumY))

    return prod / np.sqrt(float((sumX * sumY)))


def dss_apply(file: str, wmkFile: str, skey: int, alpha: float = 1):
    """
    Hides watermark in an audio file with DSS method
    :param file: wav input file
    :param watermark: watermark file
    :param alpha: pseudo-noise amplitude
    :param skey: noise generation key
    """
    sound = wave.open(file + '.wav', 'r')  # lecture d'un fichier audio
    outputFile = file + '_watermarked_dss.wav'
    sound_new = wave.open(outputFile, 'w')

    sound_new.setparams(sound.getparams())
    sample_size = sound.getsampwidth()
    channel_count = sound.getnchannels()

    watermark_bin = wmkToBin(wmkFile, sound)

    sound.setpos(0)
    bloc_size = sound.getnframes() // len(watermark_bin)
    random.seed(skey)

    write_temp = bytearray(b'')
    read_temp = sound.readframes(-1)

    for ii in range(0, len(watermark_bin)):
        bit = 1 if watermark_bin[ii] == "1" else 0

        pseudonoise = [random.randint(0, 1) for j in range(0, bloc_size)]

        for ij in range(0, bloc_size):
            bs = sample_size * channel_count
            start = bs * (ij + ii * bloc_size)
            end = bs * (ij + ii * bloc_size + 1)
            byte_4 = read_temp[start:end]

            int_4 = [int.from_bytes(byte_4[j * sample_size:(j+1) * sample_size],
                     "little") for j in range(0, channel_count)]

            # Normalization
            adding_int = int(alpha * (2 * pseudonoise[ij] - 1) * (bit - 0.5) * (-2))  

            # Calculate new byte following, actual sound, pseudo noise and alpha
            for k in range(0, channel_count):
                byte_int = int_4[k]

                byte_int += adding_int
                if byte_int < 0:
                    byte_int = 0

                if byte_int >= (1 << 8*sample_size):
                    byte_int = (1 << 8*sample_size) - 1

                # Else
                write_temp += byte_int.to_bytes(sample_size, "little")

    sound_new.writeframes(write_temp)
    
    # On ajoute les derniers samples
    sound_new.writeframes(sound.readframes(sound.getnframes() - bloc_size * len(watermark_bin)))
    
    print("--- DSS ENDED ---")
    print("Output file : "+outputFile)
    
    return watermark_bin


def dss_read(file: str, skey: int, size_watermark: int):
    """
    Lit le watermark cache dans un fichier par Direct Spread Spectrum
    :param file: Nom du fichier a decoder (Sans extension)
    :param skey: cle de generation des bruits
    :param size_watermark: taille du watermark a rechercher
    """
    inputFile = file + '.wav'
    sound = wave.open(inputFile, 'r')  # lecture d'un fichier audio

    print("Extracting from "+inputFile+" with DSS")
    sample_size = sound.getsampwidth()

    sound.setpos(0)
    nframes = sound.getnframes()
    bloc_size = sound.getnframes() // size_watermark
    random.seed(skey)

    watermark_bin = ''

    for _ in range(0, size_watermark):
        pseudonoise = [random.randint(0, 1) for j in range(0, bloc_size)]

        # Recup Big sample
        pn = []
        cw = []
        for i in range(0, bloc_size):
            # Samples to int
            cw += [int.from_bytes(sound.readframes(1)[:sample_size], "little")]
            pn += [2 * pseudonoise[i] - 1]

        watermark_bin += '1' if correlation(cw, pn) < 0 else '0'

    print(text_from_bits(watermark_bin))
    # writeBinaryWmkFile(watermark_bin, file)
    return watermark_bin


