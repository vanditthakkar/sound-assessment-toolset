'''
Author : Prashant Kumar
Date : 20.05.2016
Description: This module maps pitch to key
'''
import numpy as np
key_names = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
key0 = np.array([16.351,17.324,18.354,19.445,20.601,21.827,23.124,24.499,25.956,27.5,29.135,30.868])
key1 = key0 * 2;
key2 = key1 * 2;
key3 = key2 * 2;
key4 = key3 * 2;
key5 = key4 * 2;
key6 = key5 * 2;
key7 = key6 * 2;
key8 = key7 * 2;
key9 = key8 * 2;

#key_set = [key0,key1,key2,key3,key4,key5,key6,key7,key8,key9]

key_set = list(key0)+list(key1)+list(key2)+list(key3)+list(key4)+list(key5)+list(key6)+list(key7)+list(key8)+list(key9)
key_info = {'val':None,'octave':0}


def getInfo(data):
    index = key_set.index(data)
    key_info['octave'] = index//12
    key_info['val'] = key_names[index%12]
    return key_info

def calculateKey(pch):
    '''
    If found in range return key_info dict.
    '''
    #print type(pch)
    u = len(key_set)
    l = 0
    #print pch
    if pch < key_set[0] or pch > key_set[len(key_set)-1]:
        return key_info

    while l <= u:
        m = l + (u-l)/2
        left = key_set[m-1]
        mid = key_set[m]
        right = key_set[m+1]
        #print 'yo'
        if pch > mid:
            if pch < right:
                if right-pch < pch-mid:
                    return getInfo(right)
                else:
                    return getInfo(mid)
            l = m+1

        elif pch < mid:
            if pch > left:
                if pch-left < mid-pch:
                    return getInfo(left)
                else:
                    return getInfo(mid)
            u = m-1
        else:
            return getInfo(mid)
    return key_info

def getPerfectKey(pch):
    return calculateKey(pch)

#print key1
#print key2
