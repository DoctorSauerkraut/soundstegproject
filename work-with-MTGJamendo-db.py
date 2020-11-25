###################################
# LOAD MODULES
import sys
sys.path.append('/home/arthur/ISEN/Recherche/Stegano/work/db/MTG-Jamendo/mtg-jamendo-dataset/scripts/')
import commons
#
import os
import librosa
import glob

import time
import wave

#from matplotlib import pyplot as plt

from lsb import lsb_apply, lsb_read, getnframes, lsb_decode
from utils import compareFiles, decodeKeyFile
from spreadspectrum import dss_apply, dss_read

###################################
def selectSounds(input_dir, input_file, genre, min_dur, max_dur, **kwargs):

    min_dur=kwargs.get('min_dur', 0)
    max_dur=kwargs.get('max_dur', 600)
    genre=kwargs.get('genre', 'metal')
    verbose=kwargs.get('verbose', 0)

    # --- load metadata
    tracks, tags, extra = commons.read_file(input_dir + input_file)
    # fields of 'tracks' are: artist_id, album_id, genre, instrument, mood/theme, path, dration, tags
    #print(tracks)

    # --- loop over the metadata, select one genre en restrict to a given duration
    number_of_entries = 0; number_of_matching_entries = 0
    list_matching_keys = []
    for key in tracks:
        if verbose:
            print('-----------' + '\n current entry: \n')
            print('artist_id:' + str(tracks[key]['artist_id']))
            print('album_id:' + str(tracks[key]['album_id']))
            print('genre:' + str(tracks[key]['genre']))
            print('instrument:' + str(tracks[key]['instrument']))
            print('mood/theme:' + str(tracks[key]['mood/theme']))
            print('path:' + str(tracks[key]['path']))
            print('duration:' + str(tracks[key]['duration']))
            print('tags:' + str(tracks[key]['tags']))

        current_genre = tracks[key]['genre']
        current_duration = tracks[key]['duration']
        for current_genre_item in current_genre:
            if current_genre_item == genre:
                if current_duration > min_dur and current_duration < max_dur:
                    #print(key)
                    number_of_matching_entries+=1
                    list_matching_keys.append(key)
        number_of_entries+=1

    print('There were ' + str(number_of_entries) + ' entries in the data base')
    print('There were ' + str(number_of_matching_entries) + ' matching entries in the data base')
    #print('Matching keys (track_id) are :' + str(list_matching_keys))

    return list_matching_keys, tracks

###################################
def copySounds(list_keys_to_files,catalog,source_dir,destination_dir):
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
def encodeInSound(fileName,wmkFile,**kwargs): # free adaptation from of Olive's committed version on github of "main.py" on master branch

    algo=kwargs.get('algo', 'LSB')
    keyFile=kwargs.get('keyFile','/home/arthur/ISEN/Recherche/Stegano/work/key_test')
    
    if(algo == "DSS"):
        a = dss_apply(fileName[:-4], wmkFile, 42, 4096)
    elif(algo == "LSB"):
        key = decodeKeyFile(keyFile)
        lsb_apply(fileName[:-4], wmkFile, key, False)

###################################
def main():
    ###################################
    # FLAGS
    sound_selection = 0 # use to browse the data base and collect the sounds we want (may be run only once)
    convert_format = 0 # use to convert selected sounds from mp3 to wav, if needed
    encode = 1 # use to encode the files from a given directory
    verbose = 0 # verbose mode for some functions

    ###################################
    # PATHS
    dir_downloaded_db = '/media/arthur/DD_Sonif/db/MTG-Jamendo-db/' # where all sounds have been stored (raw db)
    output_db_dir = '/home/arthur/ISEN/Recherche/Stegano/work/db/MTG-Jamendo/working-dir/'
    dir_metadata = '/home/arthur/ISEN/Recherche/Stegano/work/db/MTG-Jamendo/mtg-jamendo-dataset/data/'   
    metadata = 'autotagging_genre.tsv' #'autotagging.tsv', 'autotagging_instrument.tsv', 'autotagging_moodtheme.tsv', 'autotagging_top50tags.tsv'
    
    ###################################
    # GENERAL PARAMETERS
    display = 0

    ###################################
    # OTHER PARAMETERS
    # --- these ones for browsing the db and selecting files
    my_genre = 'metal'
    min_dur = 10# in seconds
    max_dur = 15# in seconds
    dest_dir_selected_sounds = '/home/arthur/ISEN/Recherche/Stegano/work/db/MTG-Jamendo/working-dir/'
    # --- these ones for loading and encoding
    encode_source_dir = '/home/arthur/ISEN/Recherche/Stegano/work/db/MTG-Jamendo/working-dir/'
    encode_dest_dir = '/home/arthur/ISEN/Recherche/Stegano/work/db/MTG-Jamendo/working-dir/encoded/'
    wmkFile_dir = '/home/arthur/ISEN/Recherche/Stegano/work/'
    wmkFile = 'watermark_test'
    keyFile = 'key_test'
    encoding_alg = 'LSB' # 'DSS' 'LSB'

    if sound_selection:
        print('---- scanning database ----')
        list_keys_selectedFiles,tracks = selectSounds(dir_metadata,metadata,genre=my_genre,min_dur=min_dur,max_dur=max_dur,verbose=verbose)
        print('---- copying sounds ----')
        copySounds(list_keys_selectedFiles,tracks,dir_downloaded_db,dest_dir_selected_sounds)
       
    if convert_format: 
        print('---- mp3->wav conversion ----')
        mp3_to_wav(dest_dir_selected_sounds, rm_mp3=1) #/!\ will remove the mp3 files once converted to wav

    if encode:
        print('---- encoding with ' + encoding_alg + ' ----')
        for filename in glob.glob(encode_source_dir + '*.wav'):
            if filename.find('_watermarked_') == -1: # don't process files already watermarked (may be removed in future versions)
                print('Processing file ' + str(filename))
                encodeInSound(filename,wmkFile_dir+wmkFile,algo=encoding_alg,keyFile=wmkFile_dir+keyFile)
                #signal = audioread.audio_open(inputdir + filename)
                #signal, sr = librosa.load(filename)
                #plt.plot(signal)
                #plt.show()

    return 0


if __name__ == "__main__":
    main()
