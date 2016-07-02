import matplotlib.pyplot as plt
import json
from django.conf import settings
import sys
import os
from models import *

def result(id):
    #id = StudentFile.objects.latest('id').id
    #print "----------"+str(id)
    file_path = settings.MEDIA_ROOT + '/sound/' + str(id) + ".json"
    #file_path = os.getcwd()+'/media/sound/'+str(id)+'.json'
    f = open(file_path,'r').read()
    res = json.loads(f)

    l1 = len(res['times1'])
    l2 = len(res['times2'])
    if l1>=l2:
        max = l1
    else:
        max = l2
    plt.subplot(2, 1, 1)

    plt.xlim(0,10)

    plt.xlabel("Teacher")
    for i in range(max):
        if i <l1:
            plt.axvline(res['times1'][i],linewidth=2,ymax=0.5,ymin=0,label=res['keys1'][i])
            plt.text(res['times1'][i],0.5,res['keys1'][i],)
        else:
            plt.axvline(1, linewidth=2, ymax=0, ymin=0)


    plt.subplot(2, 1, 2)
    plt.xlim(0,10)

    plt.xlabel("Student")
    for i in range(max):
        if i < l2:
            plt.axvline(res['times2'][i], linewidth=2, ymax=0.5, ymin=0, label=res['keys2'][i])
            plt.text(res['times2'][i], 0.5, res['keys2'][i])
        else:
            plt.axvline(1, linewidth=2, ymax=0, ymin=0)

    img_path = settings.MEDIA_ROOT + '/images/' + str(id) + ".png"
    #img_path = os.getcwd()+'/media/images/'+ str(id) + '.png'
    
    plt.figure(figsize=(2,1))
    plt.savefig(img_path)

