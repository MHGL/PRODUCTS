# -*- coding:utf-8 -*-
import time
import librosa
import warnings
warnings.filterwarnings("ignore")
import numpy as np

from config import time_unit, min_energy_threshold


class AudioEnergyDetect:
    def __init__(self, y, sr):
        self.y = y
        self.hop_length = int(sr * time_unit)
        self.total_length = len(y)
        self.total_time = round(self.total_length/sr, 2)
        self.short_break_nums = int(self.total_time // 5)

    def getEnergy(self):
        radio = self.total_length // self.hop_length + 1
        energy = np.zeros(radio * self.hop_length)
        energy[:self.total_length] = self.y ** 2
        energy = energy.reshape((-1, self.hop_length))
        return energy.sum(axis=1)

    def getBreak(self):
        start, end = [], []
        energy = self.getEnergy()
        for i in range(len(energy)-1):
            if energy[i] < min_energy_threshold and energy[i+1] > min_energy_threshold:
                start.append(i)
            elif energy[i] > min_energy_threshold and energy[i+1] < min_energy_threshold:
                end.append(i)
            continue
        # filter long and short break base on the length of break
        break_long, break_length, temp = [], [], []
        if start[0] < end[0]:
            break_long.append(start[0])
            for i in range(1, len(start)):
                if start[i] - end[i-1] > 1 / time_unit:
                    break_long.append(start[i])
                elif start[i] - end[i-1] > 1:
                    temp.append(start[i])
                    break_length.append(start[i] - end[i-1])
                continue
        elif start[0] > end[0]:
            for i in range(len(start)):
                if start[i] - end[i] > 1 / time_unit:
                    break_long.append(start[i])
                elif start[i] - end[i-1] > time_unit:
                    temp.append(start[i])
                    break_length.append(start[i] - end[i-1])
                continue

        break_length = np.array(break_length)
        indices = break_length.argsort()[::-1][:self.short_break_nums]
        break_short = sorted([temp[i] for i in indices])

        return break_long, break_short
    
    def getResult(self):
        break_long, break_short = self.getBreak()
        break_long_time = [round(i*time_unit, 2) for i in break_long]
        break_short_time = [round(i*time_unit, 2) for i in break_short]
        return break_long_time, break_short_time


