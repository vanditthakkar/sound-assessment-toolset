from essentia.standard import MonoLoader
from essentia.standard import OnsetRate
from essentia.standard import Key
from essentia.standard import TonalExtractor
from essentia.standard import Loudness
from essentia.standard import PitchYin
from essentia.standard import Duration
from essentia.standard import PeakDetection
from essentia.standard import MFCC
from essentia.standard import MaxFilter
from essentia.standard import EffectiveDuration
from essentia.standard import TempoTapDegara
import key_mapping as kp
#import librosa
from librosa import load
from librosa import effects
import numpy as np

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

def getKeyScale(segment):
    '''
    Returns : Key, Scale
    '''
    tExtractor = TonalExtractor()
    key = tExtractor(segment)[2]
    scale = tExtractor(segment)[5]
    key_scale = [key,scale]
    return key_scale

def getLoudness(segment):
    loud = Loudness()
    loudness_val = loud(segment)
    return loudness_val

def getPitch(segment):
    #Pitch
    pitch = PitchYin()
    pitch_val = pitch(segment)
    return pitch_val

def getDuration(segment):
    duration = Duration()
    duration_val = duration(segment)
    return duration_val

def getPeak(segment):
    peak = PeakDetection()
    peak_val = peak(segment)
    return peak_val

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
