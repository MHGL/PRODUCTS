# -*- coding:utf-8 -*-
import librosa
import warnings
warnings.filterwarnings("ignore")
import numpy as np

from config import time_unit, min_diff_threshold


class AudioShotDetect:
    def __init__(self, y, sr):
        self.y = y
        self.sr = sr
        self.total_time = round((len(y) / sr), 2)
        self.break_nums = int(self.total_time // 5)
        self.hop_length = int(sr * time_unit)

    def getDiff(self):
        S = np.abs(librosa.feature.melspectrogram(self.y, sr=self.sr, hop_length=self.hop_length))
        P = (librosa.power_to_db(S))
        diff = np.maximum(((P[:, 1:] - P[:, :-1]).sum(axis=0) / P.shape[0]), 0)
        return diff

    def getTimes(self):
        diff = self.getDiff()
        times = [round((i * time_unit), 2) for i in range(len(diff))]
        times[-1] = self.total_time
        return times

    def getResult(self):
        diff = self.getDiff()
        times = self.getTimes()
        indices = []
        for i in range(1, len(diff)):
            avg = diff[:i].mean() + 1e-3
            radio = diff[i] / avg
            if radio > min_diff_threshold:
                indices.append(i)
        result = [indices[0]]
        for i in range(1, len(indices)):
            if indices[i] - result[-1] > 1 / time_unit:
                result.append(indices[i])
        diff = np.array([diff[i] for i in result])
        if diff.size > self.break_nums:
            indices = diff.argsort()[::-1][:self.break_nums]
            result = [result[i] for i in indices]
        result = sorted([round(i*time_unit, 2) for i in result])
        return result


