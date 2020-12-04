###################################
# LOAD MODULES
import sys
sys.path.append('/home/arthur/ISEN/Recherche/Stegano/work/db/MTG-Jamendo/mtg-jamendo-dataset/scripts/')
import commons

import glob
import os
import pandas as pd
import numpy as np

from lsb import lsb_apply, lsb_read, getnframes, lsb_decode
from utils import compareFiles, decodeKeyFile
from spreadspectrum import dss_apply, dss_read

import utilsFMA

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
    #genre_id = str(int(np.array(genres_list.where(genres_list['title']==genre).dropna(how='all').dropna(axis=1))[0]))
    genre_id = int(np.array(genres_list['genre_id'][genres_list.where(genres_list['title']==genre).dropna(how='all').dropna(axis=1).index]))

    # --- load metadata
    tracks = utilsFMA.load(input_dir + 'tracks.csv')

    tab_id_duration = tracks['track', 'duration']
    track_ids = tab_id_duration.index
    track_durations = tab_id_duration.values

    tab_id_genres = np.array(tracks['track', 'genres'])
    if verbose:
        print('looking for genre \'' + genre + '\', that is genre id #' + str(genre_id))

    # --- loop over the metadata, select one genre en restrict to a given duration
    number_of_entries = 0; number_of_matching_entries = 0
    list_matching_keys = []
    for index in range(len(tab_id_duration)):
        current_genre = tab_id_genres[index]
        current_duration = track_durations[index]
        if verbose:
            print('duration is ' + str(current_duration) + ' --- genre is ' + str(current_genre))
        for current_genre_item in current_genre:
            #print('sought genre is ' + str(genre_id) + ' --- current genre is ' + str(current_genre_item))
            #print(str(type(current_genre_item)) + ' --- ' + str(type(genre_id)))
            if current_genre_item == genre_id:
                #print('plop')
                if current_duration > min_dur and current_duration < max_dur:
                    number_of_matching_entries+=1
                    list_matching_keys.append(track_ids[index])
        number_of_entries+=1

    print('There were ' + str(number_of_entries) + ' entries in the data base')
    print('There were ' + str(number_of_matching_entries) + ' matching entries in the data base')
    #print('Matching keys (track_id) are :' + str(list_matching_keys))

    return list_matching_keys,track_ids

###################################
def copySounds_FMA(list_keys_to_files,catalog,source_dir,destination_dir, **kwargs):

    verbose=kwargs.get('verbose', 0)

    nb_sounds_copied = 0

    # --- Retrieve the corresponding files and store them locally
    for numfile in range(len(list_keys_to_files)):
        current_id = list_keys_to_files[numfile]
        current_id_str = '{:06d}'.format(current_id)
        current_path = os.path.join(source_dir, current_id_str[:3], current_id_str + '.mp3')

        if os.path.exists(current_path):
            if verbose:
                print('Found file ' + str(current_path) + '! -> retrieving it...')
            os.system('cp ' + current_path + ' ' + destination_dir + str(current_id) + '.mp3')
            nb_sounds_copied+=1
        else:
            if verbose:
                print('File ' + str(current_path) + ' not found... trying next one')

    #f = utilsFMA.get_audio_path(dir_downloaded_db, 55123) # /!\ --> change 2 with the key that is wanted
    #filename = f.split('/')[-1]
    #path = '/'.join(f.split('/')[:-1]) + '/'
    print('There were ' + str(nb_sounds_copied) + ' sounds found and copied')
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
def copySounds_MTG(list_keys_to_files,catalog,source_dir,destination_dir, **kwargs):

    verbose=kwargs.get('verbose', 0)

    nb_sounds_copied = 0
    # --- Retrieve the corresponding files and store them locally
    for numfile in range(len(list_keys_to_files)):
        current_id = list_keys_to_files[numfile]
        current_path = source_dir + catalog[current_id]['path']
        if os.path.exists(current_path):
            if verbose:
                print('Found file ' + str(current_path) + '! -> retrieving it...')
            os.system('cp ' + current_path + ' ' + destination_dir + str(current_id) + '.mp3')
            nb_sounds_copied+=1
        else:
            if verbose:
                print('File ' + str(current_path) + ' not found... trying next one')

    print('There were ' + str(nb_sounds_copied) + ' sounds found and copied')
    return 0

###################################
def encodeInSound_old(fileName,wmkFile,**kwargs):

    algo=kwargs.get('algo', 'LSB')
    keyFile=kwargs.get('keyFile','/home/arthur/ISEN/Recherche/Stegano/work/key_test')
    alphaDSS=kwargs.get('alphaDSS',1)
    keyDSS=kwargs.get('seedkey',4)

    if(algo == "DSS"):
        a = dss_apply(fileName[:-4], wmkFile, keyDSS, alphaDSS, 4096) # old version
    elif(algo == "LSB"):
        key = decodeKeyFile(keyFile)
        lsb_apply(fileName[:-4], wmkFile, key, False)

    return 0

###################################
def encodeInSound(fileBasename, signal,wmkFile,**kwargs):

    algo=kwargs.get('algo', 'LSB')
    keyFile=kwargs.get('keyFile','/home/arthur/ISEN/Recherche/Stegano/work/key_test')
    alphaDSS=kwargs.get('alphaDSS',1)
    seedkey=kwargs.get('seedkey',0)
    repeat=kwargs.get('repeat',False)

    if(algo == "DSS"):
        dss_apply(fileBasename[:-4], wmkFile, seedkey, fileBasename[:-4] + '-DSS_alpha' + str(alphaDSS) + '.wav', signal, alphaDSS)

    elif(algo == "LSB"):
        key = decodeKeyFile(keyFile)
        lsb_apply(fileBasename[:-4], wmkFile, key, True, fileBasename[:-4] + '-LSB_repeat' + str(repeat) + '.wav', signal)
    
    return 0
