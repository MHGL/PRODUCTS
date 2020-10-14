# -*- coding:utf-8 -*-
import os
import sys
import time
import librosa
import warnings
warnings.filterwarnings("ignore")
import numpy as np
# from scipy.io import wavfile


def AudioBeatDetect(y, sr=22050):    
    onset_env = librosa.onset.onset_strength(y, sr=sr,aggregate=np.median)  
    tempo, beat_frames = librosa.beat.beat_track(onset_envelope=onset_env,sr=sr, trim=False)  
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)  

    odd=0
    even=0
    for i in range(len(beat_frames)):
        tmp = onset_env[beat_frames[i]]
        if(i%2==0):  
            even=even+tmp
        else:
            odd=odd+tmp
    flag1 = max(even,odd)/min(even,odd)

    first=0
    second=0
    third=0
    for i in range(len(beat_frames)):
        tmp = onset_env[beat_frames[i]]
        if(i%3==0):  
            first = first+tmp
        elif(i%3==1):
            second = second + tmp
        else:
            third = third+tmp
    flag2 = max(first,second,third)/min(first,second,third)

    if(flag1>flag2):
        if(even>odd):
            beat_times = beat_times[::2]
            beat_frames = beat_frames[::2]
        else:
            beat_times = beat_times[1::2]
            beat_frames = beat_frames[1::2]
    else:
        if(first>=second and first>=third):
            beat_times = beat_times[::3]
            beat_frames = beat_frames[::3]
        elif(second>=first and second>=third):
            beat_times = beat_times[1::3]
            beat_frames = beat_frames[1::3]
        else:
            beat_times = beat_times[2::3]
            beat_frames = beat_frames[2::3]

    for i in range(len(beat_times)):
        beat_times[i] = round(beat_times[i],3)
    return beat_times.tolist()


