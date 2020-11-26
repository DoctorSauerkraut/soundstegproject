import glob
import os

from lsb import lsb_apply, lsb_read, getnframes, lsb_decode
from utils import compareFiles, decodeKeyFile
from spreadspectrum import dss_apply, dss_read

###################################
def mp3_to_wav(inputdir, **kwargs):

    rm_mp3=kwargs.get('rm_mp3', 1)
    verbose=kwargs.get('verbose', 0)

    # 1st, convert
    for filename in glob.glob(inputdir + '*'):
        if verbose:
            print('Processing file ' + str(filename))

        if filename[-4:] == '.mp3':
            os.system('ffmpeg -i ' + filename + ' ' + filename[:-4] + '.wav' + ' -loglevel quiet')
    
    # 2nd, remove mp3 files
    if rm_mp3:
        for filename in glob.glob(inputdir + '*.mp3'):
            os.system('rm ' + filename)

###################################
def copySounds_MTG(list_keys_to_files,catalog,source_dir,destination_dir):
    # --- Retrieve the corresponding files and store them locally
    for numfile in range(len(list_keys_to_files)):
        current_id = list_keys_to_files[numfile]
        current_path = source_dir + catalog[current_id]['path']
        if os.path.exists(current_path):
            print('Found file ' + str(current_path) + '! -> retrieving it...')
            os.system('cp ' + current_path + ' ' + destination_dir + str(current_id) + '.mp3')
        else:
            print('File ' + str(current_path) + ' not found... trying next one')

    return 0


###################################
def encodeInSound(fileName,wmkFile,**kwargs): # free adaptation from of Olive's committed version on github of "main.py" on master branch

    algo=kwargs.get('algo', 'LSB')
    keyFile=kwargs.get('keyFile','/home/arthur/ISEN/Recherche/Stegano/work/key_test')
    
    if(algo == "DSS"):
        a = dss_apply(fileName[:-4], wmkFile, 42, 4096)
    elif(algo == "LSB"):
        key = decodeKeyFile(keyFile)
        lsb_apply(fileName[:-4], wmkFile, key, False)
