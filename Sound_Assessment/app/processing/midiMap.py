import midi
import numpy as np
import os
key_names = {'C':12,'C#':13,'D':14,'D#':15,'E':16,'F':17,'F#':18,'G':19,'G#':20,'A':21,'A#':22,'B':23}



file_name = ""
def midiMap(attr,f_name):

    pattern = midi.Pattern()
    track = midi.Track()
    pattern.append(track)

    file_name = f_name
    print 'length = '+str(len(attr))

    for k in range(len(attr['key'])):
        # Instantiate a MIDI note on event, append it to the track
        #print "midi."+str(attr['key'][k])+"_"+str(attr['octave'][k])
        key = attr['key'][k]
        #print key
        octave = attr['octave'][k]

        #print key_names[key]
        key_number = key_names[key] + 12*(octave-1)
        #print key_number
        #pitch = eval("midi."+str(key)+"_"+str(octave))
        pitch = key_number
        #print pitch
        ed = attr['effective_duration'][k] * 500
        if k==(len(attr['key'])-1):
            timing_f = 50*ed
            timing_i = 0

        else :
            timing_f = attr['times'][k+1] * 1000
            timing_i = attr['times'][k] * 1000


        #print timing_f - timing_i
        #print "ed = " +str(ed)
        on = midi.NoteOnEvent(tick=0, velocity=70, pitch=pitch)
        track.append(on)
        off = midi.NoteOffEvent(tick=int(timing_f - timing_i - ed) , pitch=pitch)
        track.append(off)
        on = midi.NoteOnEvent(tick=1, velocity=0, pitch=pitch)
        track.append(on)        
        off = midi.NoteOffEvent(tick=1, pitch=pitch)
        track.append(off)
        
      



    eot = midi.EndOfTrackEvent(tick=1)
    track.append(eot)
    #print pattern
    file_name = os.path.basename(file_name).split('.')[0]
    print(file_name)
    path = "recorded_to_midi/" + file_name + ".mid"
    midi.write_midifile(path, pattern)
