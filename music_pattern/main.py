# -*- coding:utf-8 -*-
import os
import time
import librosa
import warnings
warnings.filterwarnings("ignore")

from audio_beat_detect import AudioBeatDetect
from audio_shot_detect import AudioShotDetect
from audio_energy_detect import AudioEnergyDetect


def audio_detect(audio_path):
    try:
        y, sr = librosa.load(audio_path)
    except:
        raise Exception(f"load file {audio_path} failed!")
    length = len(y) / sr
    if length > 1800 or length < 5:
        raise Exception("audio length error! (accept length:5s~600s)")
    # audio rhythm detect
    os.system(f"spleeter separate -i {audio_path} -o output")
    vocals_file = f"./output/{audio_path.split('/')[-1][:-4]}/vocals.wav"
    accompaniment_file = f"./output/{audio_path.split('/')[-1][:-4]}/accompaniment.wav"  
    if (not os.path.exists(vocals_file)) or (not os.path.exists(accompaniment_file)):
        raise Exception("opened spleeter error, maybe memory overflowed!")
    vocals_y, vocals_sr = librosa.load(vocals_file, sr=None)
    accompaniment_y, accompaniment_sr = librosa.load(accompaniment_file, sr=None)

    vocals_rhythm_times = {}
    if max(accompaniment_y) < 0.11:
        raise Exception("audio detected error, can not detected any melody from the audio!")
    elif max(vocals_y) < 0.25:
        beat_times = AudioBeatDetect(y)
        accompaniment_rhythm_times = AudioShotDetect(accompaniment_y, accompaniment_sr).getResult()
    else:
        beat_times = AudioBeatDetect(y)
        rhythm_times = AudioEnergyDetect(vocals_y, vocals_sr).getResult()
        vocals_rhythm_times['long break'] = rhythm_times[0]
        vocals_rhythm_times['short break'] = rhythm_times[1]
        accompaniment_rhythm_times = AudioShotDetect(accompaniment_y, accompaniment_sr).getResult()
    os.system("rm -rf ./output")
    # delete cache
    os.system("rm -rf /tmp/*")
    return beat_times, vocals_rhythm_times, accompaniment_rhythm_times
