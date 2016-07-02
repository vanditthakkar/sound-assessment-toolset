from algos_librosa import *
import os
import pprint
import midiMap
import time
class Process(object):

    def __init__(self,file_name):
        self.attr = {}
        self.file_name = file_name


    def extractFeatures(self):
        y,sr = load(self.file_name)
        fs = 2*sr
        y_harmonic , y_precussive = effects.hpss(y)
        audio = y_harmonic
        onset_times = np.array([0])
        onset_times, onset_rate = getOnsets(audio,fs)
        segments = getSegments(audio,fs)
        self.attr = {'key':[],
                'octave':[],
                'scale':[],
                'loudness':[],
                'pitch':[],
                'times':[],
                'peak':[],
                'duration':[],
                'effective_duration':[],
        }
        k = 0
        for segment in segments:
            #key,scale = getKeyScale(segment)
            loudness = getLoudness(segment)
            pitch = getPitch(segment)
            key_dict = getPerfectKey(pitch[0])

            key = key_dict['val']
            octave = key_dict['octave']
            times = onset_times[k]
            duration = getDuration(segment)
            effective_duration = getEffectiveDuration(segment)
            peak = getPeak(segment)

            if effective_duration<0.01:
                continue
            if loudness<1:
                continue

            k += 1

            self.attr['key'].append(key)
            self.attr['octave'].append(octave)
            self.attr['loudness'].append(loudness)
            self.attr['pitch'].append(pitch)
            self.attr['effective_duration'].append(effective_duration)
            self.attr['times'].append(times)


    print "Written to midi file"

    def getLoud(self):
		return self.attr['loudness']
    def getKeys(self):
        return self.attr['key']
    def getPitch(self):
        return self.attr['pitch']
    def getTime(self):
        return self.attr['times']
    def getEffectiveDuration(self):
        return self.attr['effective_duration']

