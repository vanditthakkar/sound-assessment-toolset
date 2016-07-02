from essentia.standard import MonoLoader
from essentia.standard import AudioLoader
from essentia.standard import OnsetRate
from essentia.standard import Key
from essentia.standard import Centroid
from essentia.standard import MaxFilter
from essentia.standard import LowPass
from essentia.standard import Trimmer
from essentia.standard import MetadataReader
from essentia.standard import Duration
from essentia.standard import MFCC
from essentia.standard import Loudness
from essentia.standard import RollOff
from essentia.standard import EffectiveDuration
from essentia.standard import TempoTapDegara
from essentia.standard import KeyExtractor
from essentia.standard import PitchYin
from essentia.standard import Variance
from essentia.standard import Mean
from collections import Counter
import key_mapping as kp

import numpy as np
fs = 44100.0

def getOnsets(audio,fs):
    '''
    Returns:  onset_times, onset_rate
    '''
    get_onsets = OnsetRate()
    return get_onsets(audio)


def getSegments(audio,fs):
    '''
    Returns the segments of audio file with repect to onsets detected
    '''
    onset_times = np.array([0])
    onset_times , onset_rate = getOnsets(audio,fs)

    onset_samples = [int(fs*i) for i in onset_times ]
    #segments
    frame_sz = int(0.2 * fs)
    segments = np.array([audio[i:i+frame_sz] for i in onset_samples] )
    return segments

def concatenateSegments(segments, fs=44100, pad_time=0.3):
    padded_segments = [np.concatenate([segment, np.zeros(int(pad_time*fs))]) for segment in segments]
    return np.concatenate(padded_segments)


def getLoudness(segment):
    loud = Loudness()
    loudness_val = loud(segment)
    return loudness_val


def getMFCC(segment):
    mfcc = MFCC()
    mfcc_val = mfcc(segment)
    return mfcc_val

def maxFilter(segment):
    mxFilter = MaxFilter()
    return mxFilter(segment)

def getPerfectKey(pitch):
    return kp.getPerfectKey(pitch)

def getEffectiveDuration(segment):
    effective_duration = EffectiveDuration()
    effective_duration_val = effective_duration(segment)
    return effective_duration_val

def getTempo(segments):
    tempo = TempoTapDegara()
    return tempo(segments)


# define all the access methods here

def is_outlier(points, thresh):
    if len(points.shape) == 1:
        points = points[:, None]

    median = np.mean(points, axis=0)
    diff = np.sum((points - median) ** 2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)

    modified_z_score = 0.6745 * diff / (med_abs_deviation + 0.00000001)
    modified_z_score_arr = np.asarray(modified_z_score)
    # print modified_z_score
    # print modified_z_score_arr
    ans = np.ones(len(points), dtype=bool)
    k = 0
    errorPts = []
    for point in points:
        if point > median:
            ans[k] = False
        else:

            ans[k] = modified_z_score_arr[k] > thresh
            if ans[k] == True:
                errorPts.append(k)

        k = k + 1

    return ans, errorPts







def getDuration(segment):
    duration = Duration()
    duration_val = duration(segment)
    return duration_val




def get_mean(segment):
    mean = Mean()
    mean_val = mean(segment)
    return mean_val



'''
def getCentroid(segment):
    centroid = Centroid()
    centroid_val = centroid(segment)
    return centroid_val
'''


def getCentroid(segment):
    cent = 0
    weight = 0
    for i in range(0, segment.size - 1):
        cent += (i + 1) * abs(segment[i])
        weight += abs(segment[i])
    cent /= weight
    return cent


def getPitch(segment):
    # Pitch
    pitch = PitchYin()
    pitch_val, m = pitch(segment)
    return pitch_val


def getRolloff(segment):
    rolloff = RollOff()
    rolloff_val = rolloff(segment)
    return rolloff_val


def getVar(segment):
    var = Variance()
    var_val = var(segment)
    return var_val


def getModCent(segment):
    cent = 0
    weight = 0
    for i in range(0, segment.size - 1):
        cent += (segment.size - i) * abs(segment[i])
        weight += abs(segment[i])
    cent /= weight
    return cent


def getkey(segment):
    key = KeyExtractor()
    key_val = key(segment)
    return key_val
import itertools
import operator

def most_common(L):
  # get an iterable of (item, iterable) pairs
  SL = sorted((x, i) for i, x in enumerate(L))
  # print 'SL:', SL
  groups = itertools.groupby(SL, key=operator.itemgetter(0))
  # auxiliary function to get "quality" for an item
  def _auxfun(g):
    item, iterable = g
    count = 0
    min_index = len(L)
    for _, where in iterable:
      count += 1
      min_index = min(min_index, where)
    # print 'item %r, count %r, minind %r' % (item, count, min_index)
    return count, -min_index
  # pick the highest-count/earliest item
  return max(groups, key=_auxfun)[0]

def filterpani(seg_value):
    sll_ = {"ge": [0, 300], "te": [2300, 7200], "ka": [320, 6000], "na": [500, 4700]}
    slop_ = {"ge": [0, 50], "te": [975, 1100], "ka": [0, 999], "na": [250, 1000]}
    ans_slop = []
    ans_sll = []
    ans_ind = 0
    # pass sll to the first, then slop
    for k in sll_:
        if (seg_value[0] > sll_[k][0] and seg_value[0] < sll_[k][1]):
            ans_sll.insert(ans_ind, k)
            ans_ind = ans_ind + 1
    ans_ind = 0
    for k in slop_:
        if (seg_value[1] > slop_[k][0] and seg_value[1] < slop_[k][1]):
            ans_slop.insert(ans_ind, k)
            ans_ind = ans_ind + 1

    modcent_ = {"ge": [7500, 8700], "te": [8500, 16000], "ka": [9300, 10500], "na": [9000, 10000]}
    roll_ = {"ge": [6500, 19000], "te": [1200, 3800], "ka": [1200, 2200], "na": [1300, 13000]}
    ans_mod = []
    ans_roll = []
    ans_ind = 0
    # pass modcent to the first, then rolloff
    for k in modcent_:
        if (seg_value[2] > modcent_[k][0] and seg_value[2] < modcent_[k][1]):
            ans_mod.insert(ans_ind, k)
            ans_ind = ans_ind + 1
    ans_ind = 0
    for k in roll_:
        if (seg_value[3] > roll_[k][0] and seg_value[3] < roll_[k][1]):
            ans_roll.insert(ans_ind, k)
            ans_ind = ans_ind + 1
    print ans_mod
    print ans_roll
    print ans_slop
    print ans_sll
    ans = ans_mod + ans_roll + ans_slop + ans_sll
    count = Counter(ans)
    ans1=count.most_common()[0]

    # print ans
    #uniq = set(ans)
    #ans = list(uniq)
    #ans1 = most_common(ans)
    print ans1[0]
    return ans1[0]