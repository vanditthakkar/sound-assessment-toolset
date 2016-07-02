
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import json
#from django.conf import settings
import sys
import os
import math
#from models import *

def normalise(x,mx,mn):
    return (x )/ (mx)

def result(id):
    #id = StudentFile.objects.latest('id').id
    #print "----------"+str(id)
    #file_path = settings.MEDIA_ROOT + '/sound/' + str(id) + ".json"
    #file_path = os.getcwd()+'/media/sound/'+str(id)+'.json'
    file_path = '/var/www/html/Sound_Assessment/media/sound/' + str(id) + '.json'
    f = open(file_path,'r').read()
    res = json.loads(f)
    mx1 = max(res['loudness1'])
    mx2 = max(res['loudness2'])
    mn1 = min(res['loudness1'])
    mn2 = min(res['loudness2'])
    l1 = len(res['times1'])
    l2 = len(res['times2'])
    if l1>=l2:
        maxx = l1
    else:
        maxx = l2


    missed = [str(i)[1] for i in res['missed']]
    extra = [str(i)[1] for i in res['extra']]

    m1 = missed
    e1 = extra
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 1, 1)
    plt.xlim(0,25)
    plt.ylabel('Loudness')
    plt.xlabel("Teacher")
    print "Missed " + str(missed)
    if res['keys1'][0] in m1:
        print "yo"
    else:
        print "No"


    temp = {}
    for i in range(l1):
        if i <l1:
            if res['keys1'][i] in m1:
            #if True:
                print "key1 : "+ str(normalise(res['loudness1'][i],mx1,mn1))
                #m1.remove(res['keys1'][i])
                plt.axvline(res['times1'][i], linewidth=5, ymax=normalise(res['loudness1'][i],mx1,mn1), ymin=0, label=res['keys1'][i],color = 'r')
            else:
                plt.axvline(res['times1'][i],linewidth=5,ymax=normalise(res['loudness1'][i],mx1,mn1),ymin=0,label=res['keys1'][i])
            plt.text(res['times1'][i],normalise(res['loudness1'][i],mx1,mn1)+0.03,res['keys1'][i],fontsize=7)
        else:
            plt.axvline(1, linewidth=5, ymax=0, ymin=0)


    plt.subplot(2, 1, 2)
    plt.xlim(0,25)
    plt.ylabel('Loudness')
    plt.xlabel("Student")



    for i in range(l2):
        print "key2 : " + str(normalise(res['loudness2'][i], mx2, mn2)) + "loudness : "+str(res['loudness2'][i])
        if i < l2:
            if res['keys2'][i] in e1:

            #if True:
                #e1.remove(res['keys2'][i])
                plt.axvline(res['times2'][i], linewidth=5, ymax=normalise(res['loudness2'][i],mx2,mn2), ymin=0, label=res['keys2'][i],color = 'r' )

            else:
                plt.axvline(res['times2'][i], linewidth=5, ymax=normalise(res['loudness2'][i],mx2,mn2), ymin=0, label=res['keys2'][i])
            plt.text(res['times2'][i], normalise(res['loudness2'][i],mx2,mn2)+0.03, res['keys2'][i],fontsize=7)
        else:
            plt.axvline(1, linewidth=2, ymax=0, ymin=0)

    #img_path = settings.MEDIA_ROOT + '/images/' + str(id) + ".png"
    #img_path = os.getcwd()+'/media/images/'+ str(id) + '.png'
    img_path = '/var/www/html/Sound_Assessment/media/images/' + str(id) + '.png'
    plt.subplots_adjust(hspace=.5)
    plt.savefig(img_path)

result(sys.argv[1])