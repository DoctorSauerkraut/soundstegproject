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

from utils_audio import mp3_to_wav, copySounds_MTG, encodeInSound, selectSounds_MTG

###################################
def main():
    ###################################
    # FLAGS
    sound_selection = 1 # use to browse the data base and collect the sounds we want (may be run only once)
    convert_format = 1 # use to convert selected sounds from mp3 to wav, if needed
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
    my_genre = 'jazz'
    min_dur = 10# in seconds
    max_dur = 100# in seconds
    dest_dir_selected_sounds = '/home/arthur/ISEN/Recherche/Stegano/work/db/MTG-Jamendo/working-dir/'
    # --- these ones for loading and encoding
    encode_source_dir = '/home/arthur/ISEN/Recherche/Stegano/work/db/MTG-Jamendo/working-dir/'
    encode_dest_dir = '/home/arthur/ISEN/Recherche/Stegano/work/db/MTG-Jamendo/working-dir/encoded/' # NOT IN USE
    wmkFile_dir = '/home/arthur/ISEN/Recherche/Stegano/work/'
    wmkFile = 'watermark_test'
    keyFile = 'key_test'
    #encoding_alg = 'LSB' # 'DSS' 'LSB'

    if sound_selection:
        print('---- scanning database ----')
        list_keys_selectedFiles,tracks = selectSounds_MTG(dir_metadata,metadata,genre=my_genre,min_dur=min_dur,max_dur=max_dur,verbose=verbose)
        print('---- copying sounds ----')
        copySounds_MTG(list_keys_selectedFiles,tracks,dir_downloaded_db,dest_dir_selected_sounds)
       
    if convert_format: 
        print('---- mp3->wav conversion ----')
        mp3_to_wav(dest_dir_selected_sounds, rm_mp3=1) #/!\ will remove the mp3 files once converted to wav

    if encode:
        for filename in glob.glob(encode_source_dir + '*.wav'):
            if (filename.find('-DSS') == -1) and (filename.find('-LSB') == -1): # don't process files already watermarked (may be removed in future versions)
                print('Processing file ' + str(filename))
                sound = wave.open(filename[:-4] + '.wav', 'r')
                for encoding_alg in ['LSB','DSS']:
                    if encoding_alg == 'DSS':
                        SEEDKEY = 1
                        for ALPHA in [1,5,10,50,100,500,1000,5000]:
                            print('---- encoding with ' + encoding_alg + ' ----')
                            encodeInSound(filename,sound,wmkFile_dir+wmkFile,algo=encoding_alg,alphaDSS=ALPHA, seedkey=SEEDKEY)
                    elif encoding_alg == 'LSB':
                        for REPEAT in [False, True]:
                            print('---- encoding with ' + encoding_alg + ' ----')
                            encodeInSound(filename,sound,wmkFile_dir+wmkFile,algo=encoding_alg,repeat=REPEAT,keyFile=wmkFile_dir+keyFile)


    return 0

###################################
if __name__ == "__main__":
    main()
