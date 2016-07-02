from algos_librosa import *
from essentia.standard import MonoLoader
from essentia.standard import AudioLoader
from essentia.standard import Loudness
import os
import pprint
import time
fs = 44100
class Process(object):

    def __init__(self,file_name):
        self.attr = {}
        self.file_name = file_name

    def extractFeatures(self):
        # y, sr = load(self.file_name)
        audio = MonoLoader(filename=self.file_name)()

        #fs = 2*sr
        #y_harmonic , y_precussive = effects.hpss(y)
        #audio = y_harmonic


        self.attr = {'key':[],

                'loudness':[],

                'times':[],

                'effective_duration':[],
        }
        onset_times = np.array([0])
        duration = getDuration(audio)
        onset_times, onset_rate = getOnsets(audio, fs)

        onset_samples = [int(fs * i) for i in onset_times]  # gives sample number at particular

        onset_s = np.asarray(onset_samples)  # converting list in numpy array
        #print "Onsets (sample number)--> total " + str(len(onset_s))
        # print onset_s
        onset_sx = np.insert(onset_s, len(onset_samples),duration * fs)  # onset contains all onset + last element is time when file ends
        #print "including time duration as last element , total length = " + str(len(onset_sx))

        # finding onset segments
        onset_segments = np.array([audio[onset_sx[i]:onset_sx[i + 1]] for i in range(0, len(onset_sx) - 1)])
        print "total segments " + str(len(onset_segments))

        m = 0
        loudness_raw = np.empty([len(onset_s)])
        eff_duration = np.empty([len(onset_s)])
        #print self.file_name
        #print ""
        #print ""
        ind = 0
        slop_in = 0
        slop = []
        sll = []  # slope*1000/loudness
        key_ar = []
        inte = []
        # ans_final=["ge","te","ka","na"]
        ans_final = []

        onset_segments_new = np.array([audio[onset_s[i]:onset_s[i] + (int)(fs * 0.4)] for i in range(0, len(onset_s))])
        #print " final array length " + str(len(onset_segments_new))


        for segment in onset_segments_new:
            # print segment
            ind = ind + 1
            #print "index->",
            #print ind

            # print li
            #print ""
            loud = Loudness()
            if (segment.size > int(0.3 * fs)):
                loudness_raw[m] = loud(abs(segment.take(list(range(int(0.3 * fs))))))
            else:
                loudness_raw[m] = loud(abs(segment))

            factor = 1000

            array = []
            for i in range(0, int(segment.size / factor)):
                # if(int((i+1)*0.02*fs)>segment.size):
                #    break
                y = abs(segment.take(list(range(int(i * factor), int((i + 1) * factor)))))
                w = np.amax(y)
                array.insert(i, w)
                # print  "max : "+str(w)
            array.sort()
            # print array
            print(len(array))

            if (loudness_raw[m] > 2.5 and len(array) > 10):
                # print "values from getkey are->"
                # print getkey(segment)
                # print "values from getdance are->"
                # print getdance(segment)
                # inte.insert(slop_in,getdance(segment))
                slope = (array[len(array) - 1] * array[len(array) - 1] * array[len(array) - 1] - array[len(array) - 3] * array[
                    len(array) - 3] * array[len(array) - 3])
                if (loudness_raw[m] > 1 and slope < 45):
                    # print "slope calculated   "+str(slope*1000)
                    slop.insert(slop_in, slope * 1000)
                    sll.insert(slop_in, slope * 100000 / loudness_raw[m])
                    slop_in = slop_in + 1
                    seg_value = []
                    seg_value.insert(0, slope * 100000 / loudness_raw[m])
                    seg_value.insert(1, slope * 1000)

                    modCent = getModCent(segment)
                    #print modCent

                    rollof = getRolloff(segment)
                    #print rollof
                    seg_value.insert(2, modCent)
                    seg_value.insert(3, rollof)

                    ans_filter = filterpani(seg_value)
                    print "answer from filter is:->"
                    print ans_filter
                    #ans_final = list(set(ans_final).union(set(ans_filter)))
                    # if(len())
                    print ""
                    eduration = EffectiveDuration()
                    eff_duration[m] = eduration(segment)
                    # vandit filter call starts
                    self.attr['key'].append(ans_filter)
                    print self.attr['key']
                    self.attr['loudness'].append(round(loudness_raw[m], 2))
                    print self.attr['loudness']
                   # self.attr['pitch'].append(pitch)
                    self.attr['effective_duration'].append(eduration)
                    self.attr['times'].append(onset_times[m])


            # print "Effective Duration : "+str(eff_duration[m])
            m = m + 1
        slop.sort()
        #print slop
        sll.sort()
        #print sll
        inte.sort()

        #print "anser final-->"
        print ans_final
        '''
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
            self.attr['loudness'].append(round(loudness,2))
            self.attr['pitch'].append(pitch)
            self.attr['effective_duration'].append(effective_duration)
            self.attr['times'].append(times)
        '''

    print "done file"

    def getLoud(self):
		return self.attr['loudness']
    def getKeys(self):
        return self.attr['key']
    def getTime(self):
        return self.attr['times']
    def getEffectiveDuration(self):
        return self.attr['effective_duration']

