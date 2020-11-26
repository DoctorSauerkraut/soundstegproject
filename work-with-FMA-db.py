###################################
# LOAD MODULES
import audioread
import os
import glob

import sys
sys.path.append('/home/arthur/ISEN/Recherche/Stegano/work/db/FMA/fma/arthur_modifs/')
import utilsFMA
# only after this import our "utils" module!

from utils_audio import mp3_to_wav

###################################
dir_downloaded_db = '/media/arthur/DD_Sonif/db/fma_small/' # where all sounds have been stored (raw db)
output_db_dir = '/home/arthur/ISEN/Recherche/Stegano/work/db/FMA/working-dir/'
dir_metadata = '/media/arthur/DD_Sonif/db/fma_metadata/'
#file_metadata = 'raw_tracks.csv' #for 'raw_tracks.csv', interesting fields are track_url, track_genres, track_duration, format 'MM:SS'
 #other files for metadata: genres.csv, raw_albums.csv, raw_artists.csv, raw_genres.csv, raw_tracks.csv, tracks.csv
#tracks.csv: fields: track/genres, 

#tracks = utilsFMA.load(dir_metadata + 'raw_tracks.csv')
#genres = utilsFMA.load(dir_metadata + 'genres.csv')

#print(genres)

f = utilsFMA.get_audio_path(dir_downloaded_db, 2000) # /!\ --> change 2 with the key that is wanted
filename = f.split('/')[-1]
path = '/'.join(f.split('/')[:-1]) + '/'

if os.path.exists(path+filename):
    print('Found file ' + str(path+filename) + '! -> retrieving it...')
    os.system('cp ' + path+filename + ' ' + output_db_dir + filename)
else:
    print('File ' + str(current_path) + ' not found... trying next one')

########## CONVERT TO WAV
mp3_to_wav(output_db_dir+filename,rm_mp3=0)

#x, sr = librosa.load(filename[:-4] + '.wav', sr=None, mono=True) # mono=True???
signal = audioread.audio_open(output_db_dir+filename[:-4] + '.wav')

print('DONE... NOW POSSIBLY RUN <sudo rm *.mp3> IN YOUR WORKING DIRECTORY')
