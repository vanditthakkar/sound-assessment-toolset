import process
import difflib
import pdb
import time
import json
from django.conf import settings
import swalign
import math
import random

#indianNote = {'C#':'Sa','D#':'Re','F':'Ga','F#':'Ma','G#':'Pa','A#':'Dh','C':'Ni', 'D':'Reb','E':'Gab','G':'Ma#','A':'Dhb','D':'Nib'}
#indianNote = {'Ge':'Ge','Ghe':'Ghe','Ka':'Ka','Na':'Na','Te':'Te','Re':'Re'}
indianNote = {'Ge':'','Ghe':'','Ka':'','Na':'','Te':'','Re':''}

def getScore(s1,s2):

	match = 2
	mismatch = -1
	scoring = swalign.NucleotideScoringMatrix(match, mismatch)

	sw = swalign.LocalAlignment(scoring)
	alignment = sw.align(s1, s2)
	print alignment.score
	lengt=len(s1)
	scc = (alignment.score/lengt)*50
	score=int(scc+49)%50 + random.randrange(0, 100, 3)%30
	print "Score is  "+ str(score)
	return  score

def grade(filename1,filename2,id):
	file1 = filename1
	file2 = filename2

	fileObj1 = process.Process(file1)
	fileObj2 = process.Process(file2)
	fileObj1.extractFeatures()
	fileObj2.extractFeatures()
	diff = difflib.Differ()

	loudness1 = [loud for loud in fileObj1.getLoud()]
	loudness2 = [loud for loud in fileObj2.getLoud()]

	keys1 = [k for k in fileObj1.getKeys()]
	keys2 = [k for k in fileObj2.getKeys()]
	print "aaaaaaaaa"
	print keys1
	print keys2
	print "aaaaaaaaa"
	times1 = [float(time0) for time0 in fileObj1.getTime()]
	times2 = [float(time0) for time0 in fileObj2.getTime()]

	result = list(diff.compare(keys1,keys2))
	missed = []
	extra = []

	for i in result:
		if i.startswith('-'):
			missed.append(i[1:])	
		if i.startswith('+'):
			extra.append(i[1:])

	#print result
	#print "Missed : "+str(missed)
	#print "Extra : "+str(extra)

	missed = []
	extra = []
	print len(loudness2)
	print len(keys2)
	print len(times2)

	s1 = ""
	s2 = ""
	for i in keys1:
		s1 += str(i)

	for i in keys2:
		s2 += str(i)


	print s1
	print s2

	# TODO : Compute
	score = getScore(s1,s2)

	# TODO : Pani
	results = {'loudness1':loudness1,'loudness2':loudness2,'keys1':keys1,'keys2':keys2,'times1':times1,'times2':times2,'missed':missed,'extra':extra,'score':score}
	#file_path = settings.MEDIA_ROOT+'/sound/'+str(id)+".json"
	file_path = '/var/www/html/Sound_Assessment/media/sound/'+str(id)+'.json'
	with open(file_path,"w") as fp:
		json.dump(results,fp)

	return results
