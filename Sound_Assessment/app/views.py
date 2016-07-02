from django.shortcuts import render
import sys
from models import *
import os
import grade
from django.conf import settings
import time
import threading


from django.views.decorators.csrf import csrf_exempt
import requests


def posting(params2,back_url):
    r = requests.post(back_url, params2)


@csrf_exempt
def lti(request):
    score = 1
    print "hi  aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa  " + score
    if 'oauth_consumer_key' in request.POST :
        oauth_consumer_key = request.POST['oauth_consumer_key']
        lis_result_sourcedid = request.POST['lis_result_sourcedid']
        lis_outcome_service_url = request.POST['lis_outcome_service_url']
        back_url = request.POST['back_url']
        test_id = request.POST['custom_test_id']
        params2 = {
            'score': 0.2,
            'oauth_consumer_key': oauth_consumer_key,
            'lis_result_sourcedid': lis_result_sourcedid,
            'lis_outcome_service_url': lis_outcome_service_url,
            'test_id': test_id,
            'back_url': back_url,

        }
        request.session['p'] = params2


    if request.method == "POST":
        params2 = request.session['p']
        form = StudentFileForm(request.POST, request.FILES)
        teacher = TeacherFile.objects.get(num=params2['test_id'])
        print form.is_valid()
        if form.is_valid():

            data = form.save()
            id = data.id
            print "Hi"
            print "id = " + str(id)
            student = StudentFile.objects.get(id=id)

            turl = settings.MEDIA_ROOT + str(teacher.file_upload.url).replace("media/", "")
            surl = settings.MEDIA_ROOT + str(student.file_upload.url).replace("media/", "")
            print turl

            results = grade.grade(turl, surl, id)
            score = results['score']
            #print "hi  aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa  "+score
            params2['score']=score

            thObj = threading.Thread(target=draw, args=[id])
            thObj.start()
            thObj.join()

            print "It Worked"
            posting(params2, params2['back_url'])

            missed = ""
            extra = ""

            for miss in results['missed']:
                missed += miss

            for ex in results['extra']:
                extra += ex

            if missed == "":
                missed = "None"
            if extra == "":
                extra = "None"

            context = {'form': form, 'flag': True, 'teacher': teacher, 'student': student, 'id': id, 'missed': missed,
                       'extra': extra,'score':score*10}
        else:
            context = {'form': form, 'flag': False, 'teacher': teacher, 'score':score}
        return render(request, "app/home.html", context)

    elif request.method == "GET":


        teacher = TeacherFile.objects.get(num=test_id)
        form = StudentFileForm()
        context = {'form': form, 'flag': False, 'teacher': teacher,'score':score}
        return render(request, "app/lti.html", context)



def draw(id):
    f = "python "+os.getcwd()+'/app/result_graph.py '+str(id)
    os.system(f)

@csrf_exempt
def home(request,lesson=1):
    print settings.MEDIA_ROOT
    teacher = TeacherFile.objects.get(num=lesson)
    print type(teacher)

    if request.method == "POST":
        form = StudentFileForm(request.POST, request.FILES)

        print form.is_valid()
        if form.is_valid():
            data = form.save()
            id = data.id
            print "id = "+str(id)
            student = StudentFile.objects.get(id=id)

            turl = settings.MEDIA_ROOT+str(teacher.file_upload.url).replace("media/","")
            surl = settings.MEDIA_ROOT+str(student.file_upload.url).replace("media/", "")
            print turl
            print surl
            results = grade.grade(turl,surl,id)

            thObj = threading.Thread(target=draw, args=[id])
            thObj.start()
            thObj.join()

            missed = ""
            extra = ""

            for miss in results['missed']:
                missed+=miss

            for ex in results['extra']:
                extra += ex

            if missed == "":
                missed = "None"
            if extra == "":
                extra = "None"

            context = {'form':form,'flag':True,'teacher':teacher,'student':student,'id':id,'missed':missed,'extra':extra}
        else:
            context = {'form':form,'flag':False,'teacher':teacher}
        return render(request,"app/home.html",context)

    elif request.method == "GET":
        form = StudentFileForm()
        context = {'form':form,'flag':False,'teacher':teacher}
        return render(request,"app/home.html",context)

