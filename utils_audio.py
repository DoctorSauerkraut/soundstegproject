import glob
import os
import pandas as pd
import numpy as np

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
def selectSounds_FMA(input_dir, input_file, genre_dir, genre_catalog, **kwargs):

    min_dur=kwargs.get('min_dur', 0)
    max_dur=kwargs.get('max_dur', 600)
    genre=kwargs.get('genre', 'Metal')
    verbose=kwargs.get('verbose', 0)

    # --- convert genre to numeric value
    genres_list = pd.read_csv(genre_dir+genre_catalog)
    genre_id = str(int(np.array(genres_list.where(genres_list['title']==genre).dropna(how='all').dropna(axis=1))))

    # --- load metadata
    tracks = utilsFMA.load(dir_metadata + 'tracks.csv')

    tab_id_duration = tracks['track', 'duration']
    track_ids = tab_id_duration.index
    track_durations = tab_id_duration.values

    tab_id_genres = np.array(tracks['track', 'genres'])

    # --- loop over the metadata, select one genre en restrict to a given duration
    number_of_entries = 0; number_of_matching_entries = 0
    list_matching_keys = []
    for index in range(len(tab_id_duration)):
        if verbose:
            pass
        current_genre = tab_id_genres[index]
        current_duration = track_durations[index]
        for current_genre_item in current_genre:
            if current_genre_item == genre_id:
                if current_duration > min_dur and current_duration < max_dur:
                    #print(key)
                    number_of_matching_entries+=1
                    list_matching_keys.append(tab_ids[index])
        number_of_entries+=1

    print('There were ' + str(number_of_entries) + ' entries in the data base')
    print('There were ' + str(number_of_matching_entries) + ' matching entries in the data base')
    #print('Matching keys (track_id) are :' + str(list_matching_keys))

    return list_matching_keys,track_ids

###################################
def copySounds_FMA(list_keys_to_files,catalog,source_dir,destination_dir):
    # --- Retrieve the corresponding files and store them locally
    for numfile in range(len(list_keys_to_files)):
        current_id = list_keys_to_files[numfile]
        current_id_str = '{:06d}'.format(current_id)
        current_path = os.path.join(source_dir, current_id_str[:3], current_id_str + '.mp3')

        if os.path.exists(current_path):
            print('Found file ' + str(current_path) + '! -> retrieving it...')
            os.system('cp ' + current_path + ' ' + destination_dir + str(current_id) + '.mp3')
        else:
            print('File ' + str(current_path) + ' not found... trying next one')

    #f = utilsFMA.get_audio_path(dir_downloaded_db, 55123) # /!\ --> change 2 with the key that is wanted
    #filename = f.split('/')[-1]
    #path = '/'.join(f.split('/')[:-1]) + '/'

    return 0

###################################
def selectSounds_MTG(input_dir, input_file, **kwargs):

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
