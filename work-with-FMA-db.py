###################################
# LOAD MODULES
import os
import glob

from utils_audio import mp3_to_wav, selectSounds_FMA, copySounds_FMA, encodeInSound

def main():
    ###################################
    # FLAGS
    sound_selection = 1 # use to browse the data base and collect the sounds we want (may be run only once)
    convert_format = 1 # use to convert selected sounds from mp3 to wav, if needed
    encode = 1 # use to encode the files from a given directory
    verbose = 0 # verbose mode for some functions

    ###################################
    # PATHS
    dir_downloaded_db = '/media/arthur/DD_Sonif/db/fma_small/' # where all sounds have been stored (raw db)
    output_db_dir = '/home/arthur/ISEN/Recherche/Stegano/work/db/FMA/working-dir/'
    dir_metadata = '/media/arthur/DD_Sonif/db/fma_metadata/'
    metadata = 'tracks.csv'
    ###################################
    # GENERAL PARAMETERS
    display = 0

    ###################################
    # OTHER PARAMETERS
    # --- these ones for browsing the db and selecting files
    my_genre = 'Metal'
    min_dur = 10# in seconds
    max_dur = 200# in seconds
    dest_dir_selected_sounds = '/home/arthur/ISEN/Recherche/Stegano/work/db/FMA/working-dir/'
    # --- these ones for loading and encoding
    encode_source_dir = '/home/arthur/ISEN/Recherche/Stegano/work/db/FMA/working-dir/'
    encode_dest_dir = '/home/arthur/ISEN/Recherche/Stegano/work/db/FMA/working-dir/encoded/' # NOT IN USE
    wmkFile_dir = '/home/arthur/ISEN/Recherche/Stegano/work/'
    wmkFile = 'watermark_test'
    keyFile = 'key_test'
    encoding_alg = 'DSS' # 'DSS' 'LSB'

    if sound_selection:
        print('---- scanning database ----')
        list_keys_selectedFiles,track_ids = selectSounds_FMA(dir_metadata,metadata,dir_metadata,'genres.csv',genre=my_genre,min_dur=min_dur,max_dur=max_dur,verbose=verbose)
        print('---- copying sounds ----')
        copySounds_FMA(list_keys_selectedFiles,track_ids,dir_downloaded_db,dest_dir_selected_sounds)
       
    if convert_format: 
        print('---- mp3->wav conversion ----')
        mp3_to_wav(dest_dir_selected_sounds, rm_mp3=0) #/!\ Arthur: for some reason, mp3 files have strange permission behavior, regarless of my chmod attempts, they remain protected, they should be manually removed

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


    print('DONE... NOW POSSIBLY RUN <sudo rm *.mp3> IN YOUR WORKING DIRECTORY')

###################################
if __name__ == "__main__":
    main()


